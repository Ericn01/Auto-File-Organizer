'''
Main script
'''
import json 
import os 
import shutil

def read_json (filepath : str):
    try: 
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data 
    except FileNotFoundError:
        print(f"Error: The file {filepath} could not be found!")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON: {e}")











def main():
    arg_config = read_json()
    parser = build_parser(arg_config)
    args = parser.parse_args()

    # --- Config management commands (exit early, no file sorting needed) --- #

    if args.reset_config:
        # save_arg_config(DEFAULT_ARG_CONFIG)
        print("Config reset to defaults.")
        return

    if args.set_default:
        raw_dest_key, raw_value = args.set_default
        if '.' not in raw_dest_key:
            print("Error: --set-default expects DEST.KEY format, e.g. max_depth.default")
            return
        dest, key = raw_dest_key.split('.', 1)

        # Try to coerce the value to the right type based on the config entry
        coerced_value = raw_value
        for entry in arg_config:
            if entry.get("dest") == dest:
                data_type = entry.get("type", "str")
                if data_type == "int":
                    coerced_value = int(raw_value)
                elif data_type == "float":
                    coerced_value = float(raw_value)
                elif data_type == "bool":
                    coerced_value = raw_value.lower() in ("true", "1", "yes")
                elif data_type == "list":
                    coerced_value = raw_value.split(',')
                break

        # update_arg_config(dest, key, coerced_value)
        return
    
    file_mappings = read_json(args.mapping)
    if not file_mappings:
        print("No mappings loaded — exiting.")
        return

    mappings_data = file_mappings["media_mappings"]

    try:
        create_mapping_folders(mappings_data, parent_dir=args.output_dir)
    except DirAlreadyExistsException as e:
        print(f"Warning: {e} Continuing with existing folders.")

    walk_directory(
        dirpath=args.source_dir,
        mapping_data=mappings_data,
        output_dir=args.output_dir,
        copy=args.copy,
        max_depth=args.max_depth,
        min_size=args.min_size,
        max_size=args.max_size,
        ignore_extensions=args.ignore_extensions,
    )




test_dir = "../Data-Science-Topics"
