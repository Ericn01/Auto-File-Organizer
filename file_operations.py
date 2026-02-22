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

def classify_file (filepath, mapping_dictionary):
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
                    max_depth: int | None = -1, min_size : int | None = -1, max_size: int | None = -1, 
                    ignore_extensions: list | None = None):
    
    if max_depth is None:
        max_depth = -1
    if min_size is None:
        min_size = -1
    if max_size is None:
        max_size = -1

    ignore_extensions = [_normalize_extension(ext) for ext in (ignore_extensions or [])]
    base_depth = dirpath.rstrip(os.sep).count(os.sep)
    for root, dirs, files in os.walk(dirpath):
        if max_depth != -1: 
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

            if min_size != -1 and file_size < min_size: 
                print(f"Skipping {file} (size {file_size}B below minimum {min_size}B).")
                continue
            if max_size != -1 and file_size > max_size: 
                print(f"Skipping {file} (size {file_size}B above maximum {max_size}B).")
                continue  

            media_type = classify_file(file, mapping_data)
            destination_path = os.path.join(output_dir, media_type, file)
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            action = "Copying" if copy else "Moving"
            print(f"{action} '{file}' → {media_type}/")
            move_file(source_path, destination_path, copy=copy)
