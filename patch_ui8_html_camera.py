with open("frontend/ui8.html", "r") as f:
    html = f.read()

camera_modal = """
  <!-- Live Camera Modal -->
  <div id="cameraModal" style="display: none; position: fixed; inset: 0; background: black; z-index: 9999; flex-direction: column;">
    <div style="padding: 1.5rem; display: flex; justify-content: space-between; align-items: center; background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent); color: white; position: absolute; top: 0; left: 0; right: 0; z-index: 10;">
        <h3 id="cameraTitle" style="font-size: 1.2rem; font-weight: 500;">Capture Monument</h3>
        <button onclick="closeCamera()" style="background: rgba(255,255,255,0.2); border: none; color: white; width: 36px; height: 36px; border-radius: 50%; font-size: 1.2rem; cursor: pointer;">×</button>
    </div>
    
    <div style="flex: 1; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden;">
        <video id="liveVideo" autoplay playsinline style="width: 100%; height: 100%; object-fit: cover;"></video>
        <!-- Scanner Overlay -->
        <div style="position: absolute; inset: 15%; border: 2px dashed rgba(255,255,255,0.5); border-radius: 12px; pointer-events: none;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: rgba(255,255,255,0.7); font-size: 0.9rem; text-align: center;">Align monument<br>within frame</div>
        </div>
    </div>
    
    <div style="padding: 2rem; background: black; display: flex; justify-content: center; align-items: center;">
        <button id="btnCapture" style="width: 72px; height: 72px; border-radius: 50%; background: white; border: 4px solid #cbd5e1; cursor: pointer; outline: 4px solid white; outline-offset: 2px; transition: transform 0.1s;"></button>
    </div>
    <canvas id="cameraCanvas" style="display: none;"></canvas>
  </div>
"""

# Insert modal right before </body>
html = html.replace('</body>', camera_modal + '\n</body>')

# Fix UI issues: change var(--brand) to var(--accent-dark)
html = html.replace('var(--brand)', 'var(--accent-dark)')
html = html.replace('var(--text-main)', 'var(--text-primary)') # standard is primary

# Improve tab styling visibility
html = html.replace('id="tabPoints" style="padding: 1rem; background: transparent; border: none; font-weight: 600; cursor: pointer; color: var(--text-muted);"', 'id="tabPoints" style="padding: 1rem; background: transparent; border: none; font-weight: 600; cursor: pointer; color: var(--text-secondary); font-size: 1.05rem;"')
html = html.replace('id="tabRedeem" style="padding: 1rem; background: transparent; border: none; font-weight: 600; cursor: pointer; color: var(--text-muted);"', 'id="tabRedeem" style="padding: 1rem; background: transparent; border: none; font-weight: 600; cursor: pointer; color: var(--text-secondary); font-size: 1.05rem;"')
html = html.replace('id="tabUpload" style="padding: 1rem; background: transparent; border: none; font-weight: 600; cursor: pointer; border-bottom: 2px solid var(--brand);"', 'id="tabUpload" style="padding: 1rem; background: transparent; border: none; font-weight: 600; cursor: pointer; border-bottom: 3px solid var(--accent-dark); color: var(--text-primary); font-size: 1.05rem;"')

with open("frontend/ui8.html", "w") as f:
    f.write(html)
print("ui8.html updated with camera modal and styling")
