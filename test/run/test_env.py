import os
import types
import run


def test_env_var(mocker, monkeypatch) -> None:
    fake = mocker.patch("kernel_builder.main.KernelBuilder", autospec=True)

    for var in ("KSU", "SUSFS", "LXC", "LOCAL_RUN"):
        monkeypatch.delenv(var, raising=False)

    ns = types.SimpleNamespace(command="build", ksu="NEXT", susfs=False, lxc=True)

    run.cmd_build(ns)

    fake.assert_called_once_with()
    fake.return_value.run_build.assert_called_once()

    assert os.environ["KSU"] == "NEXT"
    assert os.environ["SUSFS"] == "false"
    assert os.environ["LXC"] == "true"
    assert os.environ["LOCAL_RUN"] == "true"
