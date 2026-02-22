'''
Main script
'''
import file_operations
import parser_builder
import configuration

def coerce_value(raw_value: str, data_type: str = "str"):
    if raw_value is None:
        return None

    match data_type:
        case "int":
            return int(raw_value)
        case "float":
            return float(raw_value)
        case "bool":
            if isinstance(raw_value, bool):
                return raw_value
            return str(raw_value).strip().lower() in ("true", "1", "yes", "y", "on")
        case "list":
            text = str(raw_value).strip()
            if not text:
                return []
            parts = text.split(",") if "," in text else text.split()
            return [p.strip() for p in parts if p.strip()]
        case _:
            return raw_value

def main(): 
    arg_config = configuration.load_arg_config()
    parser = parser_builder.build_parser(arg_config)
    args = parser.parse_args()

    # Config management commands
    if args.reset_config: 
        configuration.save_arg_config(configuration.DEFAULT_ARG_CONFIG)
        print("Config reset to defaults")
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
                coerced_value = coerce_value(raw_value, entry.get("type", "str"))
                break
                
        try:
            configuration.update_arg_config(dest, key, coerced_value)
        except KeyError as e:
            print(f"Error: {e}")
        return 

    if not args.source_dir or not args.output_dir:
        print("Error: source_dir and output_dir are required unless using --reset-config or --set-default.")
        parser.print_help()
        return

    file_mappings = file_operations.read_file_mappings(args.mapping)
    if not file_mappings:
        print("No mappings loaded. Exiting.")
        return

    mappings_data = file_mappings.get("media_mappings", {})

    # Filtered mapping data if include_categories or exclude_categories is applied.
    mappings_data = file_operations.filter_mapping_categories(
        mappings_data,
        include_categories=getattr(args, "include_categories", None),
        exclude_categories=getattr(args, "exclude_categories", None),
    )

    file_operations.create_mapping_folders(
        mappings_data,
        parent_dir=args.output_dir,
        strict=False,
        include_other=True,
    )

    file_operations.walk_directory(
        dirpath=args.source_dir,
        mapping_data=mappings_data,
        output_dir=args.output_dir,
        copy=args.copy,
        max_depth=args.max_depth,
        min_size=args.min_size,
        max_size=args.max_size,
        ignore_extensions=args.ignore_extensions,
    )


if __name__ == "__main__":
    main()
