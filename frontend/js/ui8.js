const API_BASE = window.location.origin.includes("8000")
  ? window.location.origin
  : "http://127.0.0.1:8000";

let currentUserId = "demo_user";
let currentDestId = "";
let currentDiscount = null;

// Initialization
document.addEventListener("DOMContentLoaded", async () => {
    // Attempt to get user from Auth
    const token = localStorage.getItem("footprint_session");
    if (token) {
        try {
            const parsed = JSON.parse(atob(token));
            currentUserId = parsed.phone || "demo_user";
            document.getElementById("profilePhone").textContent = currentUserId;
        } catch (e) {}
    }
    
    bindTabs();
    await loadDestinations();
    
    document.getElementById("destSelect").addEventListener("change", (e) => {
        currentDestId = e.target.value;
        if(currentDestId) {
            loadMonuments(currentDestId);
        } else {
            document.getElementById("monumentGrid").innerHTML = '<div style="color: var(--text-muted);">Select a destination to view monuments.</div>';
        }
    });
    
    document.getElementById("btnMock").addEventListener("click", doMockBooking);
});

// API Helpers
async function apiGet(path) {
    const res = await fetch(`${API_BASE}${path}`);
    if (!res.ok) throw new Error((await res.json()).detail || "Request failed");
    return res.json();
}

async function apiPost(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Request failed");
    return res.json();
}

// Tab Logic
function bindTabs() {
    const tabs = ["Upload", "Points", "Redeem"];
    tabs.forEach(t => {
        document.getElementById(`tab${t}`).addEventListener("click", () => {
            tabs.forEach(x => {
                document.getElementById(`tab${x}`).classList.remove("active");
                document.getElementById(`tab${x}`).style.color = "var(--text-muted)";
                document.getElementById(`tab${x}`).style.borderBottom = "none";
                document.getElementById(`sec${x}`).style.display = "none";
            });
            document.getElementById(`tab${t}`).classList.add("active");
            document.getElementById(`tab${t}`).style.color = "var(--text-primary)";
            document.getElementById(`tab${t}`).style.borderBottom = "2px solid var(--accent-dark)";
            document.getElementById(`sec${t}`).style.display = "block";
            
            if (t === "Points") loadPoints();
            if (t === "Redeem") loadRedeem();
        });
    });
}

// Section 1: Upload
async function loadDestinations() {
    try {
        const dests = await apiGet("/destinations");
        const sel = document.getElementById("destSelect");
        dests.forEach(d => {
            const opt = document.createElement("option");
            opt.value = d.destination_id;
            opt.textContent = `${d.name} (${d.city})`;
            sel.appendChild(opt);
        });
    } catch(err) {
        console.error(err);
    }
}

async function loadMonuments(destId) {
    const grid = document.getElementById("monumentGrid");
    grid.innerHTML = '<div class="loading-state">Loading monuments...</div>';
    try {
        const monuments = await apiGet(`/rewards/monuments/${destId}`);
        if(monuments.length === 0) {
            grid.innerHTML = '<div style="color: var(--text-muted);">No monuments available here yet.</div>';
            return;
        }
        
        grid.innerHTML = monuments.map(m => `
            <div style="background: white; border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; display: flex; flex-direction: column;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <h3 style="font-size: 1.1rem; color: var(--text-primary);">${m.name}</h3>
                    <span style="background: #fef3c7; color: #b45309; padding: 0.2rem 0.6rem; border-radius: 999px; font-weight: bold; font-size: 0.8rem;">${m.points_value} pts</span>
                </div>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem; flex-grow: 1;">${m.description}</p>
                
                
                <input type="file" id="file_${m.monument_id}" accept="image/*" capture="environment" style="display: none;" onchange="handleUpload('${m.monument_id}')">
                
                <img id="preview_${m.monument_id}" src="" style="display:none; width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem; border: 1px solid var(--border);" />
                
                <button onclick="openCamera('${m.monument_id}', '${m.name.replace("'", "\'")}')" style="width: 100%; padding: 0.75rem; background: var(--accent-dark); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">

                    📸 Take Photo
                </button>
                <div id="res_${m.monument_id}" style="margin-top: 1rem; display: none; font-size: 0.9rem; padding: 0.75rem; border-radius: 6px;"></div>
            </div>
        `).join("");
    } catch(err) {
        grid.innerHTML = `<div style="color: red;">Error: ${err.message}</div>`;
    }
}


async function handleUpload(monumentId) {
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
}

// Section 2: Points
async function loadPoints() {
    try {
        const data = await apiGet(`/rewards/my-points/${currentUserId}`);
        document.getElementById("ptBalance").textContent = data.ledger.current_balance;
        document.getElementById("ptTotal").textContent = `Total Earned: ${data.ledger.total_points} pts`;
        
        const hl = document.getElementById("historyList");
        if(data.history.length === 0) {
            hl.innerHTML = "<div style='color: var(--text-muted);'>No submissions yet.</div>";
            return;
        }
        
        hl.innerHTML = data.history.map(h => `
            <div style="display: flex; justify-content: space-between; padding: 1rem; background: white; border: 1px solid var(--border); border-radius: 8px;">
                <div>
                    <div style="font-weight: 600; color: var(--text-primary);">${h.monument_name}</div>
                    <div style="font-size: 0.8rem; color: var(--text-muted);">${new Date(h.timestamp).toLocaleString()}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: bold; color: ${h.status === 'verified' ? '#15803d' : '#b45309'};">${h.status === 'verified' ? '+'+h.points_awarded : 'Pending'}</div>
                </div>
            </div>
        `).join("");
    } catch(err) {
        console.error(err);
    }
}

// Section 3: Redeem
async function loadRedeem() {
    const grid = document.getElementById("redeemGrid");
    grid.innerHTML = '<div class="loading-state">Loading rewards...</div>';
    try {
        const tiers = await apiGet(`/rewards/available-tiers/${currentUserId}`);
        
        grid.innerHTML = tiers.map(t => `
            <div style="background: white; border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 2rem; font-weight: 800; color: var(--accent-dark); margin-bottom: 0.5rem;">${t.discount_pct}% OFF</div>
                <div style="color: var(--text-secondary); margin-bottom: 1.5rem;">Hotel Bookings</div>
                <button 
                    onclick="doRedeem('${t.tier_id}')" 
                    ${!t.is_eligible ? 'disabled' : ''}
                    style="width: 100%; padding: 0.75rem; background: ${t.is_eligible ? 'var(--accent-dark)' : '#e2e8f0'}; color: ${t.is_eligible ? 'white' : '#94a3b8'}; border: none; border-radius: 8px; font-weight: 600; cursor: ${t.is_eligible ? 'pointer' : 'not-allowed'};">
                    ${t.is_eligible ? `Redeem (${t.points_required} pts)` : `Need ${t.points_required} pts`}
                </button>
            </div>
        `).join("");
    } catch(err) {
        grid.innerHTML = `<div style="color: red;">Error: ${err.message}</div>`;
    }
}

async function doRedeem(tierId) {
    try {
        const res = await apiPost("/rewards/redeem", { user_id: currentUserId, tier_id: tierId });
        currentDiscount = res;
        
        document.getElementById("activeCode").textContent = res.discount_code;
        document.getElementById("bookingActions").style.display = "block";
        document.getElementById("mockConfirmation").style.display = "none";
        
        // Setup MMT Link
        const destId = currentDestId || "taj_mahal"; // fallback if they haven't selected one
        const mmtRes = await apiGet(`/rewards/book/makemytrip-link?destination_id=${destId}`);
        document.getElementById("btnMmt").href = mmtRes.url;
        
        // Reload points header
        loadPoints(); // silent refresh
    } catch(err) {
        alert("Redemption failed: " + err.message);
    }
}

async function doMockBooking() {
    if(!currentDiscount) return;
    try {
        const res = await apiPost("/rewards/book/partner-preview", {
            user_id: currentUserId,
            hotel_name: "Heritage Grand Hotel (Demo)",
            discount_code: currentDiscount.discount_code,
            discount_pct: currentDiscount.discount_pct
        });
        
        const conf = document.getElementById("mockConfirmation");
        conf.style.display = "block";
        conf.innerHTML = `
            <h4 style="color: #10b981; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                Booking Confirmed (Demo)
            </h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
                <div><span style="color: var(--text-muted);">Booking ID:</span><br><b>${res.booking_id}</b></div>
                <div><span style="color: var(--text-muted);">Hotel:</span><br><b>${res.hotel_name}</b></div>
                <div><span style="color: var(--text-muted);">Original Price:</span><br><s style="color: #ef4444;">₹${res.original_price}</s></div>
                <div><span style="color: var(--text-muted);">Discounted Price:</span><br><b style="font-size: 1.1rem; color: #10b981;">₹${res.discounted_price}</b></div>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px dashed var(--border); color: var(--text-secondary); font-size: 0.85rem;">
                ℹ️ ${res.confirmation_message}<br>
                <b>Applied:</b> ${res.discount_applied}
            </div>
        `;
    } catch(err) {
        alert("Mock booking failed: " + err.message);
    }
}


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
