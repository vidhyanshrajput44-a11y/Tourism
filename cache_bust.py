import glob
import re

html_files = glob.glob("frontend/*.html")

for filepath in html_files:
    with open(filepath, "r") as f:
        content = f.read()
    
    # Replace .js" with .js?v=2"
    # But only if it doesn't already have ?v=...
    updated = re.sub(r'\.js"', r'.js?v=2"', content)
    updated = re.sub(r'\.js\?v=\d+"\?v=\d+', r'.js?v=3', updated) # just in case
    
    if updated != content:
        with open(filepath, "w") as f:
            f.write(updated)
        print(f"Cache busted {filepath}")

