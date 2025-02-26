import subprocess
import sys
from pathlib import Path
import pytest
import argparse
from src.cli import main
from unittest.mock import patch

@pytest.fixture
def mock_project_structure(tmp_path):
    """Create a temporary mock project structure for testing."""
    (tmp_path / "folder1").mkdir()
    (tmp_path / "folder1" / "file1.txt").touch()
    (tmp_path / "folder2").mkdir()
    (tmp_path / "folder2" / "file2.txt").touch()
    (tmp_path / "ignore_me").mkdir()
    return tmp_path

@pytest.mark.parametrize("args, expected_output, expected_file", [
    (["mock_dir", "--ignore", "ignore_me"], "Mocked Structure\n", None),
    (["mock_dir", "--output", "output.txt"], None, "output.txt"),
])
@patch("argparse.ArgumentParser.parse_args")
@patch("src.cli.ProjectStructureBuilder")
@patch("builtins.print")
def test_cli_variants(mock_print, mock_builder, mock_args, args, expected_output, expected_file):
    """Test CLI execution with and without an output file."""
    mock_args.return_value = argparse.Namespace(
        base_dir=args[0],
        ignore=args[2:] if "--ignore" in args else [],
        output=args[-1] if "--output" in args else None
    )

    mock_instance = mock_builder.return_value
    mock_instance.build.return_value = "Mocked Structure\n"

    main()

    mock_builder.assert_called_once_with("mock_dir", ["ignore_me"] if "--ignore" in args else [])
    
    if expected_file:
        mock_instance.save_to_file.assert_called_once_with(expected_file)
    else:
        mock_print.assert_called_once_with(expected_output)

@patch("sys.stdout.reconfigure")
@patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
    base_dir="mock_dir", ignore=[], output=None
))
@patch("src.cli.ProjectStructureBuilder")
def test_cli_utf8_reconfiguration(mock_builder, mock_args, mock_reconfigure):
    """Test if sys.stdout.reconfigure is called for UTF-8 encoding."""
    main()
    mock_reconfigure.assert_called_once_with(encoding="utf-8")

@patch("argparse.ArgumentParser.parse_args", side_effect=SystemExit)
def test_cli_missing_arguments(mock_args):
    """Test CLI when required arguments are missing (should raise SystemExit)."""
    with pytest.raises(SystemExit):
        main()

@patch("builtins.print")
@patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
    base_dir="", ignore=[], output=None
))
@patch("src.cli.ProjectStructureBuilder", side_effect=FileNotFoundError)
def test_cli_invalid_directory(mock_builder, mock_args, mock_print):
    """Test CLI when the base directory does not exist (should handle FileNotFoundError)."""
    with pytest.raises(FileNotFoundError):
        main()

def test_cli_main_execution():
    """Test executing cli.py as a script to cover `if __name__ == "__main__"`."""
    script_path = Path("src/cli.py").resolve()
    
    result = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        capture_output=True,
        text=True
    )
    
    assert "usage:" in result.stdout  # Ensure argparse runs without errors
    assert result.returncode == 0  # Ensure successful execution

