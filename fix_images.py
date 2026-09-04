import glob

js_files = glob.glob("frontend/js/*.js")

old_str = "if (!meta) return \"\";"
new_str = "if (!meta) return `https://picsum.photos/seed/${destId}/${width}/${height}`;"

for filepath in js_files:
    with open(filepath, "r") as f:
        content = f.read()
    
    updated = content.replace(old_str, new_str)
    
    if updated != content:
        with open(filepath, "w") as f:
            f.write(updated)
        print(f"Fixed {filepath}")
