#!/usr/bin/env python3
# encoding: utf-8

import os
import shutil
import zipfile
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import ClassVar, TypeAlias

from kernel_builder.config.config import (
    BOOT_SIGNING_KEY,
    GKI_URL,
    OUTPUT,
    ROOT,
    TOOLCHAIN,
    WORKSPACE,
)
from kernel_builder.post_build.kpm import KPMPatcher
from kernel_builder.pre_build.lxc import LXCPatcher
from kernel_builder.pre_build.setup_env import SetupEnvironment
from kernel_builder.pre_build.ksu import KSUInstaller
from kernel_builder.pre_build.susfs import SUSFSPatcher
from kernel_builder.pre_build.variants import Variants
from kernel_builder.utils.builder import Builder
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log
from kernel_builder.utils.shell import Shell
from kernel_builder.utils.source import SourceManager

# ====== Typing Aliases ======
Proc: TypeAlias = CompletedProcess[bytes]


class KernelBuilder:
    image_path: ClassVar[Path] = (
        WORKSPACE / "out" / "arch" / "arm64" / "boot" / "Image.gz"
    )

    def __init__(self) -> None:
        self.builder: Builder = Builder()
        self.variants: Variants = Variants()
        self.environment: SetupEnvironment = SetupEnvironment()
        self.shell: Shell = Shell()
        self.ksu: KSUInstaller = KSUInstaller()
        self.fs: FileSystem = FileSystem()
        self.source: SourceManager = SourceManager()
        self.lxc: LXCPatcher = LXCPatcher()
        self.kpm: KPMPatcher = KPMPatcher()
        self.susfs: SUSFSPatcher = SUSFSPatcher()
        self.local_run: bool = os.getenv("LOCAL_RUN", "false").lower() == "true"

    def run_build(self) -> None:
        """
        Run the complete build process.
        """
        log("Setting up environment variables...")
        self.environment.setup_env()

        # Reset paths
        reset_paths = [WORKSPACE, TOOLCHAIN, OUTPUT]
        log(f"Resetting paths: {', '.join(map(str, reset_paths))}")
        for path in reset_paths:
            self.fs.reset_path(path)

        # Clone sources
        log("Cloning kernel and toolchain repositories...")
        self.source.clone_sources()

        # Export GitHub Actions env if not local
        if not self.local_run:
            self.environment.export_github_env()

        # Enter workspace
        self.fs.cd(WORKSPACE)

        # Pre-build steps
        self.variants.setup()

        # Main build steps
        self.builder.build()

        # Post build
        kmi_checker: Path = (
            ROOT / "kernel_builder" / "post_build" / "KMI_function_symbols_test.py"
        )

        self.kpm.patch()

        subprocess.run(["python3", str(kmi_checker)], cwd=WORKSPACE, check=True)

        # Build flashable
        self.build_anykernel3()
        self.build_boot_image()

        # Rename artifacts
        log("Renaming build artifacts...")
        version: str | None = self.builder.get_kernel_version()
        suffix: str = self.variants.suffix
        anykernel_src: Path = OUTPUT / "AnyKernel3.zip"
        boot_src: Path = OUTPUT / "boot.img"

        anykernel_dest: Path = OUTPUT / f"ESK-{version}{suffix}-AnyKernel3.zip"
        boot_dest: Path = OUTPUT / f"ESK-{version}{suffix}-boot.img"

        anykernel_src.rename(anykernel_dest)
        boot_src.rename(boot_dest)

    def build_anykernel3(self) -> None:
        """
        Build a flashable AnyKernel3 ZIP package.
        """
        log("Preparing to build AnyKernel3 package...")

        ak_dir = WORKSPACE / "AnyKernel3"
        shutil.copyfile(self.image_path, ak_dir / "Image.gz")
        shutil.make_archive(
            base_name=str(OUTPUT / "AnyKernel3"),
            format="zip",
            root_dir=ak_dir,
            base_dir=".",
        )

        log(f"Created AnyKernel3.zip at {OUTPUT}")

    def build_boot_image(self) -> None:
        """
        Create and sign the boot image from the GKI release.
        """
        log("Starting boot image creation process...")

        boot_tmp = WORKSPACE / "boot"
        unpacker = TOOLCHAIN / "mkbootimg" / "unpack_bootimg.py"
        maker = TOOLCHAIN / "mkbootimg" / "mkbootimg.py"
        avbtool = TOOLCHAIN / "build-tools" / "linux-x86" / "bin" / "avbtool"

        # Prepare temp directory
        self.fs.reset_path(boot_tmp)
        self.fs.cd(boot_tmp)

        # Download and extract GKI
        log(f"Downloading GKI image from {GKI_URL}...")
        self.shell.run(["wget", "-qO", str(boot_tmp / "gki.zip"), GKI_URL])
        with zipfile.ZipFile(boot_tmp / "gki.zip", "r") as z:
            z.extractall(boot_tmp)

        log("Unpacking boot image...")
        self.shell.run(
            [
                "python3",
                str(unpacker),
                f"--boot_img={boot_tmp / 'boot-5.10.img'}",
            ]
        )

        log("Copying kernel image to boot directory...")
        shutil.copyfile(self.image_path, boot_tmp / "Image.gz")

        log("Rebuilding boot.img with mkbootimg.py...")
        self.shell.run(
            [
                "python3",
                str(maker),
                "--header_version",
                "4",
                "--kernel",
                "Image.gz",
                "--output",
                "boot.img",
                "--ramdisk",
                "out/ramdisk",
                "--os_version",
                "12.0.0",
                "--os_patch_level",
                "2025-05",
            ]
        )

        # Sign the image
        log("Signing boot.img with avbtool...")
        self.shell.run(
            [
                str(avbtool),
                "add_hash_footer",
                "--partition_name",
                "boot",
                "--partition_size",
                str(64 * 1024 * 1024),
                "--image",
                "boot.img",
                "--algorithm",
                "SHA256_RSA2048",
                "--key",
                str(BOOT_SIGNING_KEY),
            ]
        )

        shutil.move(boot_tmp / "boot.img", OUTPUT / "boot.img")
        log(f"Boot image created at {OUTPUT}")


if __name__ == "__main__":
    KernelBuilder().run_build()
