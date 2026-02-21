'''
Main script
'''
import json 
import os 
import shutil
import argparse  

def read_json (filepath : str):
    try: 
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data 
    except FileNotFoundError:
        print(f"Error: The file {filepath} could not be found!")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON: {e}")

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

def move_file(source, destination, copy=False):
    if copy:
        shutil.copyfile(src=source, dst=destination)
    else: 
        shutil.move(src=source, dst=destination)

def walk_directory (dirpath : str, mapping_data, output_dir: str, config):
    for root, dirs, files in os.walk(dirpath):
        for file in files: 
            media_type = classify_file(file, mapping_data)
            print(f"{file} is of type {media_type}.")



def save_arg_config(config, filepath: str) -> None 
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Argument config saved to {filepath}")

def add_optional_argument()

def main():
    CONFIG_FILEPATH = "./config.json"
    config = read_json(CONFIG_FILEPATH)

    if config is None:
        print("Error: Could not load configuration data. Exiting.")
        exit(1)

    parser = argparse.ArgumentParser(
        description="Sort files in a directory into categorised subfolders by media type."
    )
    parser.add_argument("source_dir",
                        help="Path to the directory to scan.")
    parser.add_argument("output_dir",
                        help="Path to the directory where sorted subfolders will be created.")
    args = parser.parse_args()


    mappings_data = file_mappings["media_mappings"]

    try:
        create_mapping_folders(mappings_data, parent_dir=args.output_dir)
    except DirAlreadyExistsException as e:
        print(f"Warning: {e}. Continuing with existing folders.")

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
