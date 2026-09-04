with open("frontend/ui7.html", "r") as f:
    ui7 = f.read()

# Extract the <head> ... <nav class="topnav">...</nav> part
import re

header_match = re.search(r'(<!DOCTYPE html>.*?</nav>)', ui7, re.DOTALL)
if header_match:
    header = header_match.group(1)
    
    # Update active link to Rewards
    header = header.replace('<a href="ui7.html" class="nav-link active">Ask FootPrint</a>', '<a href="ui7.html" class="nav-link">Ask FootPrint</a>')
    
    # Add Rewards link before the profile button
    header = header.replace('<button class="nav-link" id="navDestinations" style="display: none;">Destinations</button>', '<a href="ui8.html" class="nav-link active">Rewards</a>\n        <button class="nav-link" id="navDestinations" style="display: none;">Destinations</button>')
    
    # Update title
    header = header.replace('<title>FootPrint — AI Crowd Intelligence</title>', '<title>FootPrint — Heritage Rewards</title>')
    
    # Update status indicator text if there is one in header...
    # ui7 status is handled by JS.
    
    # Read the rest of ui8
    with open("frontend/ui8.html", "r") as f:
        ui8 = f.read()
        
    main_content_match = re.search(r'(<main class="dashboard".*</body>)', ui8, re.DOTALL)
    if main_content_match:
        main_content = main_content_match.group(1)
        
        with open("frontend/ui8.html", "w") as f:
            f.write(header + "\n  <!-- Status bar like ui7 -->\n  <div class=" + '"nav-status" id="apiStatus" style="position:absolute; right:1.5rem; top:1.2rem; font-size: 0.75rem; display:flex; align-items:center; gap:0.5rem;"><span class="status-indicator" style="background:#10b981; width:8px; height:8px; border-radius:50%; display:inline-block;"></span><span class="status-label" style="color:#64748b; letter-spacing:0.05em; text-transform:uppercase;">REWARDS ENGINE · ONLINE</span></div>\n' + main_content)
        print("Fixed ui8.html header")
