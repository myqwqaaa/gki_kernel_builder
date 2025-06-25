import requests
import shutil
import gzip
import subprocess

from typing import ClassVar
from pathlib import Path
from src.utils.fs import FileSystem
from src.utils.log import log
from src.config.config import WORKSPACE
from src.utils.shell import Shell


class KPMPatcher:
    image_path: ClassVar[Path] = (
        WORKSPACE / "out" / "arch" / "arm64" / "boot" / "Image.gz"
    )

    def __init__(self) -> None:
        self.shell: Shell = Shell()
        self.fs: FileSystem = FileSystem()

    def fetch(self, url: str, dest: Path) -> None:
        log(f"Fetching {url} to {dest}")
        with (
            requests.get(url, stream=True, allow_redirects=True) as resp,
            dest.open("wb") as fdest,
        ):
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=8_192):
                if chunk:
                    fdest.write(chunk)
        log(f"Saved {url} to {dest}")

    def patch(self) -> None:
        cwd: Path = Path.cwd()
        temp: Path = cwd / "temp"
        self.fs.reset_path(temp)
        log("Patching KPM")
        try:
            self.fs.cd(temp)

            assets: dict[str, str] = {
                "kpimg": "https://github.com/SukiSU-Ultra/SukiSU_KernelPatch_patch/raw/refs/heads/main/patch/res/kpimg",
                "kptools": "https://github.com/SukiSU-Ultra/SukiSU_KernelPatch_patch/raw/refs/heads/main/patch/res/kptools-linux",
            }

            for name, url in assets.items():
                dest: Path = temp / name
                self.fetch(url, dest)
                dest.chmod(0o755)

            gz_in: Path = temp / "Image.gz"
            img: Path = temp / "Image"
            shutil.move(self.image_path, gz_in)
            with gzip.open(gz_in, "rb") as fsrc, img.open("wb") as fdst:
                shutil.copyfileobj(fsrc, fdst)

            subprocess.run(
                [
                    str(temp / "kptools"),
                    "-p",
                    "-s",
                    "123",
                    "-i",
                    "Image",
                    "-k",
                    str(temp / "kpimg"),
                    "-o",
                    "oImage",
                ],
                cwd=str(temp),
                check=True,
            )

            patched: Path = temp / "oImage"
            if not patched.exists():
                log(f"Patched image not found at {patched}", "error")
                return

            gz_in.unlink(missing_ok=True)
            img.unlink(missing_ok=True)

            shutil.move(patched, img)
            with img.open("rb") as src, gzip.open(gz_in, "wb") as dst:
                shutil.copyfileobj(src, dst)

            shutil.move(gz_in, self.image_path)
            log("KPM patch applied successfully")

        except Exception as e:
            log(f"Error during patching: {e}", "error")
            return

        finally:
            self.fs.cd(cwd)
