# mytar

A CLI wrapper around GNU tar that creates compressed archives while excluding directories marked with `.notar` files and respecting `.gitignore` patterns.

## Features

- **`.notar` exclusion**: Directories containing a `.notar` file are automatically excluded from the archive
- **`.gitignore` support**: Respects patterns from `.gitignore` files found in the directory tree
- **Progress tracking**: Shows progress bars during scanning
- **Dry-run mode**: Preview what will be archived without creating the file
- **Automatic compression detection**: Detects compression based on file extension:
  - `.tar.gz` or `.tgz` → gzip compression
  - `.tar.bz2` → bzip2 compression
  - `.tar` → no compression (plain tar)
- **File replacement**: Automatically removes existing output files before creating new archives

## Installation

### Using uv (recommended)

```bash
make venv
make deps
make install
```

Or directly with uv:

```bash
uv venv .venv
uv sync
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Usage

```bash
# Gzip compression (recommended)
mytar path/to/directory archive.tar.gz

# Bzip2 compression
mytar path/to/directory archive.tar.bz2

# Plain tar (no compression)
mytar path/to/directory archive.tar

# Shortcut for gzip
mytar path/to/directory archive.tgz

# Dry run (preview what would be archived)
mytar path/to/directory archive.tar.gz --dry-run
# Note: If archive.tar.gz exists, dry run will show:
# "Note: Existing file 'archive.tar.gz' will be removed and replaced."

# Disable progress bars
mytar path/to/directory archive.tar.gz --no-progress

# Or run without installing
python -m mytar path/to/directory archive.tar.gz
```

## How It Works

1. **File extension detection**: Determines compression format from output filename:
   - `.tar.gz` / `.tgz` → uses `-z` flag (gzip)
   - `.tar.bz2` → uses `-j` flag (bzip2)
   - `.tar` → no compression flag
2. **Scans for `.notar` files**: Any directory containing a `.notar` file is marked for exclusion
3. **Parses `.gitignore` files**: Found patterns are used to identify additional exclusions
4. **Builds tar command**: Runs `tar` with appropriate compression flags and `--exclude-tag`, `--exclude-vcs`, and `--exclude-vcs-ignores` arguments
5. **Removes existing file**: If the output file already exists, it is deleted before creating the new archive

## Examples

### Creating an archive excluding venv and cache directories

```bash
# Create test directory structure
mkdir -p myproject/.venv/lib
mkdir -p myproject/.cache/data
mkdir -p myproject/src

# Mark directories to exclude
touch myproject/.venv/.notar
touch myproject/.cache/.notar

# Create some content
echo "Hello" > myproject/src/main.py

# Create archive (excludes .venv and .cache)
mytar myproject/ myproject.tar.gz
```

### Creating a plain tar archive (no compression)

```bash
mytar myproject/ myproject.tar
```

### Creating a bzip2 compressed archive

```bash
mytar myproject/ myproject.tar.bz2
```

### Using with git repositories

If you have a `.gitignore` in your project:

```
__pycache__/
*.pyc
.venv/
```

mytar will automatically respect these patterns when creating archives.

## Makefile Targets

| Target | Description |
|--------|-------------|
| `make venv` | Initialize the virtual environment |
| `make deps` | Install project dependencies |
| `make test` | Run project tests |
| `make lint` | Run ruff lint checks |
| `make clean` | Remove build artifacts |
| `make install` | Install package in editable mode |

## Requirements

- Python 3.11+
- click
- tqdm
- GNU tar

## License

MIT
