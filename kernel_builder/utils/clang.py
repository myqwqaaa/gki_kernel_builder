from pathlib import Path
import json
import tarfile
from kernel_builder.config.config import TOOLCHAIN
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log
from typing import Any
from kernel_builder.utils.command import authorized_curl, aria2c


def fetch_latest_aosp_clang(
    user: str = "bachnxuan",
    repo: str = "aosp_clang_mirror",
    dest: Path = TOOLCHAIN,
) -> None:
    api_url: str = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    raw: str = authorized_curl(api_url)

    data: dict[str, Any] = json.loads(raw)

    release_url: str | None = next(
        (
            asset["browser_download_url"]
            for asset in data.get("assets", [])
            if asset.get("browser_download_url", "").endswith(".tar.gz")
        ),
        None,
    )

    if release_url is None:
        log(f"No .tar.gz asset found for {user}/{repo}", "error")
        return

    log(f"Clang release url: {release_url}")

    filename: str = Path(release_url).name
    download_path: Path = dest / filename

    aria2c("-d", str(dest), "-o", filename, release_url)

    out_dir: Path = dest / "clang"
    FileSystem.reset_path(out_dir)
    with tarfile.open(download_path) as archive:
        archive.extractall(out_dir)

    download_path.unlink()
    log(f"Installed clang to {out_dir}")
