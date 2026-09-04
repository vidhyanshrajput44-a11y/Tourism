import glob
for fpath in glob.glob("frontend/ui*.html"):
    with open(fpath, "r") as f: content = f.read()
    if 'js/auth-guard.js' not in content:
        content = content.replace('</head>', '  <script src="js/auth-guard.js"></script>\n</head>')
        with open(fpath, "w") as f: f.write(content)
