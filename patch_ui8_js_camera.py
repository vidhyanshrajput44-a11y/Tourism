with open("frontend/js/ui8.js", "r") as f:
    js = f.read()

# Fix CSS vars in JS
js = js.replace('var(--brand)', 'var(--accent-dark)')
js = js.replace('var(--text-main)', 'var(--text-primary)')

# Replace the tab logic to properly handle color transitions
tab_old = """            document.getElementById(`tab${t}`).style.color = "var(--text-main)";
            document.getElementById(`tab${t}`).style.borderBottom = "2px solid var(--brand)";"""
tab_new = """            document.getElementById(`tab${t}`).style.color = "var(--text-primary)";
            document.getElementById(`tab${t}`).style.borderBottom = "3px solid var(--accent-dark)";"""
js = js.replace(tab_old, tab_new)

tab_off_old = """            document.getElementById(`tab${x}`).style.color = "var(--text-muted)";
            document.getElementById(`tab${x}`).style.borderBottom = "none";"""
tab_off_new = """            document.getElementById(`tab${x}`).style.color = "var(--text-secondary)";
            document.getElementById(`tab${x}`).style.borderBottom = "none";"""
js = js.replace(tab_off_old, tab_off_new)

# Add camera JS logic at the bottom
camera_js = """
// Live Camera Logic
let currentStream = null;
let targetMonumentId = null;

async function openCamera(monumentId, monumentName) {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        // Fallback to traditional file picker
        document.getElementById(`file_${monumentId}`).click();
        return;
    }
    
    targetMonumentId = monumentId;
    const modal = document.getElementById("cameraModal");
    const video = document.getElementById("liveVideo");
    document.getElementById("cameraTitle").textContent = `Capture ${monumentName}`;
    
    try {
        currentStream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: "environment" },
            audio: false 
        });
        video.srcObject = currentStream;
        modal.style.display = "flex";
    } catch(err) {
        console.error("Camera access denied or failed:", err);
        // Fallback
        document.getElementById(`file_${monumentId}`).click();
    }
}

function closeCamera() {
    document.getElementById("cameraModal").style.display = "none";
    if (currentStream) {
        currentStream.getTracks().forEach(t => t.stop());
        currentStream = null;
    }
}

// Add event listener to capture button
document.addEventListener("DOMContentLoaded", () => {
    const btnCapture = document.getElementById("btnCapture");
    if(btnCapture) {
        btnCapture.addEventListener("click", () => {
            if(!currentStream || !targetMonumentId) return;
            
            // Visual feedback
            btnCapture.style.transform = "scale(0.9)";
            setTimeout(() => btnCapture.style.transform = "none", 150);
            
            const video = document.getElementById("liveVideo");
            const canvas = document.getElementById("cameraCanvas");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            closeCamera();
            
            canvas.toBlob((blob) => {
                const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
                processUpload(targetMonumentId, file);
            }, "image/jpeg", 0.9);
        });
    }
});

async function processUpload(monumentId, file) {
    const resDiv = document.getElementById(`res_${monumentId}`);
    resDiv.style.display = "block";
    resDiv.style.background = "#f1f5f9";
    resDiv.style.color = "var(--text-primary)";
    resDiv.textContent = "Verifying photo with AI...";
    
    // Show Preview
    const preview = document.getElementById(`preview_${monumentId}`);
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
    
    const formData = new FormData();
    formData.append("user_id", currentUserId);
    formData.append("monument_id", monumentId);
    formData.append("destination_id", currentDestId);
    formData.append("force_verify", "true"); // Always force for reliable demos
    formData.append("image", file);
    
    try {
        const res = await fetch(`${API_BASE}/rewards/submit-photo`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        
        if(res.ok && data.status === "verified") {
            resDiv.style.background = "#dcfce7";
            resDiv.style.color = "#15803d";
            resDiv.innerHTML = `✅ Verified! <b>+${data.points_awarded} pts</b><br><small style="opacity:0.8">${data.verification_reason}</small>`;
        } else {
            resDiv.style.background = "#fef3c7";
            resDiv.style.color = "#b45309";
            resDiv.innerHTML = `⏳ Pending Review.<br><small style="opacity:0.8">${data.verification_reason || 'Could not auto-verify.'}</small>`;
        }
    } catch(err) {
        resDiv.style.background = "#fee2e2";
        resDiv.style.color = "#b91c1c";
        resDiv.textContent = `❌ Error: ${err.message}`;
    }
}
"""

js += "\n" + camera_js

# Now replace the old grid button logic to call openCamera
old_btn = """<button onclick="document.getElementById('file_${m.monument_id}').click()" style="width: 100%; padding: 0.75rem; background: var(--accent-dark); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">"""
new_btn = """<button onclick="openCamera('${m.monument_id}', '${m.name.replace("'", "\\'")}')" style="width: 100%; padding: 0.75rem; background: var(--accent-dark); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">"""
js = js.replace(old_btn, new_btn)

# Redirect old handleUpload to just call processUpload (for file picker fallback)
old_handle = """async function handleUpload(monumentId) {
    const fileInput = document.getElementById(`file_${monumentId}`);
    const file = fileInput.files[0];
    if(!file) return;
    
    // Show Preview
    const preview = document.getElementById(`preview_${monumentId}`);
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
    
    const resDiv = document.getElementById(`res_${monumentId}`);
    resDiv.style.display = "block";
    resDiv.style.background = "#f1f5f9";
    resDiv.style.color = "var(--text-primary)";
    resDiv.textContent = "Verifying photo with AI...";
    
    const formData = new FormData();
    formData.append("user_id", currentUserId);
    formData.append("monument_id", monumentId);
    formData.append("destination_id", currentDestId);
    formData.append("force_verify", "true"); // Always force for reliable demos
    formData.append("image", file);
    
    try {
        const res = await fetch(`${API_BASE}/rewards/submit-photo`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        
        if(res.ok && data.status === "verified") {
            resDiv.style.background = "#dcfce7";
            resDiv.style.color = "#15803d";
            resDiv.innerHTML = `✅ Verified! <b>+${data.points_awarded} pts</b><br><small style="opacity:0.8">${data.verification_reason}</small>`;
        } else {
            resDiv.style.background = "#fef3c7";
            resDiv.style.color = "#b45309";
            resDiv.innerHTML = `⏳ Pending Review.<br><small style="opacity:0.8">${data.verification_reason || 'Could not auto-verify.'}</small>`;
        }
    } catch(err) {
        resDiv.style.background = "#fee2e2";
        resDiv.style.color = "#b91c1c";
        resDiv.textContent = `❌ Error: ${err.message}`;
    }
}"""

new_handle = """async function handleUpload(monumentId) {
    const fileInput = document.getElementById(`file_${monumentId}`);
    const file = fileInput.files[0];
    if(!file) return;
    processUpload(monumentId, file);
}"""

js = js.replace(old_handle, new_handle)

with open("frontend/js/ui8.js", "w") as f:
    f.write(js)
print("ui8.js updated with camera JS")
