import os 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

EXTENSION_MAPPING_PATH = os.path.join(SCRIPT_DIR, 'mapping.json')
ARG_CONFIG_PATH = os.path.join(SCRIPT_DIR, 'args.json')

DEFAULT_ARG_CONFIG : dict[str, list[dict]] = {
    "run": [
        {
            "flag":    "--mapping",
            "dest":    "mapping",
            "type":    "str", 
            "default": EXTENSION_MAPPING_PATH,
            "help":    "Path to the JSON file containing extension mappings."
        },
        {
            "flag":    "--copy",
            "dest":    "copy",
            "type":    "bool",
            "default": False,
            "help":    "Copy files instead of moving them."
        },
        {
            "flag":    "--skip-duplicates",
            "dest":    "skip_duplicates",
            "type":    "bool",
            "default": False,
            "help":    "Skip files when the destination name already exists (default: keep all by renaming with a numbered suffix, e.g. file(1).txt)."
        },
        {
            "flag":    "--max-depth",
            "dest":    "max_depth",
            "type":    "int",
            "default": None,
            "help":    "Maximum directory depth to recurse into (default: unlimited)."
        },
        {
            "flag":    "--min-size",
            "dest":    "min_size",
            "type":    "int",
            "default": None,
            "help":    "Minimum file size in bytes to include (default: no limit)."
        },
        {
            "flag":    "--max-size",
            "dest":    "max_size",
            "type":    "int",
            "default": None,
            "help":    "Maximum file size in bytes to include (default: no limit)."
        },
        {
            "flag":    "--ignore-extensions",
            "dest":    "ignore_extensions",
            "type":    "list",
            "default": None,
            "help":    "File extensions to ignore, e.g. --ignore-extensions .tmp .log"
        },
        {
            "flag":    "--include-categories",
            "dest":    "include_categories",
            "type":    "list",
            "default": None,
            "help":    "Subset of categories (from mapping.json) to include, e.g. --include-categories Videos Images Audio."
        },
        {
            "flag":    "--exclude-categories",
            "dest":    "exclude_categories",
            "type":    "list",
            "default": None,
            "help":    "Subset of categories (from mapping.json) to exclude, e.g. --exclude-categories Archives Fonts."
        },
    ],
    "config": [
        {
            "flag":    "--set-default",
            "dest":    "set_default",
            "type":    "list",
            "nargs":   2,
            "metavar": ["DEST.KEY", "VALUE"],
            "default": None,
            "help":    "Update a config entry, e.g. --set-default max_depth.default 3"
        },
        {
            "flag":    "--reset",
            "dest":    "reset_config",
            "type":    "bool",
            "default": False,
            "help":    "Reset args.json to the built-in defaults."
        },
        {
            "flag":    "--list",
            "dest":    "list_config",
            "type":    "bool",
            "default": False,
            "help":    "Print all current default values and exit."
        },
    ]
}

TYPE_MAP = {
    "str":  str,
    "int":  int,
    "float": float,
    "bool": None,   
    "list": str,  
}
