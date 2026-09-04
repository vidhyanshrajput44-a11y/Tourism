import re

with open("frontend/hub.html", "r") as f:
    html = f.read()

new_card = """
      <!-- UI 8 -->
      <a href="ui8.html" class="hub-card">
        <div class="hub-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
        </div>
        <h3 class="hub-title">Heritage Rewards & Bookings</h3>
        <p class="hub-desc">Verify monument photos to earn reward points and redeem hotel discounts.</p>
        <div class="hub-btn">Open Module <span>→</span></div>
      </a>

    </div>
"""

# Replace the closing tag of the grid with the new card + closing tag
html = re.sub(r'    </div>\s*</main>', new_card + '    </main>', html)

with open("frontend/hub.html", "w") as f:
    f.write(html)

print("Patched hub.html")
