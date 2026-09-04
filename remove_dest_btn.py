import glob
import re

for filepath in glob.glob("frontend/*.html"):
    with open(filepath, "r") as f:
        content = f.read()

    # Remove the Destinations button from the nav links block
    # Note: spacing might vary, so let's use a regex
    new_content = re.sub(r'\s*<button class="nav-link" id="navDestinations">Destinations</button>', '', content)
    
    with open(filepath, "w") as f:
        f.write(new_content)

print("Destinations button removed from all HTML files.")
