import os
import subprocess
from sh import jq
from kernel_builder.config.config import WORKSPACE
from kernel_builder.utils.log import log
from kernel_builder.utils.source import SourceManager
from kernel_builder.utils import env
from kernel_builder.utils.command import authorized_curl


class KSUInstaller:
    VARIANT_URLS: dict[str, str] = {
        "NEXT": "https://raw.githubusercontent.com/KernelSU-Next/KernelSU-Next/next/kernel/setup.sh",
        "SUKI": "https://raw.githubusercontent.com/SukiSU-Ultra/SukiSU-Ultra/main/kernel/setup.sh",
    }

    def __init__(self) -> None:
        self.source: SourceManager = SourceManager()
        self.variant: str = env.ksu_variant()
        self.use_susfs: bool = env.susfs_enabled()

    def _install_ksu(self, url: str, ref: str | None) -> None:
        if not self.source.is_simplified(url):
            url = self.source.git_simplifier(url)

        if not ref:
            user, repo = url.split(":", 1)

            ref = str(
                jq(
                    "-r",
                    ".tag_name",
                    _in=authorized_curl(
                        f"https://api.github.com/repos/{user}/{repo}/releases/latest"
                    ),
                )
            ).strip()

        os.environ["KSU_VERSION"] = ref
        setup_url = f"https://raw.githubusercontent.com/{url.split(':', 1)[1]}/{ref}/kernel/setup.sh"

        log(f"Installing KernelSU from {url} | {ref}")

        # Temporary fix
        script: str = subprocess.run(
            ["curl", "-LSs", setup_url],
            capture_output=True,
            check=True,
            text=True,
        ).stdout

        subprocess.run(
            ["bash", "-s", ref],
            input=script,
            cwd=str(WORKSPACE),
            check=True,
            text=True,
        )

    def install(self) -> None:
        variant: str = self.variant.upper()

        match variant:
            case "NONE":
                return
            case "NEXT":
                self._install_ksu("github.com:kernelSU-Next/kernelSU-Next", "next")
            case "SUKI":
                if self.use_susfs:
                    self._install_ksu(
                        "github.com:SukiSU-Ultra/SukiSU-Ultra", "susfs-main"
                    )
                else:
                    self._install_ksu("github.com:SukiSU-Ultra/SukiSU-Ultra", "nongki")
            case _:
                return


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
