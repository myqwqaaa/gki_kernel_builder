from subprocess import CompletedProcess
from kernel_builder.utils import env
from kernel_builder.config.config import PATCHES
from kernel_builder.utils.shell import Shell
from kernel_builder.utils.log import log
from typing import TypeAlias
from pathlib import Path


Proc: TypeAlias = CompletedProcess[bytes]


class LXCPatcher:
    def __init__(self) -> None:
        self.shell: Shell = Shell()
        self.lxc: bool = env.lxc_enabled()
        self.susfs: bool = env.susfs_enabled()

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


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
