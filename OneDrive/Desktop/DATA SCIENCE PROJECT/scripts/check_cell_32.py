import json
import os

path = r"notebooks/datapreprocessing.ipynb"

try:
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print(f"Total cells: {len(nb['cells'])}")
    if len(nb['cells']) >= 32:
        print("--- Cell 32 ---")
        print("".join(nb['cells'][31]['source']))
    else:
        print("Cell 32 not found in datapreprocessing.ipynb")
except Exception as e:
    print(f"Error: {e}")
