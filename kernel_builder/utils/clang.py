import json
from typing import Any, Final
from kernel_builder.utils.command import authorized_curl, curl
from sh import sed, tail, sort, grep

# Toolchain Repo
SLIM_TOOLCHAIN_URL: Final[str] = "https://www.kernel.org/pub/tools/llvm/files/"
AOSP_TOOLCHAIN_URL: Final[str] = (
    "https://api.github.com/repos/bachnxuan/aosp_clang_mirror/releases/latest"
)
RV_TOOLCHAIN_URL: Final[str] = (
    "https://api.github.com/repos/Rv-Project/RvClang/releases/latest"
)
YUKI_TOOLCHAIN_URL: Final[str] = (
    "https://api.github.com/repos/Klozz/Yuki_clang_releases/releases/latest"
)
LILIUM_TOOLCHAIN_URL: Final[str] = (
    "https://api.github.com/repos/liliumproject/clang/releases/latest"
)
TNF_TOOLCHAIN_URL: Final[str] = (
    "https://api.github.com/repos/topnotchfreaks/clang/releases/latest"
)
NEUTRON_TOOLCHAIN_URL: Final[str] = (
    "https://api.github.com/repos/Neutron-Toolchains/clang-build-catalogue/releases/latest"
)


def _fetch_latest_github_release(repo_api: str) -> str:
    raw: str = authorized_curl(repo_api)
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
        raise Exception()

    return release_url


def fetch_clang(variants: str) -> str:
    match variants.upper():
        case "SLIM":
            return str(
                sed(
                    f"s|^|{SLIM_TOOLCHAIN_URL}|",
                    _in=tail(
                        "-n1",
                        _in=sort(
                            "-V",
                            _in=grep(
                                "-oP",
                                r"llvm-[\d.]+-x86_64\.tar\.xz",
                                _in=curl(SLIM_TOOLCHAIN_URL),
                            ),
                        ),
                    ),
                )
            ).strip()
        case "AOSP":
            return _fetch_latest_github_release(AOSP_TOOLCHAIN_URL)
        case "RV":
            return _fetch_latest_github_release(RV_TOOLCHAIN_URL)
        case "YUKI":
            return _fetch_latest_github_release(YUKI_TOOLCHAIN_URL)
        case "LILIUM":
            return _fetch_latest_github_release(LILIUM_TOOLCHAIN_URL)
        case "TNF":
            return _fetch_latest_github_release(TNF_TOOLCHAIN_URL)
        case "NEUTRON":
            return _fetch_latest_github_release(NEUTRON_TOOLCHAIN_URL)
        case _:
            raise Exception("Unknown clang variant")
