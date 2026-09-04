import glob
import re

nav_html = """      <div class="nav-links">
        <a href="index.html" class="nav-link{index}">Crowd Intel</a>
        <a href="ui2.html" class="nav-link{ui2}">Recommendations</a>
        <a href="ui3.html" class="nav-link{ui3}">Smart Safety</a>
        <a href="ui4.html" class="nav-link{ui4}">Local Market</a>
        <a href="ui5.html" class="nav-link{ui5}">Gov Dashboard</a>
        <a href="ui6.html" class="nav-link{ui6}">Hotels & Transport</a>
        <a href="ui7.html" class="nav-link{ui7}">Ask FootPrint</a>
        <button class="nav-link" id="navDestinations">Destinations</button>
      </div>"""

for filepath in glob.glob("frontend/*.html"):
    with open(filepath, "r") as f:
        content = f.read()

    active = {
        "index": "", "ui2": "", "ui3": "", "ui4": "", 
        "ui5": "", "ui6": "", "ui7": ""
    }
    
    if "index.html" in filepath: active["index"] = " active"
    elif "ui2.html" in filepath: active["ui2"] = " active"
    elif "ui3.html" in filepath: active["ui3"] = " active"
    elif "ui4.html" in filepath: active["ui4"] = " active"
    elif "ui5.html" in filepath: active["ui5"] = " active"
    elif "ui6.html" in filepath: active["ui6"] = " active"
    elif "ui7.html" in filepath: active["ui7"] = " active"

    new_nav = nav_html.format(**active)
    pattern = re.compile(r'      <div class="nav-links">.*?      </div>', re.DOTALL)
    new_content = pattern.sub(new_nav, content)
    
    with open(filepath, "w") as f:
        f.write(new_content)

print("Nav updated perfectly.")
