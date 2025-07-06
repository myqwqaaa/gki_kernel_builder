from types import SimpleNamespace
import pytest
from pytest_mock import MockerFixture
from pathlib import Path
from kernel_builder.utils.net import Net
from typing import Self


class FakeResp:
    def __init__(self, data: bytes) -> None:
        self._data: bytes = data

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, tb) -> None:
        pass

    def raise_for_status(self) -> None:
        pass

    def iter_content(self, chunk_size):
        yield self._data


def test_stream_to_file(tmp_path: Path, mocker: MockerFixture) -> None:
    body = b"hello world"
    mocker.patch(
        "kernel_builder.utils.net.requests.get",
        return_value=FakeResp(body),
    )

    dest: Path = tmp_path / "file.bin"
    net: Net = Net()
    net.stream_to_file("https://example.com/file", dest)

    assert dest.read_bytes() == body


def test_fetch_latest_tag_success(mocker: MockerFixture):
    fake_tags: list[dict[str, str]] = [{"name": "v3.1.4"}, {"name": "v3.1.3"}]
    mocker.patch(
        "kernel_builder.utils.net.requests.get",
        return_value=SimpleNamespace(json=lambda: fake_tags),
    )
    assert Net.fetch_latest_tag("foo", "bar") == "v3.1.4"
