from kernel_builder.utils import env
from kernel_builder.config.config import PATCHES
from kernel_builder.utils.tool import patch
from kernel_builder.utils.log import log
from pathlib import Path


class LXCPatcher:
    def __init__(self) -> None:
        self.lxc: bool = env.lxc_enabled()

    def apply(self) -> None:
        LXC: Path = PATCHES / "lxc.patch"
        if self.lxc:
            log("Applying LXC Patches")
            patch(LXC)
        else:
            return


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
