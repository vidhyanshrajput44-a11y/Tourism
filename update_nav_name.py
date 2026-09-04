import glob
import re

for filepath in glob.glob("frontend/ui*.html"):
    with open(filepath, "r") as f:
        content = f.read()

    # Find the Logout button and insert the userName span right before it, 
    # but only if it's not already there.
    if 'id="navUserName"' not in content:
        pattern = r'(<button class="nav-link" onclick="localStorage\.removeItem\(\'footprint_session\'\);)'
        replacement = r'<span id="navUserName" style="margin-left: auto; font-size: 0.9rem; color: var(--text-secondary); margin-right: 1rem;"></span>\n        \1'
        new_content = re.sub(pattern, replacement, content)
        
        # also remove margin-left: auto from the logout button since it's now on the span
        new_content = new_content.replace('margin-left: auto;"', 'margin-left: 0;"')
        
        with open(filepath, "w") as f:
            f.write(new_content)

print("Username span added to all UIs.")
