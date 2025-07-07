import shutil
import os

from subprocess import CompletedProcess
from kernel_builder.config.config import WORKSPACE
from kernel_builder.utils.env import ksu_variant, susfs_enabled
from kernel_builder.utils.shell import Shell
from kernel_builder.utils.log import log
from typing import TypeAlias
from pathlib import Path


Proc: TypeAlias = CompletedProcess[bytes]


class SUSFSPatcher:
    def __init__(self) -> None:
        self.shell: Shell = Shell()
        self.ksu_variant: str = ksu_variant()
        self.susfs: bool = susfs_enabled()

    def copy(self, src: Path, dest: Path):
        log(f"Copying content from folder {src} to {dest}")
        for entry in os.scandir(src):
            src_path: str = entry.path
            dst_path: str = os.path.join(dest, entry.name)
            if entry.is_dir():
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)

    def apply(self) -> Proc | None:
        if self.ksu_variant == "NONE" or not self.susfs:
            return

        os.chdir(WORKSPACE)

        SUSFS: Path = WORKSPACE / "susfs4ksu" / "kernel_patches"
        GKI_SUSFS: Path = SUSFS / "50_add_susfs_in_gki-android12-5.10.patch"
        KSU_SUSFS: Path = SUSFS / "KernelSU" / "10_enable_susfs_for_ksu.patch"

        log("Applying kernel-side SUSFS patches")
        self.copy(SUSFS / "fs", WORKSPACE / "fs")
        self.copy(SUSFS / "include" / "linux", WORKSPACE / "include" / "linux")

        self.shell.patch(GKI_SUSFS)

        if self.ksu_variant == "NEXT":
            orig_cwd: Path = Path.cwd()
            os.chdir(WORKSPACE / "KernelSU-Next")
            self.shell.patch(KSU_SUSFS)
            os.chdir(orig_cwd)


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
