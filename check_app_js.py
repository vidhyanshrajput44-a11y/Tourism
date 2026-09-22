with open('frontend/js/app.js', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'document.getElementById' in line and i > 400:
        print(f"Line {i+1}: {line.strip()}")
