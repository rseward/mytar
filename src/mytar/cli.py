"""CLI interface for mytar."""

from __future__ import annotations

from pathlib import Path

import click
import os

from mytar import __version__
from mytar.tar_builder import TarBuilder


@click.command()
@click.argument("source_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--no-progress",
    is_flag=True,
    default=False,
    help="Disable progress bar output",
)
@click.option(
    "--dry-run",
    "--dry",
    "--dryrun",
    "dry_run",
    is_flag=True,
    default=False,
    help="Show what would be archived without creating the tar file",
)
@click.version_option(version=__version__)
def main(source_dir: Path, output_file: Path, no_progress: bool, dry_run: bool) -> int:
    """Create a compressed tar archive excluding .notar-marked directories.

    SOURCE_DIR is the directory to archive.

    OUTPUT_FILE is the path to the resulting .tar.gz file.
    """
    # Ensure output_file has a valid tar extension
    output_str = str(output_file)
    if not (output_str.endswith(('.tar.gz', '.tgz', '.tar.bz2', '.tar'))):
        # Default to .tar.gz if no recognized extension
        output_file = Path(output_str + ".tar.gz")

    builder = TarBuilder(root=source_dir, show_progress=not no_progress)

    success = builder.build(output_path=output_file, dry_run=dry_run)

    if success:
        if dry_run:
            click.echo("Dry run complete. No archive was created.")
        else:
            click.echo(f"Archive created: {output_file}")
            os.system(f"ls -lh {output_file}")
        return 0
    else:
        click.echo("Failed to create archive.", err=True)
        return 1
