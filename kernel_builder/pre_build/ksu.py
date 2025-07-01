import subprocess
import os
import requests

from subprocess import CompletedProcess
from kernel_builder.utils.log import log
from kernel_builder.utils.source import SourceManager
from typing import TypeAlias

Proc: TypeAlias = CompletedProcess[bytes]


class KSUInstaller:
    VARIANT_URLS: dict[str, str] = {
        "NEXT": "https://raw.githubusercontent.com/KernelSU-Next/KernelSU-Next/next/kernel/setup.sh",
        "SUKI": "https://raw.githubusercontent.com/SukiSU-Ultra/SukiSU-Ultra/main/kernel/setup.sh",
    }

    def __init__(self) -> None:
        self.source: SourceManager = SourceManager()
        self.variant: str = os.getenv("KSU", "NONE").upper()
        self.use_susfs: bool = os.getenv("SUSFS", "false").lower() == "true"

    def _install_ksu(self, url: str, ref: str | None) -> Proc:
        if not self.source.is_simplified(url):
            url = self.source.git_simplifier(url)

        if not ref:
            user, repo = url.split(":", 1)
            api: str = f"https://api.github.com/repos/{user}/{repo}/tags"
            data: list[dict[str, str]] = requests.get(api).json()
            ref = data[0]["name"]  # Latest tag

        setup_url = f"https://raw.githubusercontent.com/{url.split(':', 1)[1]}/{ref}/kernel/setup.sh"

        log(f"Installing KernelSU from {url} | {ref}")

        curl: Proc = subprocess.run(
            ["curl", "-LSs", setup_url], stdout=subprocess.PIPE, check=True
        )

        return subprocess.run(
            ["bash", "-s", ref],
            input=curl.stdout,
            check=True,
        )

    def install(self) -> Proc | None:
        variant: str = self.variant.upper()

        match variant:
            case "NONE":
                return
            case "NEXT":
                self._install_ksu("github.com:kernelSU-Next/kernelSU-Next", "next")
            case "SUKI":
                self._install_ksu("github.com:SukiSU-Ultra/SukiSU-Ultra", "susfs-main")
            case "RKSU":
                self._install_ksu(
                    "github.com:rsuntk/KernelSU",
                    ("staging/susfs-main" if self.use_susfs else "main"),
                )
            case _:
                return


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
