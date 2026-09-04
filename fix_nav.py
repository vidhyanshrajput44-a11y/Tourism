import glob
import re

html_files = glob.glob("frontend/*.html")

old_pattern = r'<button class="nav-link" id="navDestinations">Destinations</button>\s*<button class="nav-link" onclick="localStorage\.removeItem\(\'footprint_session\'\); window\.location\.href=\'index\.html\';" style="color: #dc2626; border: 1px solid #dc2626; margin-left: 0;">Logout</button>'

new_replacement = """<!-- Destinations removed -->
        <div style="position: relative; margin-left: 0;">
          <button class="nav-link" onclick="const m = document.getElementById('profileMenu'); m.style.display = (m.style.display === 'none' || m.style.display === '') ? 'block' : 'none';" style="display: flex; align-items: center; gap: 0.5rem; background: white; border: 1px solid #e2e8f0; border-radius: 999px; padding: 0.35rem 0.75rem; cursor: pointer; color: #0f172a;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span style="font-size: 0.9rem; font-weight: 500;">Profile</span>
          </button>
          <div id="profileMenu" style="display: none; position: absolute; right: 0; top: calc(100% + 0.5rem); background: white; border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); min-width: 120px; z-index: 100;">
            <button onclick="localStorage.removeItem('footprint_session'); window.location.href='index.html';" style="width: 100%; text-align: left; padding: 0.75rem 1rem; background: none; border: none; border-radius: 8px; color: #dc2626; cursor: pointer; font-size: 0.9rem; font-weight: 500;">Logout</button>
          </div>
        </div>"""

for filepath in html_files:
    if "index.html" in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_content = re.sub(old_pattern, new_replacement, content, flags=re.MULTILINE)
    
    if content != updated_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Updated {filepath}")
    else:
        print(f"Pattern not found in {filepath} or already updated.")

