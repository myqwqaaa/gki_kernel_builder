from typing import override
from kernel_builder.interface.patcher import PatcherInterface
from kernel_builder.utils import env
from kernel_builder.config.config import PATCHES
from kernel_builder.utils.command import apply_patch
from kernel_builder.utils.log import log
from pathlib import Path


class LXCPatcher(PatcherInterface):
    def __init__(self) -> None:
        self.lxc: bool = env.lxc_enabled()

    @override
    def apply(self) -> None:
        LXC: Path = PATCHES / "lxc.patch"
        if self.lxc:
            log("Applying LXC Patches")
            apply_patch(LXC)
        else:
            return


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
