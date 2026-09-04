with open("frontend/js/ui8.js", "r") as f:
    js = f.read()

import re

# Add an img tag to the monument Grid template for preview
new_grid = """
                <input type="file" id="file_${m.monument_id}" accept="image/*" capture="environment" style="display: none;" onchange="handleUpload('${m.monument_id}')">
                
                <img id="preview_${m.monument_id}" src="" style="display:none; width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem; border: 1px solid var(--border);" />
                
                <button onclick="document.getElementById('file_${m.monument_id}').click()" style="width: 100%; padding: 0.75rem; background: var(--brand); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
"""

js = js.replace("""<input type="file" id="file_${m.monument_id}" accept="image/*" capture="environment" style="display: none;" onchange="handleUpload('${m.monument_id}')">
                <button onclick="document.getElementById('file_${m.monument_id}').click()" style="width: 100%; padding: 0.75rem; background: var(--brand); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">""", new_grid)

# Update handleUpload to show preview
preview_logic = """
async function handleUpload(monumentId) {
    const fileInput = document.getElementById(`file_${monumentId}`);
    const file = fileInput.files[0];
    if(!file) return;
    
    // Show Preview
    const preview = document.getElementById(`preview_${monumentId}`);
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
"""

js = js.replace("""async function handleUpload(monumentId) {
    const fileInput = document.getElementById(`file_${monumentId}`);
    const file = fileInput.files[0];
    if(!file) return;""", preview_logic)

with open("frontend/js/ui8.js", "w") as f:
    f.write(js)
print("Preview added to ui8.js")
