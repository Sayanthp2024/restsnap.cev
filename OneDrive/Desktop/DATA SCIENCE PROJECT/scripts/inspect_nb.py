import json
import os

import sys

if len(sys.argv) < 2:
    print("Usage: python scripts/inspect_nb.py <notebook_path> [cell_number]")
    sys.exit(1)

path = sys.argv[1]
cell_no = int(sys.argv[2]) if len(sys.argv) > 2 else None

if not os.path.exists(path):
    print(f"File not found: {path}")
else:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        print(f"Total cells: {len(nb['cells'])}")
        
        if cell_no:
            if 0 < cell_no <= len(nb['cells']):
                print(f"--- Cell {cell_no} ---")
                print("".join(nb['cells'][cell_no-1]['source']))
            else:
                print(f"Cell {cell_no} out of range.")
        else:
            # Show 13 and 20 by default for backward compatibility or useful context
            for c in [13, 20, 32]:
                if len(nb['cells']) >= c:
                    print(f"--- Cell {c} ---")
                    print("".join(nb['cells'][c-1]['source']))
            
    except Exception as e:
        print(f"Error: {e}")
