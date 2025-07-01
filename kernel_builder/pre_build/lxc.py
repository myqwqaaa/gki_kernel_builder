import os

from subprocess import CompletedProcess
from kernel_builder.config.config import PATCHES
from kernel_builder.utils.shell import Shell
from kernel_builder.utils.log import log
from typing import Final, TypeAlias
from pathlib import Path


Proc: TypeAlias = CompletedProcess[bytes]


class LXCPatcher:
    PATCH_URL: Final[str] = (
        "https://raw.githubusercontent.com/bachnxuan/kernel_patches/refs/heads/master/lxc_support.patch"
    )

    def __init__(self) -> None:
        self.shell: Shell = Shell()
        self.lxc: bool = os.getenv("LXC", "false").lower() == "true"
        self.susfs: bool = os.getenv("SUSFS", "false").lower() == "true"

    def apply(self) -> Proc | None:
        LXC: Path = PATCHES / "lxc.patch"
        LXC_SUSFS: Path = PATCHES / "lxc_susfs.patch"
        if self.lxc:
            log("Applying LXC Patches")
            if self.susfs:
                return self.shell.patch(str(LXC_SUSFS))
            return self.shell.patch(str(LXC))
        else:
            return
