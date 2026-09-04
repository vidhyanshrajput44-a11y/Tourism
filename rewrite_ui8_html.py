with open("frontend/ui8.html", "r") as f:
    ui8_content = f.read()

import re

# Extract everything between <main class="dashboard" ...> and </main>
main_match = re.search(r'(<main class="dashboard".*?</main>)', ui8_content, re.DOTALL)
if not main_match:
    print("Could not find main element!")
    exit(1)

main_content = main_match.group(1)

# Now, grab ui1.html to get the perfect header and footer layout
with open("frontend/ui1.html", "r") as f:
    ui1 = f.read()

header_match = re.search(r'(<!DOCTYPE html>.*?</nav>)', ui1, re.DOTALL)
footer_match = re.search(r'(<footer class="footer">.*?</html>)', ui1, re.DOTALL)

if header_match and footer_match:
    header = header_match.group(1)
    footer = footer_match.group(1)
    
    # 1. Title
    header = header.replace("<title>FootPrint — AI Crowd Intelligence</title>", "<title>FootPrint — Heritage Rewards</title>")
    
    # 2. Add Rewards nav link
    # Change active state
    header = header.replace('<a href="ui1.html" class="nav-link active">Crowd Intel</a>', '<a href="ui1.html" class="nav-link">Crowd Intel</a>')
    
    # Insert Rewards link
    header = header.replace('<button class="nav-link" id="navDestinations"', '<a href="ui8.html" class="nav-link active">Rewards</a>\n        <button class="nav-link" id="navDestinations"')
    
    # Change status label in header
    header = header.replace('<span class="status-label">Connecting…</span>', '<span class="status-label">REWARDS ENGINE · ONLINE</span>')
    header = header.replace('<span class="status-indicator"></span>', '<span class="status-indicator" style="background: #10b981;"></span>')
    
    # Replace footer JS script
    footer = footer.replace('src="js/app.js?v=2"', 'src="js/ui8.js?v=2"')
    footer = footer.replace('src="js/app.js"', 'src="js/ui8.js?v=2"')
    
    # Combine everything
    final_html = header + "\n\n  <div class=\"app-shell\">\n" + main_content + "\n  </div>\n\n" + footer
    
    with open("frontend/ui8.html", "w") as f:
        f.write(final_html)
        
    print("Rewritten ui8.html layout successfully.")
else:
    print("Failed to match header/footer in ui1.html")
