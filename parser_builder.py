import argparse 
from constants import TYPE_MAP 

def _add_entry_to_parser(parser, entry: dict):
    """Add a single config entry to an ArgumentParser"""
    flag      = entry["flag"]
    dest      = entry["dest"]
    data_type = entry.get("type", "str")
    default   = entry.get("default")
    help_msg  = entry.get("help", "")

    if data_type == "bool":
        # BooleanOptionalAction provides both --flag and --no-flag, allowing users
        # to override a saved default either way.
        parser.add_argument(
            flag,
            dest=dest,
            action=argparse.BooleanOptionalAction,
            default=default,
            help=help_msg,
        )
    elif data_type == "list":
        nargs   = entry.get("nargs", "*")
        metavar = entry.get("metavar")
        kwargs  = dict(dest=dest, nargs=nargs, default=default, help=help_msg)
        if metavar is not None:
            kwargs["metavar"] = metavar
        parser.add_argument(flag, **kwargs)
    else:
        parser.add_argument(flag, dest=dest, type=TYPE_MAP[data_type], default=default, help=help_msg)

def build_run_parser(subparsers, arg_config: dict):
    run_parser = subparsers.add_parser(
        "run",
        help="Sort files from a source directory into categorised subfolders."
    )

    # Required positional arguments for running the program
    run_parser.add_argument("source_dir", help="Path to the directory to scan.")
    run_parser.add_argument("output_dir", help="Path to the directory where sorted subfolders will be created.")

    for entry in arg_config["run"]:
        _add_entry_to_parser(run_parser, entry)

    return run_parser


def build_config_parser(subparsers, arg_config: dict):
    config_parser = subparsers.add_parser(
        "config",
        help="View or modify the default configuration stored in args.json."
    )

    for entry in arg_config["config"]:
        _add_entry_to_parser(config_parser, entry)

    return config_parser


def build_parser(arg_config: dict) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Sort files into categorised subfolders by media type."
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # Adding the run and config subparsers
    build_run_parser(subparsers, arg_config)
    build_config_parser(subparsers, arg_config)

    return parser
