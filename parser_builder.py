import argparse 

TYPE_MAP = {
    "str":  str,
    "int":  int,
    "float": float,
    "bool": None,   
    "list": str,  
}

def parse_arguments (arg_config: list[dict]):
    for entry in arg_config:
        flag      = entry["flag"]
        dest      = entry["dest"]
        data_type = entry.get("type", "str")
        default   = entry.get("default")
        help_msg  = entry.get("help", "")

        if data_type == "bool":
            run_parser.add_argument(flag, dest=dest, action="store_true", default=default, help=help_msg)
        elif data_type == "list":
            run_parser.add_argument(flag, dest=dest, nargs="*", default=default, help=help_msg)
        else:
            run_parser.add_argument(flag, dest=dest, type=TYPE_MAP[data_type], default=default, help=help_msg)

    return run_parser

def build_run_parser(subparsers: argparse.ArgumentParser, arg_config: list[dict]):
    """Subparser for the file-sorting operation."""
    run_parser = subparsers.add_subparsers(
        "run",
        help="Sort files in a directory into categorised subfolders by media type."
    )
    # Positional arguments are always required and as such, are not in the config.json file
    run_parser.add_argument("source_dir", help="Path to the directory to scan.")
    run_parser.add_argument("output_dir", help="Path to the directory where sorted subfolders will be created.",)

def build_parser(arg_config: list[dict]):
    parser = argparse.ArgumentParser(
        description="Sort files in a directory into categorised subfolders by media type."
    )
    # Positional arguments are always required and as such, are not in the config.json file
    parser.add_argument("source_dir", help="Path to the directory to scan.")
    parser.add_argument("output_dir", help="Path to the directory where sorted subfolders will be created.",)

    # Config management options used by main.py
    parser.add_argument(
        "--reset-config",
        dest="reset_config",
        action="store_true",
        default=False,
        help="Reset args.json to defaults and exit.",
    )
    parser.add_argument(
        "--set-default",
        dest="set_default",
        nargs=2,
        default=None,
        metavar=("DEST.KEY", "VALUE"),
        help="Update args.json: set a config entry field (e.g. max_depth.default 2) and exit.",
    )

    for entry in arg_config:
        flag = entry["flag"]
        dest = entry["dest"]
        data_type = entry.get("type", "str")
        default = entry.get("default")
        help_msg = entry.get("help", "")

        if data_type == "bool":
            parser.add_argument(flag, dest=dest, action="store_true", default=default, help=help_msg)
        elif data_type == "list":
            parser.add_argument(flag, dest=dest, nargs="*", default=default, help=help_msg)
        else:
            parser.add_argument(flag, dest=dest, type=TYPE_MAP[data_type], default=default, help=help_msg)
    return parser
