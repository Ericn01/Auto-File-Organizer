# Automatic File Organizer

A command-line tool that automatically organises files in a directory into categorised subfolders based on their type. By default this includes categories like Images, Videos, Documents, and so on. The mappings for the categories to file extensions are defined in `mapping.json` and can be modified as needed. You can move or copy files, filter by size, limit how deep it searches, and ignore specific file types. All of your preferred settings are saved to a config file so you don't have to re-type them every time.

---

## Demo Video

[![Alt text for the image](https://img.youtube.com/vi/kfzUY_VLy4M/0.jpg)](https://www.youtube.com/watch?v=kfzUY_VLy4M "Automatic File Organizer Script Showcase")

---

## Project Structure

```
auto-file-organizer/
├── main.py           # The main script
├── mapping.json      # Defines which file extensions belong to which category
└── args.json         # Your saved default settings (auto-created on first run)
```

---

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

---

## Basic Usage

```bash
python main.py <source_dir> <output_dir>
```

| Argument | Description |
|---|---|
| `source_dir` | The folder you want to sort (e.g. `./Downloads`) |
| `output_dir` | The folder where sorted subfolders will be created (e.g. `./Sorted`) |

**Example — sort your Downloads folder:**
```bash
python main.py ./Downloads ./Sorted
```

This will scan `./Downloads` and move all files into categorised subfolders inside `./Sorted`.

---

## Options

Add any of these flags to customise how the tool runs:

| Flag | Description | Example |
|---|---|---|
| `--copy` | Copy files instead of moving them | `--copy` |
| `--max-depth N` | Only search N levels deep (default: unlimited) | `--max-depth 2` |
| `--min-size N` | Skip files smaller than N bytes | `--min-size 1024` |
| `--max-size N` | Skip files larger than N bytes | `--max-size 10485760` |
| `--ignore-extensions` | Skip files with these extensions | `--ignore-extensions .tmp .log` |
| `--mapping PATH` | Use a custom mapping file (default: `./mapping.json`) | `--mapping ./my_map.json` |

**Example: copy only files between 1 KB and 10 MB, ignoring temp files:**
```bash
python main.py ./Downloads ./Sorted --copy --min-size 1024 --max-size 10485760 --ignore-extensions .tmp .log
```

---

## Saving Your Preferred Settings

Instead of typing the same flags every time, you can save them as new defaults to `args.json`.

Use the `--set-default` flag followed by the setting name and value:

```bash
python main.py <source_dir> <output_dir> --set-default <setting.field> <value>
```

**Examples:**

```bash
# Always copy files instead of moving them
python main.py ./src ./out --set-default copy.default true

# Set a default minimum file size of 1 KB
python main.py ./src ./out --set-default min_size.default 1024

# Set a default max search depth of 3 levels
python main.py ./src ./out --set-default max_depth.default 3
```

Once saved, those values will be used automatically on every future run — unless you override them with a flag in the command.

### Available Setting Names

| Setting Name | What It Controls |
|---|---|
| `copy.default` | Whether to copy instead of move (`true` / `false`) |
| `max_depth.default` | How many folder levels deep to search |
| `min_size.default` | Minimum file size in bytes |
| `max_size.default` | Maximum file size in bytes |
| `ignore_extensions.default` | Comma-separated list of extensions to skip |
| `mapping.default` | Path to the mapping JSON file |

---

## Resetting to Default Settings

If your `args.json` config gets into a messy state, you can wipe it and start fresh:

```bash
python main.py <source_dir> <output_dir> --reset-config
```

This restores all settings to their original out-of-the-box values.

---

## How It Works

1. **On first run**, the tool creates an `args.json` file containing all the default settings.
2. **It reads `mapping.json`** to learn which file extensions map to which category names.
3. **It creates a subfolder** for each category inside your output directory.
4. **It walks through your source directory**, checks each file against your filters (size, extension, depth), and moves or copies it into the right subfolder.
5. **Files that don't match any category** are placed in an `Other` subfolder.

---

## Troubleshooting

**"The file mapping.json could not be found"**
Make sure `mapping.json` exists in the same directory as `main.py`, or pass a custom path using `--mapping`.

**"The directory '...' already exists"**
The output folder already has a subfolder with that category name from a previous run. The tool will continue using it; this is expected behaviour and not an error.

**Files aren't being moved**
Check that your `source_dir` path is correct and that the files you expect to be sorted have extensions listed in your `mapping.json`.

---

