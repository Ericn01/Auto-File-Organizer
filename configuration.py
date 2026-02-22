import os 
import json 
from default_argconfig import DEFAULT_ARG_CONFIG


ARG_CONFIG_PATH = "./args.json"

def load_arg_config(filepath: str = ARG_CONFIG_PATH) -> list[dict]:
    """Load argument config from JSON, writing defaults if the file doesn't exist."""
    if not os.path.exists(filepath):
        print(f"No config file found at '{filepath}'. Creating default config.")
        save_arg_config(DEFAULT_ARG_CONFIG, filepath)
        return DEFAULT_ARG_CONFIG

    try:
        with open(filepath, 'r') as f:
            config_data = json.load(f)
        print(f"Loaded argument config from '{filepath}'.")
        return config_data
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode '{filepath}': {e}. Falling back to defaults.")
        return DEFAULT_ARG_CONFIG
    


def save_arg_config(config: list[dict], filepath: str = ARG_CONFIG_PATH) -> None:
    """Persist the argument config list to JSON."""
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Argument config saved to '{filepath}'.")


def update_arg_config(dest: str, key: str, value, filepath: str = ARG_CONFIG_PATH) -> None:
    """
    Update a single field of one argument entry and save.

    Args:
        dest:  The 'dest' value identifying the argument (e.g. 'max_depth').
        key:   The field to update (e.g. 'default', 'help').
        value: The new value.
    """
    config = load_arg_config(filepath)
    matched = False
    for entry in config:
        if entry.get("dest") == dest:
            entry[key] = value
            matched = True
            break
    if not matched:
        raise KeyError(f"No argument with dest='{dest}' found in config.")
    save_arg_config(config, filepath)
    print(f"Updated '{dest}.{key}' → {value!r}")