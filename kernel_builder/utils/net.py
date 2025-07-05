import requests

from collections.abc import Iterator
from pathlib import Path
from kernel_builder.utils.log import log


class Net:
    @staticmethod
    def stream_to_file(url: str, dest: Path) -> None:
        log(f"Fetching {url} to {dest}")
        with (
            requests.get(url, stream=True, allow_redirects=True) as resp,
            dest.open("wb") as fdest,
        ):
            resp.raise_for_status()
            chunks: Iterator[bytes] = resp.iter_content(chunk_size=8_192)
            for chunk in chunks:
                if chunk:
                    fdest.write(chunk)
        log(f"Saved {url} to {dest}")

    @staticmethod
    def fetch_latest_tag(user: str, repo: str) -> str:
        api: str = f"https://api.github.com/repos/{user}/{repo}/tags"
        data: list[dict[str, str]] = requests.get(api).json()
        return data[0]["name"]
