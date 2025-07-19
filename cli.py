#!/usr/bin/env python3
# encoding: utf-8

from typer.main import Typer
from typer import Option
from pathlib import Path
from typing import Annotated
import importlib
import shutil
import typer
import os

app: Typer = typer.Typer(help="GKI Kernel Builder CLI")


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

    typer.echo(message=f"Start Build: {ksu=}, {susfs=}, {lxc=}, {verbose=}")

    os.environ.update(
        KSU=str(ksu),
        SUSFS=str(susfs).lower(),
        LXC=str(lxc).lower(),
        VERBOSE_OUTPUT=str(verbose).lower(),
    )

    KernelBuilder = importlib.import_module(
        "kernel_builder.kernel_builder"
    ).KernelBuilder
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
    from kernel_builder.config.config import OUTPUT
    from kernel_builder.constants import WORKSPACE, TOOLCHAIN, ROOT

    targets: list[Path] = [WORKSPACE, TOOLCHAIN]

    if all:
        targets.append(OUTPUT)
    for folder in targets:
        shutil.rmtree(folder, ignore_errors=True)

    (ROOT / "github.env").unlink(missing_ok=True)

    typer.echo("Cleanup completed")


if __name__ == "__main__":
    app()
