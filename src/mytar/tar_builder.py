"""Tar archive builder using tar's native exclusion flags."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class TarBuilder:
    """Builds tar archives using tar's --exclude-tag and --exclude-vcs flags."""

    def __init__(self, root: Path, show_progress: bool = True):
        """Initialize the tar builder.

        Args:
            root: Root directory to archive
            show_progress: Whether to show progress bars
        """
        self.root = Path(root).resolve()
        self.show_progress = show_progress

    def build(self, output_path: Path, dry_run: bool = False) -> bool:
        """Build the tar archive.

        Args:
            output_path: Path to the output .tar, .tar.gz, or .tar.bz2 file
            dry_run: If True, only print what would be done

        Returns:
            True if successful, False otherwise
        """
        # Check if output file exists and warn about removal
        if output_path.exists():
            if dry_run:
                print(f"Note: Existing file '{output_path}' will be removed and replaced.")
            else:
                # Remove the existing tar file before creating new one
                output_path.unlink()

        cmd = self._build_tar_command(output_path)

        if dry_run:
            print("Would run:", " ".join(cmd))
            return True

        return self._execute_tar(cmd)

    def _build_tar_command(self, output_path: Path) -> list[str]:
        """Build the tar command with native exclusion flags.

        Args:
            output_path: Path to output archive

        Returns:
            List of command arguments
        """
        cmd = ["tar"]

        # Detect compression based on file extension
        if str(output_path).endswith('.gz') or str(output_path).endswith('.tgz'):
            # Gzip compression
            cmd.extend(["-cvzf", str(output_path)])
        elif str(output_path).endswith('.bz2'):
            # Bzip2 compression
            cmd.extend(["-cvjf", str(output_path)])
        else:
            # No compression (plain tar)
            cmd.extend(["-cvf", str(output_path)])

        # Use --exclude-tag to exclude directories containing .notar
        # The .notar file itself is still included (marker file)
        cmd.append("--exclude-tag=.notar")

        # Use --exclude-vcs to exclude version control directories (.git, .hg, etc.)
        cmd.append("--exclude-vcs")

        # Use --exclude-vcs-ignores to respect .gitignore, .hgignore, etc.
        cmd.append("--exclude-vcs-ignores")

        # Add the root directory to archive
        cmd.extend(["-C", str(self.root.parent)])
        cmd.append(self.root.name)

        return cmd

    def _execute_tar(self, cmd: list[str]) -> bool:
        """Execute the tar command.

        Args:
            cmd: Command to execute

        Returns:
            True if successful, False otherwise
        """
        if self.show_progress:
            print("Executing tar...")

        try:
            result = subprocess.run(
                cmd,
                stdout=None,
                stderr=subprocess.PIPE,
                text=True,
            )

            if result.returncode != 0:
                print(f"Error running tar: {result.stderr}", file=sys.stderr)
                return False

            return True

        except FileNotFoundError:
            print("Error: tar command not found. Is GNU tar installed?", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Error executing tar: {e}", file=sys.stderr)
            return False
