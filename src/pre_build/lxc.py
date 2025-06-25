import requests
import subprocess
import os

from subprocess import CompletedProcess
from src.utils.shell import Shell
from src.utils.log import log
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

    def _patch(self, patch: str | Path) -> Proc:
        with open(patch, "rb") as f:
            return subprocess.run(
                ["patch", "-p1", "--forward", "--fuzz=3"], input=f.read(), check=True
            )

    def apply(self) -> Proc | None:
        if self.lxc:
            log("Downloading LXC patch")
            resp = requests.get(self.PATCH_URL)
            resp.raise_for_status()
            patch_file = Path("lxc.patch")
            patch_file.write_bytes(resp.content)
            log("Applying LXC patch")
            return self._patch(str(patch_file))
        else:
            return
