import os 
import shutil
import json

def read_file_mappings(filepath: str):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file {filepath} could not be found!")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON: {e}")

def get_file_extension(filepath):
    _, extension = os.path.splitext(filepath)
    return extension

def _normalize_extension(extension: str) -> str:
    extension = (extension or "").strip().lower()
    if not extension:
        return ""
    if not extension.startswith("."):
        return f".{extension}"
    return extension

def _normalize_category_name(name: str) -> str:
    return (name or "").strip().lower()

def _flatten_category_args(values: list | None) -> list[str] | None:
    if not values:
        return None
    flattened: list[str] = []
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        # Allow both nargs-style and comma-separated lists for robustness.
        parts = text.split(",") if "," in text else [text]
        for part in parts:
            part = part.strip()
            if part:
                flattened.append(part)
    return flattened or None

def filter_mapping_categories(
    mapping_data: dict,
    include_categories: list | None = None,
    exclude_categories: list | None = None,
    warn=print,
):
    """
    Filter mapping categories (mapping.json keys) for a run.

    - include_categories keeps only specified existing categories.
    - exclude_categories removes specified existing categories.
    - Unknown categories emit warnings and are ignored.
    - If both are provided, include is applied first, then exclude.
    """
    include_categories = _flatten_category_args(include_categories)
    exclude_categories = _flatten_category_args(exclude_categories)

    if not include_categories and not exclude_categories:
        return mapping_data

    lower_to_key: dict[str, str] = {}
    for key in mapping_data.keys():
        normalized = _normalize_category_name(key)
        if normalized and normalized not in lower_to_key:
            lower_to_key[normalized] = key

    result = dict(mapping_data)

    if include_categories:
        filtered: dict = {}
        for requested in include_categories:
            normalized = _normalize_category_name(requested)
            if normalized in lower_to_key:
                key = lower_to_key[normalized]
                filtered[key] = mapping_data[key]
            else:
                warn(f"Warning: include category '{requested}' does not exist in mapping.json")
        result = filtered

    if exclude_categories:
        for requested in exclude_categories:
            normalized = _normalize_category_name(requested)
            if normalized in lower_to_key:
                key = lower_to_key[normalized]
                result.pop(key, None)
            else:
                warn(f"Warning: exclude category '{requested}' does not exist in mapping.json")

    return result

def classify_file_extension (filepath, mapping_dictionary):
    file_extention = _normalize_extension(get_file_extension(filepath))
    media_type = "Other"
    for media, extensions in mapping_dictionary.items():
        normalized_extensions = {_normalize_extension(ext) for ext in extensions}
        if file_extention in normalized_extensions:
            media_type = media 
            break 
    return media_type


class DirAlreadyExistsException(Exception):
    """Exception raised when a directory with the same name exists already"""


# Create the mapping folders 
def create_mapping_folders(mappings_dict, parent_dir: str = '.', strict: bool = True, include_other: bool = False):
    folder_names = list(mappings_dict.keys())
    if include_other and "Other" not in folder_names:
        folder_names.append("Other")

    os.makedirs(parent_dir, exist_ok=True)

    for name in folder_names:
        target_dir = os.path.join(parent_dir, name)
        if os.path.exists(target_dir):
            if strict:
                raise DirAlreadyExistsException(f"The directory with name '{name}' already exists")
            continue
        os.makedirs(target_dir, exist_ok=True)

def move_file(source : str, destination : str, copy=False):
    if copy:
        shutil.copyfile(src=source, dst=destination)
    else: 
        shutil.move(src=source, dst=destination)


def walk_directory (dirpath : str, mapping_data, output_dir: str, copy: bool = False, 
                    max_depth: int | None = None, min_size : int | None = None, max_size: int | None = None, 
                    ignore_extensions: list | None = None):
    
    ignore_extensions = [_normalize_extension(ext) for ext in (ignore_extensions or [])]
    base_depth = dirpath.rstrip(os.sep).count(os.sep)
    for root, dirs, files in os.walk(dirpath):
        if max_depth: 
            current_depth = root.rstrip(os.sep).count(os.sep) - base_depth 
            if current_depth >= max_depth:
                dirs.clear()
        
        for file in files: 
            ext = _normalize_extension(get_file_extension(file))

            if ext in ignore_extensions:
                print(f"Skipping {file} (ignore extension).")
                continue 

            source_path = os.path.join(root, file)
            file_size = os.path.getsize(source_path)

            if min_size and (file_size < min_size): 
                print(f"Skipping {file} (size {file_size}B below minimum {min_size}B).")
                continue
            if max_size and (file_size > max_size): 
                print(f"Skipping {file} (size {file_size}B above maximum {max_size}B).")
                continue  

            media_type = classify_file_extension(file, mapping_data)
            destination_path = os.path.join(output_dir, media_type, file)
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            action = "Copying" if copy else "Moving"
            print(f"{action} '{file}' → {media_type}/")
            move_file(source_path, destination_path, copy=copy)


def handle_run(args, arg_config: dict):
    """Handle the 'run' subcommand — filter, create folders, and walk the directory."""
    file_mappings = read_file_mappings(args.mapping)
    if not file_mappings:
        print("No mappings loaded. Exiting.")
        return

    mappings_data = file_mappings.get("media_mappings", {})

    mappings_data = filter_mapping_categories(
        mappings_data,
        include_categories=getattr(args, "include_categories", None),
        exclude_categories=getattr(args, "exclude_categories", None),
    )

    create_mapping_folders(
        mappings_data,
        parent_dir=args.output_dir,
        strict=False,
        include_other=True,
    )

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