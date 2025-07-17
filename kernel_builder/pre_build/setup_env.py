import os
from typing import Final
from pathlib import Path
from kernel_builder.config.config import BUILD_HOST, BUILD_USER
from kernel_builder.constants import (
    LLVM,
    LLVM_IAS,
    LTO_CLANG_FULL,
    LTO_CLANG_THIN,
    TOOLCHAIN,
    CLANG_TRIPLE,
    CROSS_COMPILE,
)
from kernel_builder.utils.build import Builder
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
        os.environ["LLVM"] = LLVM
        os.environ["LLVM_IAS"] = LLVM_IAS

        # Clang LTO (Thin, Full)
        os.environ["CONFIG_LTO_CLANG_THIN"] = LTO_CLANG_THIN
        os.environ["CONFIG_LTO_CLANG_FULL"] = LTO_CLANG_FULL

        # Set ll.lld as the linker
        os.environ["LD"] = str(self.CLANG_BIN / "ld.lld")

    def setup_env(self) -> None:
        """Set up the environment for building the kernel."""
        self.config_kbuild()
        self.config_path()
        self.config_cross_compile()
        self.config_llvm()


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
