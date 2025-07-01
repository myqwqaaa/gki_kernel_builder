import os
from typing import Final
from pathlib import Path
from kernel_builder.config.config import (
    BUILD_HOST,
    BUILD_USER,
    TOOLCHAIN,
    CLANG_TRIPLE,
    CROSS_COMPILE,
    OUTPUT,
)
from kernel_builder.utils.builder import Builder
from kernel_builder.pre_build.variants import Variants


class SetupEnvironment:
    """Set up necessary environment variables for building the kernel."""

    CLANG_BIN: Final[Path] = TOOLCHAIN / "clang" / "bin"

    def __init__(self) -> None:
        self.builder: Builder = Builder()
        self.variants: Variants = Variants()

    def config_kbuild(self) -> None:
        os.environ["KBUILD_BUILD_USER"] = BUILD_USER
        os.environ["KBUILD_BUILD_HOST"] = BUILD_HOST

    def config_path(self) -> None:
        os.environ["PATH"] = f"{self.CLANG_BIN}{os.pathsep}{os.environ.get('PATH', '')}"

    def config_cross_compile(self) -> None:
        os.environ["CLANG_TRIPLE"] = CLANG_TRIPLE
        os.environ["CROSS_COMPILE"] = CROSS_COMPILE

    def config_llvm(self) -> None:
        # Force LLVM binutils and Clang IAS
        os.environ["LLVM"] = "1"
        os.environ["LLVM_IAS"] = "1"

        # Force Thin LTO
        os.environ["CONFIG_LTO_CLANG_THIN"] = "y"
        os.environ["CONFIG_LTO_CLANG_FULL"] = "n"

        # Set ll.lld as the linker
        os.environ["LD"] = str(self.CLANG_BIN / "ld.lld")

    def export_github_env(self) -> None:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"output={OUTPUT}\n")
            f.write(f"version={self.builder.get_kernel_version()}\n")
            f.write(f"variant={self.variants.suffix}\n")

    def setup_env(self) -> None:
        """Set up the environment for building the kernel."""
        self.config_kbuild()
        self.config_path()
        self.config_cross_compile()
        self.config_llvm()


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
