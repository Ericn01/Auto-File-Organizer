'''
Main script
'''
import json 
import os 

def read_file_mappings (filepath : str):
    try: 
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data 
    except FileNotFoundError:
        print(f"Error: The file {filepath} could not be found!")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON: {e}")

mapping_directory = "./mapping.json"
file_mappings = read_file_mappings(mapping_directory)

def get_file_extension(filepath):
    _, extension = os.path.splitext(filepath)
    return extension

def walk_directory (dirpath : str, mapping_data):
    for root, dirs, files in os.walk(dirpath):
        for file in files: 
            media_type = classify_file(file, mapping_data)
            print(f"{file} is of type {media_type}.")

# Create the mapping folders 
def create_mapping_folders (mappings_dict, parent_dir: str = '.'):
    folder_names = mappings_dict.keys()
    print(folder_names)
    for name in folder_names:
        target_dir = f"{parent_dir}/{name}"
        os.makedirs(target_dir, exist_ok=False)


def classify_file (filepath, mapping_dictionary):
    file_extention = get_file_extension(filepath)
    
    media_type = "Other"
    for media, extensions in mapping_dictionary.items():
        if file_extention in extensions:
            media_type = media 
            break 

    return media_type


test_dir = "../Data-Science-Topics"
if file_mappings:
    mappings_data = file_mappings["media_mappings"]
    walk_directory(test_dir, mappings_data)
