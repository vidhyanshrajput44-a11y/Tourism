import glob
import re

html_files = glob.glob("frontend/*.html")

old_pattern = r'<!-- Destinations removed -->'
new_replacement = '<button class="nav-link" id="navDestinations" style="display: none;">Destinations</button>'

for filepath in html_files:
    if "index.html" in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_content = content.replace(old_pattern, new_replacement)
    
    if content != updated_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Fixed {filepath}")
    else:
        print(f"Skipped {filepath}")

