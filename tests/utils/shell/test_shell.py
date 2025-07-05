from pytest_mock.plugin import MockType


from pytest_mock.plugin import MockType


from pytest_mock.plugin import MockType


from pytest_mock.plugin import MockType
import os
import sys
import pytest
from pytest_mock import MockerFixture
from types import SimpleNamespace
from kernel_builder.utils.shell import Proc, Shell
import subprocess
import importlib


def test_shell_run_success(mocker: MockerFixture):
    fake_proc: SimpleNamespace = SimpleNamespace(returncode=0, stdout=b"ok", stderr=b"")
    spy_sub: MockType = mocker.patch(
        "kernel_builder.utils.shell.subprocess.run",
        return_value=fake_proc,
        autospec=True,
    )

    spy_log: MockType = mocker.spy(
        importlib.import_module("kernel_builder.utils.shell"), "log"
    )

    cmd: list[str] = [sys.executable, "-c", "print('hi')"]
    result: Proc = Shell().run(cmd)

    spy_sub.assert_called_once_with(cmd, check=True, env=os.environ)

    logged = spy_log.call_args[0][0]
    assert logged.startswith("Running command ")
    assert " ".join(cmd) in logged

    assert result is fake_proc


def test_run_failure(mocker: MockerFixture):
    err = subprocess.CalledProcessError(1, ["false"], stderr=b"boom")
    mocker.patch(
        "kernel_builder.utils.shell.subprocess.run", side_effect=err, autospec=True
    )

    with pytest.raises(subprocess.CalledProcessError) as exc:
        Shell().run(["false"])

    assert exc.value is err
