import argparse
import sys
from structure.builder import ProjectStructureBuilder

def main():
    """CLI entry point."""
    # ✅ Force UTF-8 encoding for printing (fix for Windows Unicode issue)
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Generate a project directory structure.")
    parser.add_argument("base_dir", help="Base directory to analyze.")
    parser.add_argument("--ignore", nargs="*", default=[], help="Files/folders to ignore.")
    parser.add_argument("--output", help="Optional file to save the output.")
    args = parser.parse_args()

    builder = ProjectStructureBuilder(args.base_dir, args.ignore)

    if args.output:
        builder.save_to_file(args.output)
    else:
        print(builder.build())

if __name__ == "__main__":
    main()
