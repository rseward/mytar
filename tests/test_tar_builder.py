"""Integration tests for mytar."""

import tarfile
import tempfile
from pathlib import Path

import pytest

from mytar.tar_builder import TarBuilder


class TestTarBuilder:
    """Integration tests for TarBuilder."""

    def test_build_basic_archive(self, tmp_path):
        """Test creating a basic archive without exclusions."""
        # Create source directory
        source = tmp_path / "source"
        source.mkdir()
        (source / "file1.txt").write_text("Hello")
        (source / "file2.txt").write_text("World")

        output = tmp_path / "archive.tar.gz"

        builder = TarBuilder(source, show_progress=False)
        result = builder.build(output)

        assert result is True
        assert output.exists()

        # Verify contents
        with tarfile.open(output, "r:gz") as tf:
            names = tf.getnames()
            assert len(names) == 3  # source/file1.txt, source/file2.txt, and possibly source/

    def test_build_with_notar_exclusion(self, tmp_path):
        """Test that .notar directories' contents are excluded.

        Note: --exclude-tag=.notar excludes directory contents but keeps
        the directory entry and .notar marker file itself.
        """
        # Create source with subdirectories
        source = tmp_path / "source"
        source.mkdir()
        (source / "file.txt").write_text("Include me")

        excluded_dir = source / "excluded"
        excluded_dir.mkdir()
        (excluded_dir / "file.txt").write_text("Exclude me")
        (excluded_dir / ".notar").touch()

        output = tmp_path / "archive.tar.gz"

        builder = TarBuilder(source, show_progress=False)
        result = builder.build(output)

        assert result is True

        # Verify excluded dir contents are not in archive
        # (directory and .notar may still appear, but not file.txt)
        with tarfile.open(output, "r:gz") as tf:
            names = tf.getnames()
            # The actual file should be excluded
            assert "source/excluded/file.txt" not in names

    def test_dry_run(self, tmp_path):
        """Test dry-run mode doesn't create archive."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "file.txt").write_text("Hello")

        output = tmp_path / "archive.tar.gz"

        builder = TarBuilder(source, show_progress=False)
        result = builder.build(output, dry_run=True)

        assert result is True
        assert not output.exists()

    def test_tar_command_structure(self, tmp_path):
        """Test that tar command is built correctly with native flags."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "file.txt").write_text("Hello")

        output = tmp_path / "archive.tar.gz"

        builder = TarBuilder(source, show_progress=False)

        cmd = builder._build_tar_command(output)
        assert cmd[0] == "tar"
        assert "-cvzf" in cmd
        assert str(output) in cmd
        assert "--exclude-tag=.notar" in cmd
        assert "--exclude-vcs" in cmd
        assert "--exclude-vcs-ignores" in cmd

    def test_notar_marker_file_included(self, tmp_path):
        """Test that .notar marker file itself is still included."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "file.txt").write_text("Hello")

        excluded_dir = source / "excluded"
        excluded_dir.mkdir()
        (excluded_dir / ".notar").touch()
        (excluded_dir / "secret.txt").write_text("Exclude me")

        output = tmp_path / "archive.tar.gz"

        builder = TarBuilder(source, show_progress=False)
        result = builder.build(output)

        assert result is True

        # Verify .notar file is in archive (marker kept)
        with tarfile.open(output, "r:gz") as tf:
            names = tf.getnames()
            notar_paths = [n for n in names if ".notar" in n]
            # .notar file itself should be included
            assert len(notar_paths) == 1
            assert "excluded/.notar" in notar_paths[0]
