const API_BASE = (window.location.protocol === "http:" || window.location.protocol === "https:")
  ? (window.location.port === "5500" || window.location.port === "3000" ? "http://127.0.0.1:8000" : window.location.origin)
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

// Tab Logic with bold prominent states
function bindTabs() {
    const tabs = ["Upload", "Points", "Redeem"];
    tabs.forEach(t => {
        const btn = document.getElementById(`tab${t}`);
        if (!btn) return;
        btn.addEventListener("click", () => {
            tabs.forEach(x => {
                const b = document.getElementById(`tab${x}`);
                const sec = document.getElementById(`sec${x}`);
                if (b) {
                    b.classList.remove("active");
                    b.style.background = "transparent";
                    b.style.color = "#334155";
                    b.style.boxShadow = "none";
                }
                if (sec) sec.style.display = "none";
            });
            btn.classList.add("active");
            btn.style.background = "#0f172a";
            btn.style.color = "#ffffff";
            btn.style.boxShadow = "0 4px 12px rgba(15,23,42,0.18)";
            const secTarget = document.getElementById(`sec${t}`);
            if (secTarget) secTarget.style.display = "block";
            
            if (t === "Points") loadPoints();
            if (t === "Redeem") loadRedeem();
        });
    });
}

// Curated Destination and Monument Image Datasets
const DEST_PHOTO_MAP = {
  taj_mahal: "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1000&q=80",
  jaipur_city_palace: "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1000&q=80",
  goa_baga_beach: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1000&q=80",
  kerala_backwaters: "https://images.unsplash.com/photo-1593693401060-9fc28cf9e368?auto=format&fit=crop&w=1000&q=80",
  varanasi_ghats: "https://images.unsplash.com/photo-1561359313-0639aad073f0?auto=format&fit=crop&w=1000&q=80",
  hampi_ruins: "https://images.unsplash.com/photo-1722934804353-0d9f6a55ab5e?auto=format&fit=crop&w=1000&q=80",
  manali: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1000&q=80",
  mysore_palace: "https://images.unsplash.com/photo-1611510338559-2f463335092c?auto=format&fit=crop&w=1000&q=80",
  kempty_falls: "images/kempty_falls.jpg",
  robbers_cave: "images/robbers_cave.jpg",
};

function getDestImage(destId) {
  return DEST_PHOTO_MAP[destId] || "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1000&q=80";
}

// Section 1: Upload & Photography Journey
async function loadDestinations() {
    try {
        const dests = await apiGet("/destinations");
        const progress = await apiGet(`/rewards/progress-overview/${currentUserId}`);
        
        // Update global progress with modern progress bar
        const pGlobal = progress.global_progress;
        const globalPct = Math.round((pGlobal.captured_monuments / (pGlobal.total_monuments || 1)) * 100);
        const globalEl = document.getElementById("globalProgress");
        if (globalEl) {
            globalEl.innerHTML = `
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
                        <div>
                            <h3 style="font-size: 1.25rem; font-weight: 700; margin: 0 0 0.25rem 0; color: var(--text-primary);">Heritage Photography Journey</h3>
                            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">Photograph authentic Indian monuments & hidden gems to earn hotel discounts</p>
                        </div>
                        <div style="text-align: right; background: #f8fafc; padding: 0.5rem 1rem; border-radius: 10px; border: 1px solid var(--border);">
                            <span style="font-size: 1.4rem; font-weight: 800; color: var(--accent-dark);">${pGlobal.captured_monuments}</span>
                            <span style="color: var(--text-muted); font-size: 0.95rem;"> / ${pGlobal.total_monuments}</span>
                            <span style="font-size: 0.75rem; font-weight: 600; color: #10b981; margin-left: 0.35rem; text-transform: uppercase;">(${globalPct}% Captured)</span>
                        </div>
                    </div>
                    <div style="width: 100%; height: 8px; background: #f1f5f9; border-radius: 999px; overflow: hidden; margin-top: 0.75rem; border: 1px solid #e2e8f0;">
                        <div style="width: ${globalPct}%; height: 100%; background: linear-gradient(90deg, #10b981, #06b6d4); transition: width 0.5s ease;"></div>
                    </div>
                </div>
            `;
        }
            
        const grid = document.getElementById("destOverviewGrid");
        grid.innerHTML = "";
        
        dests.forEach(d => {
            const destProgress = progress.destinations.find(x => x.destination_id === d.destination_id);
            if (!destProgress) return;
            
            const pct = Math.round((destProgress.captured_monuments / (destProgress.total_monuments || 1)) * 100);
            const isAllCaptured = destProgress.captured_monuments === destProgress.total_monuments && destProgress.total_monuments > 0;
            const destImg = getDestImage(d.destination_id);
            
            const card = document.createElement("div");
            card.style.background = "white";
            card.style.borderRadius = "16px";
            card.style.border = "1px solid var(--border)";
            card.style.overflow = "hidden";
            card.style.cursor = "pointer";
            card.style.transition = "transform 0.25s ease, box-shadow 0.25s ease";
            card.style.display = "flex";
            card.style.flexDirection = "column";
            card.style.boxShadow = "0 2px 6px rgba(0,0,0,0.04)";
            
            card.onmouseover = () => {
                card.style.transform = "translateY(-5px)";
                card.style.boxShadow = "0 12px 24px -4px rgba(0,0,0,0.1)";
                const img = card.querySelector(".dest-card-img");
                if (img) img.style.transform = "scale(1.05)";
            };
            card.onmouseout = () => {
                card.style.transform = "none";
                card.style.boxShadow = "0 2px 6px rgba(0,0,0,0.04)";
                const img = card.querySelector(".dest-card-img");
                if (img) img.style.transform = "scale(1)";
            };
            card.onclick = () => showDestinationDetail(d, destProgress, progress.captured_monument_ids);
            
            card.innerHTML = `
                <div style="height: 160px; background: #0f172a; position: relative; overflow: hidden;">
                    <img class="dest-card-img" src="${destImg}" alt="${d.name}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.35s ease;" onerror="this.src='https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80'" />
                    <div style="position: absolute; inset: 0; background: linear-gradient(to top, rgba(15,23,42,0.7) 0%, transparent 60%);"></div>
                    
                    <!-- Location Pill -->
                    <div style="position: absolute; top: 0.75rem; left: 0.75rem; background: rgba(15,23,42,0.75); backdrop-filter: blur(4px); color: white; padding: 0.25rem 0.65rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; gap: 0.3rem;">
                        📍 ${d.city}
                    </div>

                    <!-- Points Badge -->
                    <div style="position: absolute; top: 0.75rem; right: 0.75rem; background: #fef3c7; color: #92400e; padding: 0.25rem 0.65rem; border-radius: 999px; font-size: 0.75rem; font-weight: 700; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        ✨ Up to ${destProgress.total_points_possible || 600} pts
                    </div>
                </div>
                <div style="padding: 1.25rem; display: flex; flex-direction: column; flex: 1;">
                    <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin: 0 0 0.35rem 0;">${d.name}</h3>
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">${d.city}, ${d.state}</div>
                    
                    <!-- Progress Section -->
                    <div style="margin-top: auto; padding-top: 0.75rem; border-top: 1px solid var(--border);">
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; margin-bottom: 0.4rem;">
                            <span style="color: var(--text-muted);">${destProgress.total_monuments} Heritage Spots</span>
                            <span style="font-weight: 600; color: ${isAllCaptured ? '#10b981' : 'var(--accent-dark)'};">
                                ${isAllCaptured ? '✅ All Captured' : `${destProgress.captured_monuments}/${destProgress.total_monuments} captured`}
                            </span>
                        </div>
                        <div style="width: 100%; height: 6px; background: #f1f5f9; border-radius: 999px; overflow: hidden; border: 1px solid #e2e8f0;">
                            <div style="width: ${pct}%; height: 100%; background: ${isAllCaptured ? '#10b981' : 'linear-gradient(90deg, #f59e0b, #ef4444)'};"></div>
                        </div>
                    </div>

                    <div style="margin-top: 0.75rem; display: flex; align-items: center; justify-content: space-between; color: var(--accent-dark); font-size: 0.8rem; font-weight: 600;">
                        <span>Explore Sites</span>
                        <span>→</span>
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });
        
    } catch(err) {
        console.error(err);
        document.getElementById("destOverviewGrid").innerHTML = '<div style="color: red; padding: 1rem;">Failed to load destinations.</div>';
    }
}

function showDestinationDetail(dest, destProgress, capturedIds) {
    currentDestId = dest.destination_id;
    document.getElementById("destOverviewGrid").style.display = "none";
    document.getElementById("globalProgress").style.display = "none";
    document.getElementById("destDetailView").style.display = "block";
    
    document.getElementById("destHeroName").textContent = dest.name;
    document.getElementById("destHeroCity").textContent = `${dest.city}, ${dest.state} · ${destProgress.total_monuments} Heritage Sites · Up to ${destProgress.total_points_possible || 600} Points`;
    document.getElementById("destHeroImg").src = getDestImage(dest.destination_id);
    
    document.getElementById("btnBackOverview").onclick = () => {
        document.getElementById("destDetailView").style.display = "none";
        document.getElementById("destOverviewGrid").style.display = "grid";
        document.getElementById("globalProgress").style.display = "flex";
        loadDestinations(); // Refresh progress
    };
    
    loadMonuments(currentDestId, capturedIds);
}

async function loadMonuments(destId, capturedIds) {
    const grid = document.getElementById("monumentGrid");
    grid.innerHTML = '<div class="loading-state">Loading monuments & hidden gems...</div>';
    try {
        const monuments = await apiGet(`/rewards/monuments/${destId}`);
        if(monuments.length === 0) {
            grid.innerHTML = '<div style="color: var(--text-muted); padding: 1.5rem;">No monuments available here yet.</div>';
            return;
        }
        
        grid.innerHTML = monuments.map((m, index) => {
            const isCaptured = capturedIds.includes(m.monument_id);
            const monumentImg = m.image_url || getDestImage(destId);
            
            let badgeHtml = "";
            let btnHtml = "";
            let overlayHtml = "";
            
            if (isCaptured) {
                overlayHtml = `<div style="position: absolute; inset: 0; background: rgba(255,255,255,0.7); z-index: 10; pointer-events: none;"></div>`;
                badgeHtml = `<div style="position: absolute; top: 0.75rem; right: 0.75rem; background: #10b981; color: white; padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.8rem; font-weight: 700; z-index: 11; display: flex; align-items: center; gap: 0.35rem; box-shadow: 0 2px 6px rgba(16,185,129,0.3);">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    Captured
                </div>`;
                btnHtml = `
                <button disabled style="width: 100%; padding: 0.75rem; background: #e2e8f0; color: var(--text-muted); border: none; border-radius: 10px; font-weight: 600; cursor: not-allowed; display: flex; justify-content: center; align-items: center; gap: 0.5rem; z-index: 11; position: relative;">
                    ✅ Already Photographed
                </button>`;
            } else {
                badgeHtml = `<div style="position: absolute; top: 0.75rem; right: 0.75rem; background: #fef3c7; color: #92400e; padding: 0.3rem 0.8rem; border-radius: 999px; font-weight: 800; font-size: 0.8rem; z-index: 11; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
                    +${m.points_value} pts
                </div>`;
                btnHtml = `
                <div style="display: flex; gap: 0.5rem; width: 100%;">
                    <button onclick="openCamera('${m.monument_id}', '${m.name.replace("'", "\\'")}')" style="flex: 1; padding: 0.7rem 0.5rem; background: var(--accent-dark); color: white; border: none; border-radius: 8px; font-weight: 600; font-size: 0.85rem; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 0.35rem; z-index: 11; position: relative; transition: opacity 0.2s;">
                        📸 Camera
                    </button>
                    <button onclick="document.getElementById('file_${m.monument_id}').click()" style="flex: 1; padding: 0.7rem 0.5rem; background: #f1f5f9; color: var(--text-primary); border: 1px solid var(--border); border-radius: 8px; font-weight: 600; font-size: 0.85rem; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 0.35rem; z-index: 11; position: relative; transition: background 0.2s;">
                        📁 Upload
                    </button>
                </div>`;
            }
            
            return `
            <div style="background: white; border: 1px solid var(--border); border-radius: 16px; overflow: hidden; position: relative; display: flex; flex-direction: column; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 0.2s ease;">
                ${overlayHtml}
                ${badgeHtml}

                <!-- Monument Image -->
                <div style="height: 190px; background: #0f172a; position: relative; overflow: hidden;">
                    <img src="${monumentImg}" alt="${m.name}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.src='${getDestImage(destId)}'" />
                    <div style="position: absolute; inset: 0; background: linear-gradient(to top, rgba(15,23,42,0.7) 0%, transparent 60%);"></div>
                    <div style="position: absolute; bottom: 0.75rem; left: 0.75rem; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); color: white; padding: 0.2rem 0.55rem; border-radius: 6px; font-size: 0.75rem; font-weight: 500;">
                        Site #${index + 1}
                    </div>
                </div>

                <div style="padding: 1.25rem; display: flex; flex-direction: column; flex-grow: 1;">
                    <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin: 0 0 0.4rem 0;">${m.name}</h3>
                    <p style="color: var(--text-secondary); font-size: 0.88rem; line-height: 1.4; margin-bottom: 1.25rem; flex-grow: 1;">${m.description}</p>
                    
                    <input type="file" id="file_${m.monument_id}" accept="image/*" capture="environment" style="display: none;" onchange="handleUpload('${m.monument_id}')">
                    <img id="preview_${m.monument_id}" src="" style="display:none; width: 100%; height: 180px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem; border: 1px solid var(--border); position: relative; z-index: 11;" />
                    
                    ${btnHtml}
                    
                    <div id="res_${m.monument_id}" style="margin-top: 1rem; display: none; font-size: 0.85rem; padding: 0.75rem; border-radius: 8px; position: relative; z-index: 11;"></div>
                </div>
            </div>
        `}).join("");
    } catch(err) {
        grid.innerHTML = `<div style="color: red; padding: 1rem;">Error: ${err.message}</div>`;
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

// Section 3: Redeem & Hotel Bookings
async function loadRedeem() {
    const grid = document.getElementById("redeemGrid");
    grid.innerHTML = '<div class="loading-state">Loading rewards...</div>';
    try {
        const tiers = await apiGet(`/rewards/available-tiers/${currentUserId}`);
        
        grid.innerHTML = tiers.map(t => {
            const isMax = t.discount_pct === 10;
            const badgeText = isMax ? '⭐ Max Allowed Coupon (10%)' : 'Verified Partner Voucher';
            const badgeBg = isMax ? '#fef3c7' : '#f1f5f9';
            const badgeColor = isMax ? '#92400e' : '#475569';
            
            return `
            <div class="coupon-card" style="background: white; border: 2px solid ${isMax ? '#f59e0b' : 'var(--border)'}; border-radius: 16px; padding: 2rem 1.5rem; text-align: center; position: relative; overflow: hidden; box-shadow: 0 4px 14px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s ease, box-shadow 0.2s ease;">
                
                <!-- Notch ornament -->
                <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); background: #f8fafc; border: 1px solid var(--border); border-top: none; width: 60px; height: 10px; border-radius: 0 0 10px 10px;"></div>

                <div>
                    <div style="display: inline-block; background: ${badgeBg}; color: ${badgeColor}; padding: 0.3rem 0.85rem; border-radius: 999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 1.25rem;">
                        ${badgeText}
                    </div>
                    
                    <div style="font-size: 3rem; font-weight: 900; color: var(--accent-dark); line-height: 1; margin-bottom: 0.5rem; font-family: 'Instrument Serif', Georgia, serif;">
                        ${t.discount_pct}% OFF
                    </div>
                    
                    <div style="font-weight: 700; color: var(--text-primary); font-size: 1.1rem; margin-bottom: 0.25rem;">Hotel Bookings</div>
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1.5rem;">Valid on all partner stays across India</div>
                </div>

                <div>
                    <div style="font-size: 0.85rem; color: #b45309; font-weight: 700; margin-bottom: 0.75rem; display: flex; align-items: center; justify-content: center; gap: 0.3rem;">
                        ✨ Requires ${t.points_required} Points
                    </div>

                    <button 
                        id="btn_redeem_${t.tier_id}"
                        onclick="doRedeem('${t.tier_id}')" 
                        style="width: 100%; padding: 0.9rem; background: var(--accent-dark); color: white; border: none; border-radius: 12px; font-weight: 800; font-size: 1rem; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; transition: transform 0.15s, box-shadow 0.15s; box-shadow: 0 4px 12px rgba(15,23,42,0.18);">
                        <span>🎁 Redeem Voucher</span>
                    </button>

                    <!-- Reveal code block -->
                    <div id="code_box_${t.tier_id}" style="display: none; margin-top: 1rem; padding: 1rem; background: #f0fdf4; border: 2px dashed #16a34a; border-radius: 12px; text-align: center;">
                        <div style="font-size: 0.75rem; font-weight: 700; color: #166534; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">Redeem Code:</div>
                        <div id="code_val_${t.tier_id}" style="font-family: monospace; font-size: 1.25rem; font-weight: 900; color: #15803d; margin: 0.35rem 0; letter-spacing: 1.5px;"></div>
                        <button onclick="copyVoucherCode('${t.tier_id}')" id="copy_btn_${t.tier_id}" style="padding: 0.45rem 1rem; background: #16a34a; color: white; border: none; border-radius: 6px; font-size: 0.85rem; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; gap: 0.4rem; box-shadow: 0 2px 6px rgba(22,163,74,0.3);">
                            📋 Copy Code
                        </button>
                        <div style="font-size: 0.75rem; color: #166534; margin-top: 0.5rem;">✅ ${t.discount_pct}% discount code ready to apply</div>
                    </div>
                </div>
            </div>
            `;
        }).join("");
    } catch(err) {
        grid.innerHTML = `<div style="color: red; padding: 1rem;">Error: ${err.message}</div>`;
    }
}

async function doRedeem(tierId) {
    const btn = document.getElementById(`btn_redeem_${tierId}`);
    if (btn) {
        btn.textContent = "Generating Code...";
        btn.style.opacity = "0.7";
        btn.disabled = true;
    }
    try {
        const res = await apiPost("/rewards/redeem", { user_id: currentUserId, tier_id: tierId });
        currentDiscount = res;
        
        // Show code directly inside the coupon card
        const codeBox = document.getElementById(`code_box_${tierId}`);
        const codeVal = document.getElementById(`code_val_${tierId}`);
        if (codeBox && codeVal) {
            codeVal.textContent = res.discount_code;
            codeBox.style.display = "block";
        }
        if (btn) {
            btn.style.display = "none";
        }
        
        // Update booking section below
        document.getElementById("activeCode").textContent = res.discount_code;
        document.getElementById("bookingActions").style.display = "block";
        document.getElementById("mockConfirmation").style.display = "none";
        
        // Setup MMT Link
        const destId = currentDestId || "taj_mahal";
        const mmtRes = await apiGet(`/rewards/book/makemytrip-link?destination_id=${destId}`);
        document.getElementById("btnMmt").href = mmtRes.url;
        
        // Refresh balance display
        loadPoints();
    } catch(err) {
        if (btn) {
            btn.textContent = "🎁 Redeem Voucher";
            btn.style.opacity = "1";
            btn.disabled = false;
        }
        alert("Redemption failed: " + err.message);
    }
}

function copyVoucherCode(tierId) {
    const codeEl = document.getElementById(`code_val_${tierId}`);
    if (!codeEl) return;
    const text = codeEl.textContent.trim();
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById(`copy_btn_${tierId}`);
        if (btn) {
            btn.textContent = "✅ Copied!";
            setTimeout(() => { btn.textContent = "📋 Copy Code"; }, 2500);
        }
    }).catch(() => {
        const btn = document.getElementById(`copy_btn_${tierId}`);
        if (btn) btn.textContent = "✅ Copied!";
    });
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
