import argparse 

TYPE_MAP = {
    "str":  str,
    "int":  int,
    "float": float,
    "bool": None,   
    "list": str,  
}

def build_parser(arg_config: list[dict]):
    parser = argparse.ArgumentParser(
        description="Sort files in a directory into categorised subfolders by media type."
    )
    # Positional arguments are always required and as such, are not in the config.json file
    parser.add_argument("source_dir", help="Path to the directory to scan.")
    parser.add_argument("output_dir", help="Path to the directory where sorted subfolders will be created.")

    for entry in arg_config:
        flag = entry["flag"],
        dest = entry["dest"],
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