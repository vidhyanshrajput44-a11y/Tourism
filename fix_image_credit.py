import glob

js_files = glob.glob("frontend/js/*.js")

# Find imageCreditHtml function and replace its internal logic safely.
import re

for filepath in js_files:
    with open(filepath, "r") as f:
        content = f.read()
    
    # regex to find the incorrect line inside imageCreditHtml
    # function imageCreditHtml(destId) {
    #   const meta = DEST_IMAGES[destId];
    #   if (!meta) return `https://picsum.photos/seed/${destId}/${width}/${height}`;
    
    pattern = r'(function imageCreditHtml\(destId\) \{\s*const meta = DEST_IMAGES\[destId\];\s*)if \(!meta\) return `https://picsum\.photos/seed/\$\{destId\}/\$\{width\}/\$\{height\}`;'
    updated = re.sub(pattern, r'\1if (!meta) return "";', content)
    
    if updated != content:
        with open(filepath, "w") as f:
            f.write(updated)
        print(f"Fixed {filepath}")
