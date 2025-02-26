import subprocess

def test_main_script_execution():
    """Test that the main script runs without errors."""
    result = subprocess.run(
        ["python", "src/main.py", "tests"], 
        capture_output=True, 
        text=True, 
        encoding="utf-8"  # ✅ Force UTF-8 encoding to avoid UnicodeEncodeError
    )
    
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    assert result.returncode == 0  # Ensure script runs successfully
