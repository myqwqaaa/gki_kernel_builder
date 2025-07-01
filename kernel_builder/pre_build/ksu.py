import subprocess
import os

from subprocess import CompletedProcess
from kernel_builder.utils.log import log
from typing import TypeAlias

Proc: TypeAlias = CompletedProcess[bytes]


class KSUInstaller:
    VARIANT_URLS: dict[str, str] = {
        "NEXT": "https://raw.githubusercontent.com/KernelSU-Next/KernelSU-Next/next/kernel/setup.sh",
        "SUKI": "https://raw.githubusercontent.com/SukiSU-Ultra/SukiSU-Ultra/main/kernel/setup.sh",
    }

    def __init__(self) -> None:
        self.variant: str = os.getenv("KSU", "NONE").upper()

    def install(self) -> Proc | None:
        variant: str = self.variant.upper()
        if variant == "NONE":
            return None

        url: str | None = self.VARIANT_URLS.get(variant)
        if not url:
            log(f"Unknown KernelSU variant {variant!r}", "error")
            return None

        log(f"Installing KernelSU variant: {variant}")
        curl: Proc = subprocess.run(
            ["curl", "-LSs", url], stdout=subprocess.PIPE, check=True
        )

        return subprocess.run(
            ["bash", "-s", "next" if variant == "NEXT" else "susfs-main"],
            input=curl.stdout,
            check=True,
        )


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
