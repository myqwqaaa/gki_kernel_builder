from .config import WORKSPACE, TOOLCHAIN
from typing import Final


KERNEL: Final[dict[str, str]] = {
    "url": "github.com:bachnxuan/android12-5.10-lts",
    "branch": "android12-5.10-lts",
    "to": str(WORKSPACE),
}

ANYKERNEL: Final[dict[str, str]] = {
    "url": "github.com:bachnxuan/AnyKernel3",
    "branch": "android12-5.10",
    "to": str(WORKSPACE / "AnyKernel3"),
}

BUILD_TOOL: Final[dict[str, str]] = {
    "url": "android.googlesource.com:kernel/prebuilts/build-tools",
    "branch": "main-kernel-build-2024",
    "to": str(TOOLCHAIN / "build-tools"),
}

MKBOOTIMG: Final[dict[str, str]] = {
    "url": "android.googlesource.com:platform/system/tools/mkbootimg",
    "branch": "main-kernel-build-2024",
    "to": str(TOOLCHAIN / "mkbootimg"),
}

CLANG: Final[dict[str, str]] = {
    "url": "gitlab.com:crdroidandroid/android_prebuilts_clang_host_linux-x86_clang-r547379.git",
    "branch": "15.0",
    "to": str(TOOLCHAIN / "clang"),
}

SUSFS: Final[dict[str, str]] = {
    "url": "gitlab.com:simonpunk/susfs4ksu.git",
    "branch": "gki-android12-5.10",
    "to": str(WORKSPACE / "susfs4ksu"),
}

SOURCES: Final[list[dict[str, str]]] = [
    KERNEL,
    ANYKERNEL,
    BUILD_TOOL,
    MKBOOTIMG,
    CLANG,
    SUSFS,
]

if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
