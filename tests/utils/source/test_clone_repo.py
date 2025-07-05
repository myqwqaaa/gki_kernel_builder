from pathlib import Path
import pytest
from pytest_mock import MockerFixture
from kernel_builder.utils.source import SourceManager


def test_clone_repo_args(mocker: MockerFixture, tmp_path: Path):
    fake_proc = object()
    spy_run = mocker.patch(
        "kernel_builder.utils.source.Shell.run",
        return_value=fake_proc,
        autospec=True,
    )
    sm = SourceManager()
    repo = {
        "url": "github.com:foo/bar",
        "branch": "dev",
        "to": str(tmp_path / "bar"),
    }

    result = sm.clone_repo(repo, depth=3, args=["--filter=blob:none"])
    assert result is fake_proc

    spy_run.assert_called_once()
    cmd = spy_run.call_args.args[1]
    assert cmd[:5] == ["git", "clone", "--depth", "3", "-b"]
    assert "--filter=blob:none" in cmd
    assert cmd[-2:] == ["https://github.com/foo/bar", repo["to"]]
