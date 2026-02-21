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

print(file_mappings)

def get_file_extension(filepath):
    _, extension = os.path.splitext(filepath)
    return extension

def walk_directory (dirpath : str):
    for root, dirs, files in os.walk(dirpath):
        # Current directory
        print(f"Current directory: {root}")
        # Print all available directories 
        print(f"Directories at current level: {dirs}")
        # Files at current level 
        print(f"Files in current directory: {files}")

        for f in files:
            print(f"File extension: {get_file_extension(f)}")


walk_directory("/home/darkii/Takeout")