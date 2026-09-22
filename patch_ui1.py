import re

with open("frontend/ui1.html", "r") as f:
    html = f.read()

# Add leaflet head tags
if "leaflet.css" not in html:
    html = html.replace('</head>', '  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>\n  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>\n</head>')

# Add map container
map_html = """
          <!-- Location Map -->
          <div class="card map-card">
            <div class="card-head">
              <h3>Location Map</h3>
            </div>
            <div id="ui1Map" style="height: 300px; border-radius: 8px; z-index: 1;"></div>
          </div>
"""
if "ui1Map" not in html:
    html = html.replace('<!-- Bottom row: table + AI predictor -->', map_html + '\n          <!-- Bottom row: table + AI predictor -->')

with open("frontend/ui1.html", "w") as f:
    f.write(html)
print("Patched ui1.html")
