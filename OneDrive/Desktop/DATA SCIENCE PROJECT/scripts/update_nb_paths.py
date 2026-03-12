import json
import os
import glob

def update_notebook_paths():
    notebooks = glob.glob("notebooks/*.ipynb")
    for nb_path in notebooks:
        print(f"Updating {nb_path}...")
        try:
            with open(nb_path, 'r', encoding='utf-8') as f:
                nb = json.load(f)
            
            modified = False
            for cell in nb.get('cells', []):
                if cell.get('cell_type') == 'code':
                    new_source = []
                    for line in cell.get('source', []):
                        # Replace absolute path with relative path
                        new_line = line.replace(r"C:\Users\sayxp\OneDrive\Desktop\DATA SCIENCE PROJECT\Restaurant_Reviews", r"../data/Restaurant_Reviews")
                        # Also handle local case if they were relative but in same dir
                        if "Restaurant_Reviews" in new_line and "../data/" not in new_line and "models/" not in new_line:
                            import re
                            # If it's just the filename, prepend ../data/
                            new_line = re.sub(r'([\'"])(Restaurant_Reviews\.(csv|tsv))([\'"])', r'\1../data/\2\4', new_line)
                        
                        if new_line != line:
                            modified = True
                        new_source.append(new_line)
                    cell['source'] = new_source
            
            if modified:
                with open(nb_path, 'w', encoding='utf-8') as f:
                    json.dump(nb, f, indent=1)
                print(f"  Successfully updated {nb_path}")
            else:
                print(f"  No changes needed in {nb_path}")
                
        except Exception as e:
            print(f"  Error updating {nb_path}: {e}")

if __name__ == "__main__":
    update_notebook_paths()
