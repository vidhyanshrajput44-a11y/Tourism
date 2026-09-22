with open("frontend/ui1.html", "r") as f:
    html = f.read()

html = html.replace('<div class="card map-card">', '<div class="card map-card" hidden>')

with open("frontend/ui1.html", "w") as f:
    f.write(html)
