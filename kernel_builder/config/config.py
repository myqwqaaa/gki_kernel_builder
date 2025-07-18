from pathlib import Path
from typing import Final, Literal
from kernel_builder.constants import ROOT

# Build Info
DEFCONFIG: Final[str] = "gki_defconfig"
BUILD_USER: Final[str] = "gki-builder"
BUILD_HOST: Final[str] = "esk"
IMAGE_COMP: Final[Literal["raw", "lz4", "gz"]] = "gz"

# Clang
CLANG_VARIANT: Final[Literal["SLIM", "AOSP", "RV", "YUKI", "LILIUM", "NEUTRON"]] = (
    "AOSP"
)
CLANG_URL: str | None = None

# AnyKernel3
ANYKERNEL_REPO = "github.com:bachnxuan/AnyKernel3"
ANYKERNEL_BRANCH = "android12-5.10"

# Build Output
OUTPUT: Final[Path] = ROOT / "dist"

# Boot Image Config
BOOT_SIGNING_KEY: Final[Path] = ROOT / "key" / "key.pem"
GKI_URL: Final[str] = (
    "https://dl.google.com/android/gki/gki-certified-boot-android12-5.10-2025-05_r1.zip"
)

# Logging
LOGFILE: Final[str | Path | None] = None

if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
