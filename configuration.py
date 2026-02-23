import os 
import json 
from copy import deepcopy
from constants import DEFAULT_ARG_CONFIG, ARG_CONFIG_PATH

def _merge_missing_defaults(current: object, defaults: dict[str, list[dict]]) -> tuple[dict[str, list[dict]], bool]:
    """
    Merge any missing default arguments into an existing args.json structure.

    This allows the project to add new CLI options while preserving a user's
    existing customized entries.
    """
    if not isinstance(current, dict):
        return deepcopy(defaults), True

    merged: dict[str, list[dict]] = dict(current)  # shallow copy of sections
    changed = False

    for section, default_entries in defaults.items():
        section_entries = merged.get(section)
        if not isinstance(section_entries, list):
            merged[section] = deepcopy(default_entries)
            changed = True
            continue

        existing_dests = {
            entry.get("dest")
            for entry in section_entries
            if isinstance(entry, dict) and entry.get("dest")
        }

        for default_entry in default_entries:
            dest = default_entry.get("dest")
            if not dest or dest in existing_dests:
                continue
            section_entries.append(deepcopy(default_entry))
            existing_dests.add(dest)
            changed = True

    return merged, changed

def load_arg_config(filepath: str = ARG_CONFIG_PATH) -> dict[str, list[dict]]:
    """Load argument config from JSON, writing defaults if the file doesn't exist."""
    if not os.path.exists(filepath):
        print(f"No config file found at '{filepath}'. Creating default config.")
        save_arg_config(DEFAULT_ARG_CONFIG, filepath)
        return DEFAULT_ARG_CONFIG

    try:
        with open(filepath, 'r') as f:
            config_data = json.load(f)
        merged, changed = _merge_missing_defaults(config_data, DEFAULT_ARG_CONFIG)
        if changed:
            save_arg_config(merged, filepath)
            print(f"Loaded argument config from '{filepath}' (updated with new defaults).")
        else:
            print(f"Loaded argument config from '{filepath}'.")
        return merged
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode '{filepath}': {e}. Falling back to defaults.")
        return DEFAULT_ARG_CONFIG
    


def save_arg_config(config: dict[str, list[dict]] , 
                    filepath: str = ARG_CONFIG_PATH) -> None:
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
    for group in config.values():
        for entry in group:
            if entry.get("dest") == dest:
                entry[key] = value
                matched = True
                break
        if matched:
            break
    if not matched:
        raise KeyError(f"No argument with dest='{dest}' found in config.")
    save_arg_config(config, filepath)
    print(f"Updated '{dest}.{key}' → {value!r}")
