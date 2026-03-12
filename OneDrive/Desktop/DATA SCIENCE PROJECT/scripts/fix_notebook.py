import json
import os

path = r"C:\Users\sayxp\OneDrive\Desktop\DATA SCIENCE PROJECT\datamunging.ipynb"

if not os.path.exists(path):
    print(f"File not found: {path}")
    exit(1)

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 3 is index 1 or 2? 
# In the view_file:
# Cell 1 (index 0): Conversion done! (import csv)
# Cell 2 (index 1): pandas import (which failed)
# Cell 3 (index 2): %pip install pandas
# Cell 4 (index 3): pandas import (which succeeded)
# Cell 5 (index 4): data munging

# Fix cell 3 (index 2) - commenting out %pip
nb['cells'][2]['source'] = ["# %pip install pandas\n"]

# Fix cell 5 (index 4) - refactoring data loading
nb['cells'][4]['source'] = [
    "# code for data munging and analysis\n",
    "import pandas as pd\n",
    "path = r\"C:\\Users\\sayxp\\OneDrive\\Desktop\\DATA SCIENCE PROJECT\\Restaurant_Reviews.csv\"\n",
    "data = pd.read_csv(path)\n",
    "data.head(100)"
]

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated successfully.")
