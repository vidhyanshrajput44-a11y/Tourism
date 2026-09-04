import glob

for filepath in glob.glob("frontend/ui*.html"):
    with open(filepath, "r") as f:
        content = f.read()

    # Replace backslashes
    content = content.replace("localStorage.removeItem(\\'footprint_session\\');", "localStorage.removeItem('footprint_session');")
    content = content.replace("window.location.href=\\'index.html\\';", "window.location.href='index.html';")
    
    with open(filepath, "w") as f:
        f.write(content)

print("Logout fixed.")
