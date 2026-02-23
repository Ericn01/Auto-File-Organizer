# Automatic File Organizer

A command-line tool that automatically organises files in a directory into categorised subfolders based on their type. By default this includes categories like Images, Videos, Documents, and so on. The mappings for the categories to file extensions are defined in `mapping.json` and can be modified as needed. You can move or copy files, filter by size, limit how deep it searches, and ignore specific file types. All of your preferred settings are saved to a config file so you don't have to re-type them every time.


## Demo Video

[![Automatic File Organizer Video Thumbnail](https://img.youtube.com/vi/kfzUY_VLy4M/0.jpg)](https://www.youtube.com/watch?v=kfzUY_VLy4M "Automatic File Organizer Script Showcase")


## Project Structure

```
auto-file-organizer/
├── main.py           # The main script
├── mapping.json      # Defines which file extensions belong to which category
└── args.json         # Your saved default settings (auto-created on first run)
```


## Setting Up Your Mapping File

Before running the tool, make sure you have a `mapping.json` file in the same folder as `main.py`. This file tells the tool how to categorise files. Here's an example:

```json
{
    "media_mappings": {
        "Images":    [".jpg", ".jpeg", ".png", ".gif", ".webp"],
        "Videos":    [".mp4", ".mov", ".avi", ".mkv"],
        "Audio":     [".mp3", ".wav", ".flac", ".aac"],
        "Programming":      [".py", ".js", ".html", ".css", ".json"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
        "Spreadsheets": [".csv", ".xlsx", ".xls", ".ods", ".numbers", ".tsv"]
    }
}
```

You can add, remove, or rename any of the categories and extensions to suit your needs. Any file whose extension isn't listed will be placed in an **Other** folder automatically.


## Usage Overview

The tool has two subcommands. Use `run` to sort files, and `config` to manage your saved settings:

```bash
python main.py run <source_dir> <output_dir> [options]
python main.py config [options]
```

You can always add `--help` to either subcommand to see a full list of its options:

```bash
python main.py run --help
python main.py config --help
```

## The `run` Subcommand

This is the command that actually moves or copies your files.

```bash
python main.py run   [options]
```

| Argument | Description |
|---|---|
| `source_dir` | The folder you want to sort (e.g. `./Downloads`) |
| `output_dir` | The folder where sorted subfolders will be created (e.g. `./Sorted`) |

### Run Options

| Flag | Description |
|---|---|
| `--copy` | Copy files instead of moving them (original files are left in place) |
| `--mapping PATH` | Use a custom mapping file (default: `./mapping.json`) |
| `--max-depth N` | Only search N levels of subfolders deep (default: unlimited) |
| `--min-size N` | Skip files smaller than N bytes |
| `--max-size N` | Skip files larger than N bytes |
| `--ignore-extensions .x .y` | Skip any files with these extensions |
| `--include-categories A B` | Only sort these categories. Everything else is ignored |
| `--exclude-categories A B` | Sort everything except these categories |

### Examples

**1. Sort your Downloads folder (move mode):**
```bash
python main.py run ./Downloads ./Sorted
```

**2. Copy files instead of moving them:**
```bash
python main.py run ./Downloads ./Sorted --copy
```

**3. Only search 2 levels deep, and skip files smaller than 1 KB:**
```bash
python main.py run ./Downloads ./Sorted --max-depth 2 --min-size 1024
```

**4. Copy files between 1 KB and 10 MB, skipping temp and log files:**
```bash
python main.py run ./Downloads ./Sorted --copy --min-size 1024 --max-size 10485760 --ignore-extensions .tmp .log
```

**5. Only sort Images, Videos, and Audio. Ignore everything else:**
```bash
python main.py run ./Downloads ./Sorted --include-categories Images Videos Audio
```

**6. Sort everything except Archives and System files:**
```bash
python main.py run ./Downloads ./Sorted --exclude-categories Archives System
```

## The `config` Subcommand

Use this to view and update the default settings saved in `args.json`. Changes made here apply automatically to every future `run`.

```bash
python main.py config [options]
```

### Config Options

| Flag | Description |
|---|---|
| `--list` | Print all current saved defaults |
| `--set-default DEST.KEY VALUE` | Update a single setting and save it |
| `--reset` | Wipe `args.json` and restore all built-in defaults |

### Examples

**See all your current saved defaults:**
```bash
python main.py config --list
```

**Always copy files instead of moving them:**
```bash
python main.py config --set-default copy.default true
```

**Set a default minimum file size of 1 KB (1024 bytes):**
```bash
python main.py config --set-default min_size.default 1024
```

**Set a default maximum file size of 10 MB:**
```bash
python main.py config --set-default max_size.default 10485760
```

**Limit search depth to 3 levels by default:**
```bash
python main.py config --set-default max_depth.default 3
```

**Change the default mapping file path:**
```bash
python main.py config --set-default mapping.default ./my_custom_mapping.json
```

**Reset everything back to factory defaults:**
```bash
python main.py config --reset
```

## Options

Add any of these flags to customise how the tool runs:

| Flag | Description | Example |
|---|---|---|
| `--copy` | Copy files instead of moving them | `--copy` |
| `--include-categories CATEGORY [CATEGORY ...]` | Only use specific categories from `mapping.json` (unknown categories warn) | `--include-categories Images Videos` |
| `--exclude-categories CATEGORY [CATEGORY ...]` | Exclude specific categories from `mapping.json` (unknown categories warn) | `--exclude-categories Archives` |
| `--max-depth N` | Only search N levels deep (default: unlimited) | `--max-depth 2` |
| `--min-size N` | Skip files smaller than N bytes | `--min-size 1024` |
| `--max-size N` | Skip files larger than N bytes | `--max-size 10485760` |
| `--ignore-extensions` | Skip files with these extensions | `--ignore-extensions .tmp .log` |
| `--mapping PATH` | Use a custom mapping file (default: `./mapping.json`) | `--mapping ./my_map.json` |
| `--skip-duplicates` | Skip files when the destination filename already exists | `--skip-duplicates` |

**Example: copy only files between 1 KB and 10 MB, ignoring temp files:**
```bash
python main.py run ./Downloads ./Sorted --copy --min-size 1024 --max-size 10485760 --ignore-extensions .tmp .log
```


## How It Works

1. **On first run**, the tool creates an `args.json` file containing all the default settings.
2. **It reads `mapping.json`** to learn which file extensions map to which category names.
3. **It creates a subfolder** for each category inside your output directory.
4. **It walks through your source directory**, checks each file against your filters (size, extension, depth), and moves or copies it into the right subfolder.
5. **Files that don't match any category** are placed in an `Other` subfolder.

