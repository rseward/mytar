# Purpose

Create a simple python CLI tool around the GNU tar utility.

When given a directory to tar, it will look for .notar flag files in the sub-directories.
As the tool finds such files it will build an exclusion list for such sub-directories.

The tool should call the tar utility with -cvzf options specifying a target file given from the CLI.
The tool will also pass a list of excluded directories that should be omitted from the tar.

If the tool finds .gitignore files in the directory structure it will honor those exclusions as well.

This is not a complete wrapper around tar. It is just a convenient wrapper for creating new tar files
excluding unwanted files.

## Python Requirements

- Use python click module for CLI parsing
- Use python's uv tool for dep management
- Create a Makefile with these targets
  - make venv -> Initialize the virtual env
  - make deps -> Install project deps
  - make test -> Run project tests
  - make lint -> Run ruff lint checks
- Use tqdm if file scans are needed before executing tar
- Write an appropriate set of documentation including user usage for the utility.

## Examples

```
mkdir -p foo/boo
mkdir -p foo/.git
mkdir -p foo/.venv

touch foo/boo/.notar
touch foo/.git/.notar
touch foo/.venv/.notar
echo "Hello data!" > foo/bar
```

./mytar.py foo/ foo.tar.gz -> The complete contents of the foo directory will be tar save the directories marked with .notar exclusion file tags.


