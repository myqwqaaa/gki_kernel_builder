#!/usr/bin/env python3
from pathlib import Path
from typing import Final

# ====== Paths ======
ROOT: Final[Path] = Path(__file__).resolve().parent.parent.parent
WORKSPACE: Final[Path] = ROOT / "kernel"
TOOLCHAIN: Final[Path] = Path("/opt/toolchain")

# ====== Build ======
DEFCONFIG: Final[str] = "esk_defconfig"
BUILD_USER: Final[str] = "gki-builder"
BUILD_HOST: Final[str] = "esk"

# ====== Artifacts ======
OUTPUT: Final[Path] = ROOT / "dist"  # To store build artifacts

# Boot Image
BOOT_SIGNING_KEY: Final[Path] = ROOT / "key" / "key.pem"
GKI_URL: Final[str] = (
    "https://dl.google.com/android/gki/gki-certified-boot-android12-5.10-2025-05_r1.zip"
)

# ====== Logging ======
LOGFILE: Final[str | Path | None] = None  # Optional: Set log file

# ====== Cross Compile ======
CLANG_TRIPLE: Final[str] = "aarch64-linux-gnu-"
CROSS_COMPILE: Final[str] = "aarch64-linux-gnu-"

if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
