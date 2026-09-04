import glob
import re

html_files = glob.glob("frontend/ui*.html")

for filepath in html_files:
    if "ui8.html" in filepath:
        continue # ui8 already has it correctly set up as active
        
    with open(filepath, "r") as f:
        content = f.read()
    
    # Check if it already has the Rewards link
    if 'href="ui8.html"' in content:
        continue
        
    # Inject before the Destinations button
    target = '<button class="nav-link" id="navDestinations"'
    replacement = '<a href="ui8.html" class="nav-link">Rewards</a>\n        <button class="nav-link" id="navDestinations"'
    
    updated = content.replace(target, replacement)
    
    if updated != content:
        with open(filepath, "w") as f:
            f.write(updated)
        print(f"Added Rewards link to {filepath}")

