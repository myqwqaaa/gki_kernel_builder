#!/usr/bin/env python3
from pathlib import Path
from typing import Final, Literal

# ====== Paths ======
ROOT: Final[Path] = Path(__file__).resolve().parent.parent.parent
WORKSPACE: Final[Path] = ROOT / "kernel"
TOOLCHAIN: Final[Path] = ROOT / "toolchain"
PATCHES: Final[Path] = ROOT / "kernel_patches"
VARIANT_JSON: Final[Path] = ROOT / "kernel_builder" / "config" / "variants.json"

# ====== Build ======
DEFCONFIG: Final[str] = "gki_defconfig"
BUILD_USER: Final[str] = "gki-builder"
BUILD_HOST: Final[str] = "esk"
IMAGE_COMP: Final[Literal["raw", "lz4", "gz"]] = "gz"  # <raw|lz4|gz>

# ====== Artifacts ======
# Build Output
OUTPUT: Final[Path] = ROOT / "dist"

# Boot Image
BOOT_SIGNING_KEY: Final[Path] = ROOT / "key" / "key.pem"
GKI_URL: Final[str] = (
    "https://dl.google.com/android/gki/gki-certified-boot-android12-5.10-2025-05_r1.zip"
)

# ====== Logging ======
# Optional: Set log file
LOGFILE: Final[str | Path | None] = None

# ====== Compile ======
# Force LLVM binutils and Clang IAS
LLVM: Final[str] = "1"
LLVM_IAS: Final[str] = "1"

# Clang LTO (Default: Thin)
LTO_CLANG_THIN: Final[str] = "y"
LTO_CLANG_FULL: Final[str] = "n"

# Cross compiling
CLANG_TRIPLE: Final[str] = "aarch64-linux-gnu-"
CROSS_COMPILE: Final[str] = "aarch64-linux-gnu-"

if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
