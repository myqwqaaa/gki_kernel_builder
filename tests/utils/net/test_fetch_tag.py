from types import SimpleNamespace
import pytest
from pytest_mock import MockerFixture
from pathlib import Path
from kernel_builder.utils.net import Net


def test_fetch_latest_tag_success(mocker: MockerFixture):
    fake_tags: list[dict[str, str]] = [{"name": "v3.1.4"}, {"name": "v3.1.3"}]
    mocker.patch(
        "kernel_builder.utils.net.requests.get",
        return_value=SimpleNamespace(json=lambda: fake_tags),
    )
    assert Net.fetch_latest_tag("foo", "bar") == "v3.1.4"
