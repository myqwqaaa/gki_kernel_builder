from .config import WORKSPACE, TOOLCHAIN
from typing import Final, TypeAlias

Source: TypeAlias = Final[dict[str, str]]

KERNEL: Source = {
    "url": "github.com:bachnxuan/android12-5.10-lts",
    "branch": "esk/main",
    "to": str(WORKSPACE),
}

ANYKERNEL: Source = {
    "url": "github.com:bachnxuan/AnyKernel3",
    "branch": "android12-5.10",
    "to": str(WORKSPACE / "AnyKernel3"),
}

BUILD_TOOL: Source = {
    "url": "android.googlesource.com:kernel/prebuilts/build-tools",
    "branch": "main-kernel-build-2024",
    "to": str(TOOLCHAIN / "build-tools"),
}

MKBOOTIMG: Source = {
    "url": "android.googlesource.com:platform/system/tools/mkbootimg",
    "branch": "main-kernel-build-2024",
    "to": str(TOOLCHAIN / "mkbootimg"),
}

# CLANG: Source = {
#     "url": "gitlab.com:crdroidandroid/android_prebuilts_clang_host_linux-x86_clang-r547379.git",
#     "branch": "15.0",
#     "to": str(TOOLCHAIN / "clang"),
# }

SUSFS: Source = {
    "url": "gitlab.com:simonpunk/susfs4ksu.git",
    "branch": "gki-android12-5.10",
    "to": str(WORKSPACE / "susfs4ksu"),
}

WILD_PATCHES: Source = {
    "url": "github.com:WildKernels/kernel_patches",
    "branch": "main",
    "to": str(WORKSPACE / "kernel_patches"),
}

SOURCES: Final[list[Source]] = [
    KERNEL,
    ANYKERNEL,
    BUILD_TOOL,
    MKBOOTIMG,
    SUSFS,
    WILD_PATCHES,
]

AOSP_REPO: Final[str] = (
    "https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/+/mirror-goog-main-llvm-toolchain-source"
)
AOSP_ARCHIVE: Final[str] = (
    "https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/+archive/mirror-goog-main-llvm-toolchain-source"
)

if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
