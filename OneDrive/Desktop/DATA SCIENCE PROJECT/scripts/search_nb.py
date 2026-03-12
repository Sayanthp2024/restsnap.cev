import json
import os
import glob

def search_notebooks():
    files = glob.glob("**/*.ipynb", recursive=True)
    for file in files:
        print(f"Checking {file}...")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                nb = json.load(f)
            for i, cell in enumerate(nb.get('cells', [])):
                if cell.get('cell_type') == 'code':
                    source = "".join(cell.get('source', []))
                    if "'''" in source or '"""' in source:
                        print(f"  Found in cell {i+1} of {file}")
                        print("  Source snippet:")
                        print(source[:200])
                        print("-" * 20)
        except Exception as e:
            print(f"  Error reading {file}: {e}")

if __name__ == "__main__":
    search_notebooks()
