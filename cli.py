#!/usr/bin/env python3
# encoding: utf-8

from typer.main import Typer
from typer import Option
from pathlib import Path
from typing import Annotated
from kernel_builder.utils.log import configure_log
from kernel_builder.config.config import LOGFILE
from kernel_builder.constants import WORKSPACE, TOOLCHAIN, ROOT, OUTPUT
from kernel_builder.kernel_builder import KernelBuilder
import shutil
import typer
import dotenv
import os
import sh

app: Typer = typer.Typer(help="GKI Kernel Builder CLI", pretty_exceptions_enable=False)


def _bool_env(var: str, default: bool = False) -> bool:
    return os.getenv(var, str(default)).lower() in ("true", "1", "yes")


@app.command()
def build(
    ksu: Annotated[
        str,
        Option(
            "--ksu",
            "-k",
            envvar="KSU",
            help="KernelSU variant",
        ),
    ] = "NONE",
    susfs: Annotated[
        bool,
        Option(
            "--susfs/--no-susfs",
            "-s",
            help="Enable SUSFS support",
        ),
    ] = _bool_env("SUSFS"),
    lxc: Annotated[
        bool,
        Option(
            "--lxc/--no-lxc",
            "-l",
            help="Enable or disable LXC",
        ),
    ] = _bool_env("LXC"),
    verbose: Annotated[
        bool,
        Option(
            "--verbose/--no-verbose",
            "-v",
            help="Verbose output",
        ),
    ] = _bool_env("VERBOSE_OUTPUT"),
) -> None:
    if ksu == "NONE" and susfs:
        typer.secho("[ERROR] SUSFS requires KernelSU", err=True, fg=typer.colors.RED)
        raise typer.Exit(1)

    if os.getenv("GITHUB_ACTIONS") != "true":
        dotenv.load_dotenv()

    typer.echo(message=f"Start Build: {ksu=}, {susfs=}, {lxc=}, {verbose=}")

    configure_log(logfile=LOGFILE)
    if verbose:
        sh.Command._call_args["_tee"] = True

    os.environ.update(
        KSU=str(ksu),
        SUSFS=str(susfs).lower(),
        LXC=str(lxc).lower(),
        VERBOSE_OUTPUT=str(verbose).lower(),
    )

    KernelBuilder().run_build()


@app.command()
def clean(
    all: Annotated[
        bool,
        typer.Option(
            "--all/--no-all",
            "-a",
            help="Also delete dist/ (output) directory",
        ),
    ] = False,
) -> None:
    targets: list[Path] = [WORKSPACE, TOOLCHAIN]

    if all:
        targets.append(OUTPUT)
    for folder in targets:
        shutil.rmtree(folder, ignore_errors=True)

    (ROOT / "github.env").unlink(missing_ok=True)

    typer.echo("Cleanup completed")


if __name__ == "__main__":
    app()
