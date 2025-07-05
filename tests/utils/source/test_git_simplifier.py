import pytest
from pytest_mock import MockerFixture

from kernel_builder.utils.source import SourceManager


class FakeResp:
    url = "https://github.com/torvalds/linux"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


def test_git_simplifier(mocker: MockerFixture):
    mocker.patch("kernel_builder.utils.source.requests.get", return_value=FakeResp())

    sm: SourceManager = SourceManager()
    simplified: str = sm.git_simplifier("https://github.com/torvalds/linux")
    assert simplified == "github.com:torvalds/linux"
