import glob
import re

for filepath in glob.glob("frontend/ui*.html"):
    with open(filepath, "r") as f:
        content = f.read()

    # Find the nav-links div and add the logout button right after "Destinations"
    pattern = r'(<button class="nav-link" id="navDestinations">Destinations</button>)'
    replacement = r'\1\n        <button class="nav-link" onclick="localStorage.removeItem(\'footprint_session\'); window.location.href=\'index.html\';" style="color: #dc2626; border: 1px solid #dc2626; margin-left: auto;">Logout</button>'
    
    new_content = re.sub(pattern, replacement, content)
    
    with open(filepath, "w") as f:
        f.write(new_content)

print("Logout button added to all UIs.")
