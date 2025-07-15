from pathlib import Path
import tarfile
from sh import aria2c, curl, awk, grep
from kernel_builder.config.config import TOOLCHAIN
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log

_USER = "bachnxuan"
_REPO = "aosp_clang_mirror"


def fetch_latest_aosp_clang(
    dest: Path = TOOLCHAIN,
) -> None:
    api_url: str = f"https://github.com/{_USER}/{_REPO}/releases/latest"
    latest_tag: str = str(
        awk(
            "-F/",
            "{print $NF}",
            _in=grep(
                "-i",
                "^Location:",
                _in=curl("-fsSLI", "--retry", "5", "--retry-connrefused", api_url),
            ),
        )
    ).strip()
    latest_clang: str = (
        f"{latest_tag.removesuffix(f'-{latest_tag.split("-")[-1]}')}.tar.gz"
    )

    release_url: str = f"https://github.com/bachnxuan/aosp_clang_mirror/releases/download/{latest_tag}/{latest_clang}"

    log(f"Clang release url: {release_url}")

    filename: str = Path(release_url).name
    download_path: Path = dest / filename

    aria2c(
        "-x16",
        "-s32",
        "-k8M",
        "--file-allocation=falloc",
        "--timeout=60",
        "--retry-wait=5",
        "-d",
        str(dest),
        "-o",
        filename,
        release_url,
    )

    out_dir: Path = dest / "clang"
    FileSystem.reset_path(out_dir)
    with tarfile.open(download_path) as archive:
        archive.extractall(out_dir)

    download_path.unlink()
    log(f"Installed clang to {out_dir}")
