import os
import sh
import re
from pathlib import Path
from dotenv import set_key
from sh import Command, head, sed
from datetime import datetime, timezone
from kernel_builder.utils.env import susfs_enabled
from kernel_builder.config.config import OUTPUT
from kernel_builder.constants import ROOT, TOOLCHAIN, WORKSPACE
from kernel_builder.utils.build import Builder
from kernel_builder.pre_build.variants import Variants
from kernel_builder.utils.log import log


class GithubExportEnv:
    def __init__(self) -> None:
        self.builder: Builder = Builder()
        self.variants: Variants = Variants()
        self.env_file: Path = ROOT / "github.env"

    def _write_env(self, env_map: dict[str, str]) -> None:
        self.env_file.touch()
        for k, v in env_map.items():
            set_key(self.env_file, k.strip(), v.strip())

    def export_github_env(self) -> None:
        clang: Command = sh.Command(str(TOOLCHAIN / "clang" / "bin" / "clang"))
        raw_toolchain = head("-n", "1", _in=clang("-v", _err_to_out=True))
        toolchain: str = str(
            sed("s/(https..*//; s/ version//", _in=raw_toolchain)
        ).strip()

        susfs_version: str | None = (
            re.search(
                r"v\d+\.\d+\.\d+",
                (WORKSPACE / "include" / "linux" / "susfs.h").read_text(),
            ).group()  # pyright: ignore[reportOptionalMemberAccess]
            if susfs_enabled()
            else None
        )

        ksu_version: str = os.getenv("KSU_VERSION", "Unknown")

        now: datetime = datetime.now(timezone.utc)
        current_time: str = now.strftime("%a %b %d %H:%M:%S %Y")

        env_map: dict[str, str] = {
            "output": str(OUTPUT),
            "version": self.builder.get_kernel_version(),
            "variant": self.variants.suffix,
            "susfs_version": susfs_version or "Disabled",
            "ksu_version": ksu_version,
            "toolchain": toolchain,
            "build_time": current_time,
        }
        log(f"Environment map to export: {env_map}")
        self._write_env(env_map)
