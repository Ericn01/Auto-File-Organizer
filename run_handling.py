import configuration
import file_operations
from constants import DEFAULT_ARG_CONFIG
from utils import coerce_value
import os

def handle_config(args, arg_config: dict) -> bool:
    """
    Handle all 'config' subcommand actions.
    Returns True if a config action was handled (so main can return early).
    """
    if args.reset_config:
        configuration.save_arg_config(DEFAULT_ARG_CONFIG)
        print("Config reset to defaults.")
        return True

    if args.list_config:
        print("\nCurrent default configuration:\n")
        for section, entries in arg_config.items():
            print(f"  [{section}]")
            for entry in entries:
                print(f"    {entry['dest']}: {entry.get('default')!r} → {entry.get('help', '')}")
        print()
        return True

    if args.set_default:
        raw_dest_key, raw_value = args.set_default
        if '.' not in raw_dest_key:
            print("Error: --set-default expects DEST.KEY format, e.g. max_depth.default 3")
            return True
        dest, key = raw_dest_key.split('.', 1)

        # Find the entry across both config sections to determine the correct type
        coerced_value = raw_value
        for entries in arg_config.values():
            for entry in entries:
                if entry.get("dest") == dest:
                    coerced_value = coerce_value(raw_value, entry.get("type", "str"))
                    break

        try:
            configuration.update_arg_config(dest, key, coerced_value)
        except KeyError as e:
            print(f"Error: {e}")
        return True

    return False


def handle_run(args):
    """Handle the 'run' subcommand: filter, create folders, and walk the directory."""
    file_mappings = file_operations.read_file_mappings(args.mapping)
    if not file_mappings:
        print("No mappings loaded. Exiting.")
        return

    mappings_data = file_mappings.get("media_mappings", {})

    # If the user has narrowed the run to specific categories, there is no meaningful "Other" category; unrecognised files are simply left alone.
    category_filter_active = bool(args.include_categories or args.exclude_categories)
    include_other = not category_filter_active

    mappings_data = file_operations.filter_mapping_categories(
        mappings_data,
        include_categories=getattr(args, "include_categories", None),
        exclude_categories=getattr(args, "exclude_categories", None),
    )

    # Create the output directory upfront, but create category folders lazily only when a valid (unskipped) file is actually written there.
    os.makedirs(args.output_dir, exist_ok=True)

    file_operations.walk_directory(
        dirpath=args.source_dir,
        mapping_data=mappings_data,
        output_dir=args.output_dir,
        copy=args.copy,
        max_depth=args.max_depth,
        min_size=args.min_size,
        max_size=args.max_size,
        ignore_extensions=args.ignore_extensions,
        skip_duplicates=args.skip_duplicates,
        include_other=include_other
    )
