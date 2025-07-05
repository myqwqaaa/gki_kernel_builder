import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest
from pytest_mock import MockerFixture

from kernel_builder.utils.shell import Shell


@pytest.fixture
def dummy_patch(tmp_path: Path) -> Path:
    p: Path = tmp_path / "fix.patch"
    p.write_text("--- a/README.md\n+++ b/README.md\n@@\n-old line\n+new line\n")
    return p


def test_patch_success(mocker: MockerFixture, dummy_patch: Path):
    fake_proc = SimpleNamespace(returncode=0, stdout=b"", stderr=b"")
    spy_run = mocker.patch(
        "kernel_builder.utils.shell.subprocess.run",
        autospec=True,
        return_value=fake_proc,
    )

    result = Shell().patch(dummy_patch)

    spy_run.assert_called_once()
    cmd, kwargs = spy_run.call_args

    assert cmd[0] == ["patch", "-p1", "--forward", "--fuzz=3"]
    assert kwargs["check"] is True
    assert kwargs["input"] == dummy_patch.read_bytes()
    assert result is fake_proc


def test_patch_failure(mocker: MockerFixture, dummy_patch: Path):
    err = subprocess.CalledProcessError(1, ["patch"])
    mocker.patch(
        "kernel_builder.utils.shell.subprocess.run",
        autospec=True,
        side_effect=err,
    )

    with pytest.raises(subprocess.CalledProcessError) as exc:
        Shell().patch(dummy_patch)

    assert exc.value is err
