import requests
import shutil

from requests import Response
from pathlib import Path
from typing import Any
from src.utils.log import log


def fetch_latest(user: str, repo: str, asset: str, dest: Path) -> None:
    """
    Fetch the latest release asset from a GitHub repository.
    :param user: GitHub username or organization.
    :param repo: Repository name.
    :param asset: Name of the asset to download.
    :return: None
    """

    api: str = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    data: dict[str, Any] = requests.get(api).json()
    release_url: str | None = next(
        (a["browser_download_url"] for a in data["assets"] if asset in a["name"]),
        None,
    )

    if release_url is None:
        log(f"No asset matching {asset!r} found", "error")
        return

    resp: Response = requests.get(release_url)
    resp.raise_for_status()
    name: str = release_url.split("/")[-1]
    with open(dest, "wb") as f:
        shutil.copyfileobj(resp.raw, f)
    log(f"Downloaded {name}")
