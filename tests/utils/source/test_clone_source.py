from pytest_mock.plugin import MockType
import types
from pathlib import Path
import importlib
import pytest
from pytest_mock import MockerFixture
from kernel_builder.utils.source import SourceManager


def test_clone_sources_logs_and_calls(mocker: MockerFixture):
    mocker.patch("kernel_builder.utils.source.Shell.run", autospec=True)

    spy_clone: MockType = mocker.spy(SourceManager, "clone_repo")
    spy_log: MockType = mocker.spy(
        importlib.import_module("kernel_builder.utils.source"), "log"
    )

    sm: SourceManager = SourceManager(
        sources=[
            {
                "url": "github.com:foo/bar",
                "branch": "main",
                "to": "bar",
            }
        ]
    )
    sm.clone_sources()

    spy_clone.assert_called_once()
    assert (
        "Cloning github.com:foo/bar into bar on branch main" in spy_log.call_args[0][0]
    )
