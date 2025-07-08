from pathlib import Path


from requests.models import Response
import requests
import tarfile
import re

from kernel_builder.config.config import TOOLCHAIN
from kernel_builder.config.manifest import AOSP_ARCHIVE, AOSP_REPO
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.net import Net


def _get_latest_aosp_clang(aosp_repo: str = AOSP_REPO) -> str:
    resp: Response = requests.get(aosp_repo)
    resp.raise_for_status()
    html: str = resp.text

    versions: list[str] = re.findall(r"clang-r(\d+)", html)
    if not versions:
        raise RuntimeError("No AOSP clang version found on the page")

    latest_num: int = max(int(v) for v in versions)

    return f"clang-r{latest_num}"


def fetch_latest_aosp_clang(aosp_archive: str = AOSP_ARCHIVE):
    latest_version: str = _get_latest_aosp_clang()
    clang_file: str = f"{latest_version}.tar.gz"
    clang_url: str = f"{aosp_archive}/{clang_file}"

    clang_path: Path = TOOLCHAIN / clang_file
    Net.stream_to_file(clang_url, clang_path)
    FileSystem.reset_path(TOOLCHAIN / "clang")
    with tarfile.open(clang_path) as archive:
        archive.extractall(TOOLCHAIN / "clang")
    clang_path.unlink()
