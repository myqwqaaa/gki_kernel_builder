import tarfile
from pathlib import Path
from kernel_builder.utils.clang import fetch_clang
from kernel_builder.utils.command import aria2c
from kernel_builder.config.config import (
    CLANG_URL,
    CLANG_VARIANT,
    IMAGE_COMP,
    KERNEL_NAME,
    OUTPUT,
)
from kernel_builder.constants import TOOLCHAIN, WORKSPACE
from kernel_builder.post_build.flashable import FlashableBuilder
from kernel_builder.post_build.kpm import KPMPatcher
from kernel_builder.pre_build.setup_env import SetupEnvironment
from kernel_builder.pre_build.susfs import SUSFSPatcher
from kernel_builder.pre_build.variants import Variants
from kernel_builder.utils.build import Builder
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log
from kernel_builder.utils.source import SourceManager
from kernel_builder.post_build.export_env import GithubExportEnv
from kernel_builder.utils.env import (
    ksu_variant,
    susfs_enabled,
    lxc_enabled,
    verbose_enabled,
)


class KernelBuilder:
    def __init__(self) -> None:
        self.builder: Builder = Builder()
        self.variants: Variants = Variants()
        self.environment: SetupEnvironment = SetupEnvironment()
        self.kpm: KPMPatcher = KPMPatcher()
        self.fs: FileSystem = FileSystem()
        self.source: SourceManager = SourceManager()
        self.susfs: SUSFSPatcher = SUSFSPatcher()
        self.flashable: FlashableBuilder = FlashableBuilder()
        self.export_env: GithubExportEnv = GithubExportEnv()

        boot_dir: Path = WORKSPACE / "out" / "arch" / "arm64" / "boot"
        image: Path = boot_dir / "Image"
        self.image_path: Path = (
            image if IMAGE_COMP == "raw" else image.with_suffix(f".{IMAGE_COMP}")
        )

    def run_build(self) -> None:
        """
        Run the complete build process.
        """
        log(
            f"Build Config: {ksu_variant()=}, {susfs_enabled()=}, {lxc_enabled()=}, {verbose_enabled()}"
        )

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
        clang_url: str = CLANG_URL or fetch_clang(CLANG_VARIANT)
        dest: Path = TOOLCHAIN
        tarball: Path = dest / "tarball"
        clang: Path = dest / "clang"

        aria2c("-d", str(dest), "-o", "tarball", clang_url)
        FileSystem.reset_path(clang)

        with tarfile.open(tarball, "r:*") as tar:
            tar.extractall(clang)

        tarball.unlink()

        # Enter workspace
        self.fs.cd(WORKSPACE)

        # Pre-build steps
        self.variants.setup()

        # Main build steps
        self.builder.build()

        # Post build
        self.kpm.patch()
        self.export_env.export_github_env()

        # Build flashable
        self.flashable.build_anykernel3()
        self.flashable.build_boot_image()

        # Rename artifacts
        log("Renaming build artifacts...")
        version: str | None = self.builder.get_kernel_version()
        suffix: str = self.variants.suffix
        anykernel_src: Path = OUTPUT / "AnyKernel3.zip"
        boot_src: Path = OUTPUT / "boot.img"

        anykernel_dest: Path = (
            OUTPUT / f"{KERNEL_NAME}-{version}{suffix}-AnyKernel3.zip"
        )
        boot_dest: Path = OUTPUT / f"{KERNEL_NAME}-{version}{suffix}-boot.img"

        anykernel_src.rename(anykernel_dest)
        boot_src.rename(boot_dest)
