import os 
import shutil

def get_file_extension(filepath):
    _, extension = os.path.splitext(filepath)
    return extension

def classify_file (filepath, mapping_dictionary):
    file_extention = get_file_extension(filepath)
    media_type = "Other"
    for media, extensions in mapping_dictionary.items():
        if file_extention in extensions:
            media_type = media 
            break 
    return media_type


class DirAlreadyExistsException(Exception):
    """Exception raised when a directory with the same name exists already"""


# Create the mapping folders 
def create_mapping_folders (mappings_dict, parent_dir: str = '.'):
    folder_names = mappings_dict.keys()
    dir_folders = os.listdir(parent_dir)
    for name in folder_names:
        target_dir = os.path.join(parent_dir, name)
        if name not in dir_folders:
            os.makedirs(target_dir, exist_ok=True)
        else:
            raise DirAlreadyExistsException(f"The directory with name '{name}' already exists")

def move_file(source : str, destination : str, copy=False):
    if copy:
        shutil.copyfile(src=source, dst=destination)
    else: 
        shutil.move(src=source, dst=destination)


def walk_directory (dirpath : str, mapping_data, output_dir: str, copy: bool = False, 
                    max_depth: int = -1, min_size : int = -1, max_size: int = -1, 
                    ignore_entensions: list = []):
    
    ignore_entensions = [ext.lower() for ext in ignore_entensions]
    base_depth = dirpath.rstrip(os.sep).count(os.sep)
    for root, dirs, files in os.walk(dirpath):
        if max_depth != -1: 
            current_depth = root.rstrip(os.sep).count(os.sep) - base_depth 
            if current_depth >= max_depth:
                dirs.clear()
        
        for file in files: 
            ext = get_file_extension(file).lower()

            if ext in ignore_entensions:
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
            action = "Copying" if copy else "Moving"
            print(f"{action} '{file}' → {media_type}/")
            move_file(source_path, destination_path, copy=copy)