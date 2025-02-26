import os

class ProjectStructureBuilder:
    """Handles project directory scanning and structure generation."""

    def __init__(self, base_dir, ignore_patterns=None):
        self.base_dir = base_dir
        self.ignore_patterns = ignore_patterns or []
    
    def _should_ignore(self, path):
        """Check if a file/folder should be ignored based on exact matches or directory names."""
        base_name = os.path.basename(path)
        return base_name in self.ignore_patterns

    
    def _get_structure(self, directory, indent_level=0):
        """Recursively generate the directory structure."""
        structure = ""
        entries = os.listdir(directory)
        
        dirs = sorted([e for e in entries if os.path.isdir(os.path.join(directory, e))])
        files = sorted([e for e in entries if os.path.isfile(os.path.join(directory, e))], key=self._custom_sort)


        for entry in dirs + files:
            if self._should_ignore(os.path.join(directory, entry)):
                continue

            path = os.path.join(directory, entry)
            indent = "│   " * indent_level

            if os.path.isdir(path):
                structure += f"{indent}├── {entry}/\n"
                structure += self._get_structure(path, indent_level + 1)
            else:
                structure += f"{indent}├── {entry}\n"

        return structure    

    def _custom_sort(self, entry):
        """Sort files and folders naturally, case-insensitive."""
        return entry.lower()


    def build(self):
        """Build the directory structure."""
        return f"{os.path.basename(self.base_dir)}/\n" + self._get_structure(self.base_dir)

    def save_to_file(self, output_file):
        """Save the directory structure to a file."""
        structure = self.build()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(structure)
        print(f"Project structure written to: {output_file}")
