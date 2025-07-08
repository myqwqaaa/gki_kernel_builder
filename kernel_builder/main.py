#!/usr/bin/env python3
# encoding: utf-8

from pathlib import Path
from subprocess import CompletedProcess
from typing import ClassVar, TypeAlias

from kernel_builder.config.config import (
    OUTPUT,
    TOOLCHAIN,
    WORKSPACE,
)
from kernel_builder.post_build.flashable import FlashableBuilder
from kernel_builder.post_build.kpm import KPMPatcher
from kernel_builder.pre_build.lxc import LXCPatcher
from kernel_builder.pre_build.setup_env import SetupEnvironment
from kernel_builder.pre_build.ksu import KSUInstaller
from kernel_builder.pre_build.susfs import SUSFSPatcher
from kernel_builder.pre_build.variants import Variants
from kernel_builder.utils import env
from kernel_builder.utils.build import Builder
from kernel_builder.utils.clang import fetch_latest_aosp_clang
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
        self.flashable: FlashableBuilder = FlashableBuilder()
        self.local_run: bool = env.local_run()

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

        # Clone Clang
        fetch_latest_aosp_clang()

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
        self.kpm.patch()

        # Build flashable
        self.flashable.build_anykernel3()
        self.flashable.build_boot_image()

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


if __name__ == "__main__":
    try:
        KernelBuilder().run_build()
    except Exception as err:
        log(str(err), "error")
