from argparse import ArgumentParser, Namespace, BooleanOptionalAction
import argparse
import os
from pathlib import Path
import shutil
from kernel_builder.utils.log import log


def build_parser() -> ArgumentParser:
    parser: ArgumentParser = argparse.ArgumentParser(description="Kernel Builder")
    sub = parser.add_subparsers(dest="command", required=True)

    # Build
    build = sub.add_parser(
        "build",
        help="Compile a kernel image",
        usage="%(prog)s build [-k {NONE,NEXT,SUKI,RKSU}] [-s/--susfs] [-l/--lxc]",
    )
    build.add_argument(
        "-k",
        "--ksu",
        choices=["NONE", "NEXT", "SUKI", "RKSU"],
        default="NONE",
        help="KernelSU variant (default: %(default)s)",
    )
    build.add_argument(
        "-s",
        "--susfs",
        help="Enable SUSFS support",
        action=BooleanOptionalAction,
        default=False,
    )
    build.add_argument(
        "-l",
        "--lxc",
        help="Enable LXC support",
        action=BooleanOptionalAction,
        default=False,
    )

    # Clean
    clean: ArgumentParser = sub.add_parser("clean", help="Remove build artefacts")
    clean.add_argument(
        "-a",
        "--all",
        action=BooleanOptionalAction,
        default=False,
        help="Also delete dist/ (out) directory",
    )

    return parser


def cmd_build(args: Namespace) -> None:
    if args.ksu == "NONE" and args.susfs:
        raise SystemExit("SUSFS requires KernelSU ≠ NONE")

    os.environ["KSU"] = args.ksu
    os.environ["SUSFS"] = str(args.susfs).lower()
    os.environ["LXC"] = str(args.lxc).lower()
    os.environ["LOCAL_RUN"] = "true"

    from kernel_builder.main import KernelBuilder

    KernelBuilder().run_build()


def cmd_clean(args: Namespace) -> None:
    from kernel_builder.config.config import OUTPUT, WORKSPACE, TOOLCHAIN

    build_folder: list[Path] = [WORKSPACE, TOOLCHAIN]

    if args.all:
        build_folder.append(OUTPUT)
    for folder in build_folder:
        shutil.rmtree(folder, ignore_errors=True)


def main():
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()

    match args.command:
        case "build":
            cmd_build(args)
        case "clean":
            cmd_clean(args)
        case _:
            parser.error("Unknown command")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        log(str(err), "error")
