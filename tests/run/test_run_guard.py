import pytest
import types
import run
from types import SimpleNamespace
from pytest_mock.plugin import MockType
from pytest_mock import MockerFixture


@pytest.mark.parametrize(
    "ksu, susfs, expect_exit",
    [
        ("NEXT", True, False),
        ("SUKI", True, False),
        ("NONE", True, True),
    ],
)
def test_build_guard(mocker: MockerFixture, ksu, susfs, expect_exit) -> None:
    fake: MockType = mocker.patch(
        "kernel_builder.kernel_builder.KernelBuilder", autospec=True
    )
    ns: SimpleNamespace = types.SimpleNamespace(
        command="build", ksu=ksu, susfs=susfs, lxc=False, verbose=False
    )

    if expect_exit:
        with pytest.raises(SystemExit):
            run.cmd_build(ns)
    else:
        run.cmd_build(ns)
