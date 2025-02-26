# Print Directory Structure

A Python tool to visualize and export the directory structure of a given project.

## Features
✔️ Recursively scans directories  
✔️ Supports ignoring specific files/folders  
✔️ Outputs structure as text  
✔️ Option to save output to a file  

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/PrintDirectoryStructure.git
   cd PrintDirectoryStructure
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To generate the directory structure:
```sh
python src/main.py /path/to/your/project
```

### **Ignore Specific Files or Folders**
```sh
python src/main.py /path/to/project --ignore __pycache__ .git node_modules
```

### **Save Output to a File**
```sh
python src/main.py /path/to/project --output structure.txt
```

## Testing

To run unit tests:
```sh
pytest tests/
```

## Contributing
Feel free to fork and submit pull requests! 🚀

