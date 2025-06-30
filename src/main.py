#!/usr/bin/env python3
import shutil
from subprocess import CompletedProcess
from typing import ClassVar, TypeAlias
from pathlib import Path
import zipfile
import os

from src.config.config import (
    BOOT_SIGNING_KEY,
    GKI_URL,
    OUTPUT,
    TOOLCHAIN,
    WORKSPACE,
)
from src.pre_build.kpm import KPMPatcher
from src.pre_build.lxc import LXCPatcher
from src.pre_build.setup_env import SetupEnvironment
from src.pre_build.ksu import KSUInstaller
from src.pre_build.variants import Variants
from src.utils.builder import Builder
from src.utils.fs import FileSystem
from src.utils.log import log
from src.utils.shell import Shell
from src.utils.source import SourceManager

# ====== Typing Aliases ======
Proc: TypeAlias = CompletedProcess[bytes]


# ====== Kernel Builder ======
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
        self.local_run: bool = os.getenv("LOCAL_RUN", "false").lower() == "true"

    def run_build(self) -> None:
        """
        Run the complete build process.

        :return: None
        """

        # ====== Setup Environment ======
        log("Setting up environment variables...")
        self.environment.setup_env()

        # ====== Create Workspace ======
        reset: list[Path] = [WORKSPACE, TOOLCHAIN, OUTPUT]
        log(f"Resetting paths: {WORKSPACE}, {TOOLCHAIN}, {OUTPUT}")
        for path in reset:
            self.fs.reset_path(path)

        # ====== Clone Kernel & Toolchain ======
        log("Cloning kernel and toolchain repositories...")
        self.source.clone_sources()

        # Export environment variables for GitHub Actions after clone kernel
        if not self.local_run:
            self.environment.export_github_env()

        # ====== Build  ======
        # Enter Workspace
        self.fs.cd(WORKSPACE)

        # Setup KSU and LXC
        self.ksu.install()
        self.lxc.apply()

        # Main build process
        self.builder.build()

        # ====== Patch KPM =====
        self.kpm.patch()

        # ====== Build AnyKernel3 ======
        self.build_anykernel3()

        # ====== Build Boot Image ======
        self.build_boot_image()

        # ====== Rename Build Artifacts ======
        log("Renaming build artifacts...")
        anykernel_path: Path = OUTPUT / "AnyKernel3.zip"
        boot_image_path: Path = OUTPUT / "boot.img"

        anykernel_path.rename(
            OUTPUT
            / f"ESK-{self.builder.get_kernel_version()}{self.variants.suffix}-AnyKernel3.zip"
        )
        boot_image_path.rename(
            OUTPUT
            / f"ESK-{self.builder.get_kernel_version()}{self.variants.suffix}-boot.img"
        )

    def build_anykernel3(self) -> None:
        """
        Build a AnyKernel3 flashable zip.

        :return: None
        """
        log("Preparing to build AnyKernel3 package...")

        _anykernel_path: Path = WORKSPACE / "AnyKernel3"

        shutil.copyfile(self.image_path, _anykernel_path / "Image.gz")

        shutil.make_archive(
            base_name=str(OUTPUT / "AnyKernel3"),
            format="zip",
            root_dir=_anykernel_path,
            base_dir=".",
        )

        log(f"Created AnyKernel3.zip at {OUTPUT}")

    def build_boot_image(self) -> None:
        """
        Build a boot image.

        :return: None
        """

        log("Starting boot image creation process...")
        _boot_tmp: Path = WORKSPACE / "boot"
        _unpack_bootimg: Path = TOOLCHAIN / "mkbootimg" / "unpack_bootimg.py"
        _mkbootimg: Path = TOOLCHAIN / "mkbootimg" / "mkbootimg.py"
        _avbtool: Path = TOOLCHAIN / "build-tools" / "linux-x86" / "bin" / "avbtool"

        self.fs.reset_path(_boot_tmp)  # Create a temp folder to build boot image
        self.fs.cd(_boot_tmp)

        log(f"Downloading GKI image from {GKI_URL}...")
        self.shell.run(["wget", "-qO", str(_boot_tmp / "gki.zip"), GKI_URL])

        with zipfile.ZipFile(_boot_tmp / "gki.zip", "r") as zip:
            zip.extractall(_boot_tmp)

        log("Unpacking boot image...")
        self.shell.run(
            [
                "python3",
                str(_unpack_bootimg),
                f"--boot_img={str(_boot_tmp / 'boot-5.10.img')}",
            ]
        )

        log("Copying kernel image to boot directory...")
        shutil.copyfile(self.image_path, _boot_tmp / "Image.gz")

        log("Rebuilding boot.img using mkbootimg.py...")
        self.shell.run(
            [
                "python3",
                str(_mkbootimg),
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

        log("Signing boot.img with avbtool...")
        self.shell.run(
            [
                str(_avbtool),
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

        shutil.move(_boot_tmp / "boot.img", OUTPUT / "boot.img")
        log(f"Boot image created at {OUTPUT}")


if __name__ == "__main__":
    build: KernelBuilder = KernelBuilder()
    build.run_build()
