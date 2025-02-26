import pytest
import os
from src.structure.builder import ProjectStructureBuilder

@pytest.fixture
def mock_project_structure(tmp_path):
    """Create a temporary mock project structure for testing."""
    (tmp_path / "folder1").mkdir()
    (tmp_path / "folder1" / "file1.py").touch()
    (tmp_path / "folder1" / "README.md").touch()
    
    (tmp_path / "folder2").mkdir()
    (tmp_path / "folder2" / "file2.txt").touch()
    
    (tmp_path / "ignore_me").mkdir()
    
    (tmp_path / "script.py").touch()
    (tmp_path / "README.md").touch()
    
    return tmp_path

def test_build_project_structure(mock_project_structure):
    """Test that the project structure is correctly generated."""
    builder = ProjectStructureBuilder(str(mock_project_structure), ignore_patterns=["ignore_me"])
    result = builder.build()

    assert "folder1/" in result
    assert "file1.py" in result
    assert "README.md" in result
    assert "folder2/" in result
    assert "file2.txt" in result
    assert "script.py" in result
    assert "ignore_me/" not in result

def test_ignore_patterns(mock_project_structure):
    """Test that ignore patterns work correctly."""
    builder = ProjectStructureBuilder(str(mock_project_structure), ignore_patterns=["folder1", "file2.txt", "README.md"])
    result = builder.build()

    assert "folder1/" not in result
    assert "file1.py" not in result  # Fixed this assertion
    assert "folder2/" in result
    assert "file2.txt" not in result
    assert "README.md" not in result

def test_empty_directory(tmp_path):
    """Test that an empty directory is handled correctly."""
    builder = ProjectStructureBuilder(str(tmp_path))
    result = builder.build()

    assert result == f"{os.path.basename(tmp_path)}/\n"

def test_save_to_file(mock_project_structure, tmp_path):
    """Test that the structure can be saved to a file."""
    builder = ProjectStructureBuilder(str(mock_project_structure), ignore_patterns=["ignore_me"])
    output_file = tmp_path / "output.txt"
    builder.save_to_file(output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "folder1/" in content
    assert "file1.py" in content
    assert "folder2/" in content
    assert "file2.txt" in content
    assert "ignore_me/" not in content

def test_should_ignore():
    """Test the _should_ignore method."""
    builder = ProjectStructureBuilder("/test", ignore_patterns=["ignore_this"])
    
    assert builder._should_ignore("/test/ignore_this") is True
    assert builder._should_ignore("/test/not_ignored") is False

def test_custom_sort():
    """Test the _custom_sort function's sorting behavior."""
    builder = ProjectStructureBuilder("/test")
    
    files = ["README.md", "script.py", "notes.txt"]
    sorted_files = sorted(files, key=builder._custom_sort)

    assert sorted_files == ["notes.txt", "README.md", "script.py"]  # Fixed sorting order

def test_nested_directories(tmp_path):
    """Test that deeply nested directories are correctly structured."""
    (tmp_path / "parent").mkdir()
    (tmp_path / "parent" / "child").mkdir()
    (tmp_path / "parent" / "child" / "file.py").touch()
    
    builder = ProjectStructureBuilder(str(tmp_path))
    result = builder.build()

    assert "parent/" in result
    assert "child/" in result
    assert "file.py" in result