/**
 * FootPrint — AI Crowd Intelligence Dashboard
 * All API logic unchanged; UI presentation layer only.
 */

const API_BASE = window.location.origin.includes("8000")
  ? window.location.origin
  : "http://127.0.0.1:8000";

/* Curated Unsplash photos — location-specific, hotlinked per Unsplash guidelines
   Format: images.unsplash.com/{photo-id}?auto=format&fit=crop&w=&h=&q=80 */
const DEST_IMAGES = {
  taj_mahal: {
    photo: "photo-1564507592333-c60657eea523",
    alt: "Taj Mahal, Agra",
    credit: "Jovyn Chamb",
    creditUrl: "https://unsplash.com/@jovynchamb",
    photoUrl: "https://unsplash.com/photos/taj-mahal-india-iWMfiInivp4",
  },
  jaipur_city_palace: {
    photo: "photo-1757310062384-d3bcfe3026e8",
    alt: "Hawa Mahal, Jaipur",
    credit: "Uttara B",
    creditUrl: "https://unsplash.com/@virat11",
    photoUrl: "https://unsplash.com/photos/intricate-facade-of-the-hawa-mahal-palace-in-jaipur-ZIoAHmZCcSs",
  },
  goa_baga_beach: {
    photo: "photo-1605649487212-47bdab064df7",
    alt: "Goa beach coastline",
    credit: "Rohan Rego",
    creditUrl: "https://unsplash.com/@r2ind",
    photoUrl: "https://unsplash.com/photos/sandy-beach-with-lush-green-hill-and-blue-ocean-INa5mgDXEUk",
  },
  kerala_backwaters: {
    photo: "photo-1593693401060-9fc28cf9e368",
    alt: "Kerala backwaters houseboat, Alleppey",
    credit: "Sreehari Devadas",
    creditUrl: "https://unsplash.com/@sreehari_dev",
    photoUrl: "https://unsplash.com/photos/brown-wooden-boat-on-body-of-water-near-green-palm-trees-during-daytime-ayFW56Rz5Cs",
  },
  varanasi_ghats: {
    photo: "photo-1570168007204-dfb528c6958f",
    alt: "Varanasi ghats at sunrise",
    credit: "Julian Yu",
    creditUrl: "https://unsplash.com/@julianyu",
    photoUrl: "https://unsplash.com/photos/varanasi-ghats-India",
  },
  hampi_ruins: {
    photo: "photo-1722934804353-0d9f6a55ab5e",
    alt: "Hampi stone temple ruins, Karnataka",
    credit: "Unsplash",
    creditUrl: "https://unsplash.com/@unsplash",
    photoUrl: "https://unsplash.com/photos/a-group-of-stone-structures-sitting-on-top-of-a-dirt-field-jDMCUnvD5lY",
  },
  manali: {
    photo: "photo-1506905925346-21bda4d32df4",
    alt: "Himalayan mountains near Manali",
    credit: "Simon Berger",
    creditUrl: "https://unsplash.com/@simon_berger",
    photoUrl: "https://unsplash.com/photos/snow-covered-mountain-under-stars-1506905925346",
  },
  mysore_palace: {
    photo: "photo-1611510338559-2f463335092c",
    alt: "Mysore Palace, Karnataka",
    credit: "Kiran CK",
    creditUrl: "https://unsplash.com/@kiranck",
    photoUrl: "https://unsplash.com/photos/mysore-palace-at-night-1611510338559",
  },
  agra_fort: {
    photo: "photo-1564507592333-c60657eea523",
    alt: "Agra Fort",
    credit: "Jovyn Chamb",
    creditUrl: "https://unsplash.com/@jovynchamb",
    photoUrl: "https://unsplash.com/photos/taj-mahal-india-iWMfiInivp4",
  },
  mehtab_bagh: {
    photo: "photo-1564507592333-c60657eea523",
    alt: "Mehtab Bagh",
    credit: "Jovyn Chamb",
    creditUrl: "https://unsplash.com/@jovynchamb",
    photoUrl: "https://unsplash.com/photos/taj-mahal-india-iWMfiInivp4",
  },
  fatehpur_sikri: {
    photo: "photo-1564507592333-c60657eea523",
    alt: "Fatehpur Sikri",
    credit: "Jovyn Chamb",
    creditUrl: "https://unsplash.com/@jovynchamb",
    photoUrl: "https://unsplash.com/photos/taj-mahal-india-iWMfiInivp4",
  },
  nahargarh_fort: {
    photo: "photo-1757310062384-d3bcfe3026e8",
    alt: "Nahargarh Fort",
    credit: "Uttara B",
    creditUrl: "https://unsplash.com/@virat11",
    photoUrl: "https://unsplash.com/photos/intricate-facade-of-the-hawa-mahal-palace-in-jaipur-ZIoAHmZCcSs",
  },
  albert_hall_museum: {
    photo: "photo-1757310062384-d3bcfe3026e8",
    alt: "Albert Hall Museum",
    credit: "Uttara B",
    creditUrl: "https://unsplash.com/@virat11",
    photoUrl: "https://unsplash.com/photos/intricate-facade-of-the-hawa-mahal-palace-in-jaipur-ZIoAHmZCcSs",
  },
  amer_fort: {
    photo: "photo-1757310062384-d3bcfe3026e8",
    alt: "Amer Fort",
    credit: "Uttara B",
    creditUrl: "https://unsplash.com/@virat11",
    photoUrl: "https://unsplash.com/photos/intricate-facade-of-the-hawa-mahal-palace-in-jaipur-ZIoAHmZCcSs",
  },
  anjuna_beach: {
    photo: "photo-1605649487212-47bdab064df7",
    alt: "Anjuna Beach",
    credit: "Rohan Rego",
    creditUrl: "https://unsplash.com/@r2ind",
    photoUrl: "https://unsplash.com/photos/sandy-beach-with-lush-green-hill-and-blue-ocean-INa5mgDXEUk",
  },
  chapora_fort: {
    photo: "photo-1605649487212-47bdab064df7",
    alt: "Chapora Fort",
    credit: "Rohan Rego",
    creditUrl: "https://unsplash.com/@r2ind",
    photoUrl: "https://unsplash.com/photos/sandy-beach-with-lush-green-hill-and-blue-ocean-INa5mgDXEUk",
  },
  morjim_beach: {
    photo: "photo-1605649487212-47bdab064df7",
    alt: "Morjim Beach",
    credit: "Rohan Rego",
    creditUrl: "https://unsplash.com/@r2ind",
    photoUrl: "https://unsplash.com/photos/sandy-beach-with-lush-green-hill-and-blue-ocean-INa5mgDXEUk",
  },
  marari_beach: {
    photo: "photo-1593693401060-9fc28cf9e368",
    alt: "Marari Beach",
    credit: "Sreehari Devadas",
    creditUrl: "https://unsplash.com/@sreehari_dev",
    photoUrl: "https://unsplash.com/photos/brown-wooden-boat-on-body-of-water-near-green-palm-trees-during-daytime-ayFW56Rz5Cs",
  },
  kumarakom_bird_sanctuary: {
    photo: "photo-1593693401060-9fc28cf9e368",
    alt: "Kumarakom Bird Sanctuary",
    credit: "Sreehari Devadas",
    creditUrl: "https://unsplash.com/@sreehari_dev",
    photoUrl: "https://unsplash.com/photos/brown-wooden-boat-on-body-of-water-near-green-palm-trees-during-daytime-ayFW56Rz5Cs",
  },
  sarnath: {
    photo: "photo-1570168007204-dfb528c6958f",
    alt: "Sarnath",
    credit: "Julian Yu",
    creditUrl: "https://unsplash.com/@julianyu",
    photoUrl: "https://unsplash.com/photos/varanasi-ghats-India",
  },
  ramnagar_fort: {
    photo: "photo-1570168007204-dfb528c6958f",
    alt: "Ramnagar Fort",
    credit: "Julian Yu",
    creditUrl: "https://unsplash.com/@julianyu",
    photoUrl: "https://unsplash.com/photos/varanasi-ghats-India",
  },
  matanga_hill: {
    photo: "photo-1722934804353-0d9f6a55ab5e",
    alt: "Matanga Hill",
    credit: "Unsplash",
    creditUrl: "https://unsplash.com/@unsplash",
    photoUrl: "https://unsplash.com/photos/a-group-of-stone-structures-sitting-on-top-of-a-dirt-field-jDMCUnvD5lY",
  },
  sanapur_lake: {
    photo: "photo-1722934804353-0d9f6a55ab5e",
    alt: "Sanapur Lake",
    credit: "Unsplash",
    creditUrl: "https://unsplash.com/@unsplash",
    photoUrl: "https://unsplash.com/photos/a-group-of-stone-structures-sitting-on-top-of-a-dirt-field-jDMCUnvD5lY",
  },
  solang_valley: {
    photo: "photo-1506905925346-21bda4d32df4",
    alt: "Solang Valley",
    credit: "Simon Berger",
    creditUrl: "https://unsplash.com/@simon_berger",
    photoUrl: "https://unsplash.com/photos/snow-covered-mountain-under-stars-1506905925346",
  },
  naggar_castle: {
    photo: "photo-1506905925346-21bda4d32df4",
    alt: "Naggar Castle",
    credit: "Simon Berger",
    creditUrl: "https://unsplash.com/@simon_berger",
    photoUrl: "https://unsplash.com/photos/snow-covered-mountain-under-stars-1506905925346",
  },
  chamundi_hill: {
    photo: "photo-1611510338559-2f463335092c",
    alt: "Chamundi Hill",
    credit: "Kiran CK",
    creditUrl: "https://unsplash.com/@kiranck",
    photoUrl: "https://unsplash.com/photos/mysore-palace-at-night-1611510338559",
  },
  brindavan_gardens: {
    photo: "photo-1611510338559-2f463335092c",
    alt: "Brindavan Gardens",
    credit: "Kiran CK",
    creditUrl: "https://unsplash.com/@kiranck",
    photoUrl: "https://unsplash.com/photos/mysore-palace-at-night-1611510338559",
  }
};

function destImageUrl(destId, width, height) {
  const meta = DEST_IMAGES[destId];
  if (!meta) return `https://picsum.photos/seed/${destId}/${width}/${height}`;
  // Unique sig per destination prevents browser/CDN serving a stale cached image
  return `https://images.unsplash.com/${meta.photo}?auto=format&fit=crop&w=${width}&h=${height}&q=80&ixlib=rb-4.0.3&sig=${encodeURIComponent(destId)}`;
}

function setHeroImage(destId) {
  const heroEl = document.getElementById("intelHero");
  let heroImg = document.getElementById("intelHeroImg");
  const imgMeta = DEST_IMAGES[destId];

  heroEl.classList.remove("hero-fallback");
  if (!imgMeta) return;

  const newUrl = destImageUrl(destId, 960, 280);

  // Replace img node so the browser cannot keep showing the previous destination photo
  const freshImg = document.createElement("img");
  freshImg.id = "intelHeroImg";
  freshImg.alt = imgMeta.alt;
  freshImg.decoding = "async";
  freshImg.loading = "eager";
  freshImg.className = "intel-hero-img";

  freshImg.onload = () => {
    heroEl.classList.remove("hero-fallback");
    freshImg.style.display = "block";
  };
  freshImg.onerror = () => {
    heroEl.classList.add("hero-fallback");
    freshImg.style.display = "none";
  };

  heroImg.replaceWith(freshImg);
  freshImg.src = newUrl;

  document.getElementById("heroImageCredit").innerHTML = imageCreditHtml(destId);
}

function imageCreditHtml(destId) {
  const meta = DEST_IMAGES[destId];
  if (!meta) return "";
  const utm = "utm_source=footprint&utm_medium=referral";
  return `Photo by <a href="${meta.creditUrl}?${utm}" target="_blank" rel="noopener noreferrer">${meta.credit}</a> on <a href="https://unsplash.com?${utm}" target="_blank" rel="noopener noreferrer">Unsplash</a>`;
}

let destinations = [];
let selectedDest = null;
let currentForecast = [];

// ---------------------------------------------------------------------------
// API helpers (unchanged)
// ---------------------------------------------------------------------------
async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `API error: ${res.status}`);
  }
  return res.json();
}

// ---------------------------------------------------------------------------
// Crowd level mapping (UI: Low → Moderate → High → Critical)
// Backend returns Low / Medium / High — mapped for display only
// ---------------------------------------------------------------------------
function displayLevel(cat, score) {
  if (score >= 90) return "Critical";
  const c = (cat || "").toLowerCase();
  if (c === "medium") return "Moderate";
  if (c === "high" && score < 90) return "High";
  if (c === "low") return "Low";
  return c.charAt(0).toUpperCase() + c.slice(1);
}

function levelClass(cat, score) {
  if (score >= 90) return "critical";
  const c = (cat || "medium").toLowerCase();
  return c === "medium" ? "moderate" : c;
}

function formatNumber(n) {
  return n.toLocaleString("en-IN");
}

function setApiStatus(online, text) {
  const el = document.getElementById("apiStatus");
  el.className = `nav-status ${online ? "online" : "offline"}`;
  el.querySelector(".status-label").textContent = text;
}

function updateScaleMarker(score) {
  const marker = document.getElementById("scaleMarker");
  marker.style.left = `${Math.min(100, Math.max(0, score))}%`;
}

function updateBestTime(forecast) {
  if (!forecast || !forecast.length) return;

  const best = forecast.reduce((a, b) =>
    a.crowd_score <= b.crowd_score ? a : b
  );

  const dateObj = new Date(best.date + "T00:00:00");
  const formatted = dateObj.toLocaleDateString("en-IN", {
    weekday: "long",
    month: "short",
    day: "numeric",
  });

  document.getElementById("bestTimeDate").textContent = formatted;
  document.getElementById("bestTimeDetail").textContent =
    `${best.day_of_week}${best.is_holiday ? " (Holiday — expect higher crowds nearby)" : ""} · Lowest predicted crowd in the next 7 days`;
  document.getElementById("bestTimeScore").textContent =
    `${best.crowd_score}/100 · ${displayLevel(best.crowd_category, best.crowd_score)}`;
}

// ---------------------------------------------------------------------------
// Render destination list (compact sidebar cards)
// ---------------------------------------------------------------------------
function renderDestinations() {
  const grid = document.getElementById("destinationsGrid");
  grid.innerHTML = destinations
    .map((d) => {
      const cls = levelClass(d.current_crowd_category, d.current_crowd_score);
      const level = displayLevel(d.current_crowd_category, d.current_crowd_score);
      const imgMeta = DEST_IMAGES[d.destination_id];
      const thumbUrl = destImageUrl(d.destination_id, 160, 112);
      const alt = imgMeta?.alt || d.name;
      const isActive = selectedDest?.destination_id === d.destination_id;
      return `
      <article class="dest-item${isActive ? " active" : ""}" data-id="${d.destination_id}" tabindex="0" role="button">
        <div class="dest-thumb">
          <img src="${thumbUrl}" alt="${alt}" loading="lazy" decoding="async" width="80" height="56" onerror="this.closest('.dest-thumb').classList.add('thumb-fallback')" />
          <span class="crowd-badge ${cls} dest-thumb-badge">${level}</span>
        </div>
        <div class="dest-info">
          <h4>${d.name}</h4>
          <p>${d.city}, ${d.state}</p>
          <div class="dest-score-row">
            <span class="score-label">Crowd Index</span>
            <span class="score">${d.current_crowd_score}<span class="score-max">/100</span></span>
          </div>
        </div>
        <div class="dest-indicator ${cls}" aria-hidden="true"></div>
      </article>`;
    })
    .join("");

  grid.querySelectorAll(".dest-item").forEach((item) => {
    item.addEventListener("click", () => openDetail(item.dataset.id));
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openDetail(item.dataset.id);
      }
    });
  });
}

// ---------------------------------------------------------------------------
// Detail / intelligence panel (UI 2 version)
// ---------------------------------------------------------------------------
async function openDetail(destId) {
  selectedDest = destinations.find((d) => d.destination_id === destId);
  if (!selectedDest) return;

  document.getElementById("emptyState").hidden = true;
  document.getElementById("detailSection").hidden = false;
  document.getElementById("intelPanel").classList.add("has-selection");

  document.getElementById("detailTitle").textContent = selectedDest.name;
  document.getElementById("detailSubtitle").textContent =
    `${selectedDest.city}, ${selectedDest.state} · Max capacity ${formatNumber(selectedDest.max_capacity)} visitors/day`;

  const score = selectedDest.current_crowd_score;
  const gaugeScoreEl = document.getElementById("gaugeScore");
  if (gaugeScoreEl) gaugeScoreEl.textContent = score;

  setHeroImage(selectedDest.destination_id);

  renderDestinations();

  if (window.innerWidth <= 768) {
    document.getElementById("intelPanel").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // UI 3 Safety Data Fetch
  try {
    const riskZones = await apiGet(`/safety/risk-zones/${destId}`);
    renderRiskZones(riskZones);
    
    // Demo-friendly: pre-fill the routing form so it intersects the first risk zone
    if (riskZones.length > 0) {
      const demoLat = riskZones[0].latitude;
      const demoLon = riskZones[0].longitude;
      
      document.getElementById("startLat").value = (demoLat - 0.005).toFixed(4);
      document.getElementById("startLon").value = (demoLon - 0.005).toFixed(4);
      document.getElementById("endLat").value = (demoLat + 0.005).toFixed(4);
      document.getElementById("endLon").value = (demoLon + 0.005).toFixed(4);

      // Populate dummy dynamic map
      const mapUrl = `https://maps.google.com/maps?q=${demoLat},${demoLon}&z=14&output=embed`;
      document.getElementById("sosMap").src = mapUrl;
    }
  } catch (err) {
    document.getElementById("riskZonesTable").innerHTML = `<tr><td colspan="3">Error loading risk zones</td></tr>`;
  }

  try {
    const helpPoints = await apiGet(`/safety/help-points/${destId}`);
    renderHelpPoints(helpPoints);
  } catch (err) {
    document.getElementById("helpPointsTable").innerHTML = `<tr><td colspan="3">Error loading help points</td></tr>`;
  }
}

function renderRiskZones(zones) {
  const tbody = document.getElementById("riskZonesTable");
  if (!zones || zones.length === 0) {
    tbody.innerHTML = `<tr><td colspan="3">No risk zones flagged for this destination.</td></tr>`;
    return;
  }

  tbody.innerHTML = zones.map(z => {
    let color = z.risk_level === 'High' ? 'color: #e11d48; font-weight: bold;' : 'color: #ea580c; font-weight: 500;';
    return `
      <tr>
        <td style="${color}">${z.risk_level}</td>
        <td style="text-transform: capitalize;">${z.risk_type.replace('_', ' ')}</td>
        <td style="font-size: 0.85rem;">Lat: ${z.latitude.toFixed(3)}<br>Lon: ${z.longitude.toFixed(3)}</td>
      </tr>
    `;
  }).join("");
}

function renderHelpPoints(points) {
  const tbody = document.getElementById("helpPointsTable");
  if (!points || points.length === 0) {
    tbody.innerHTML = `<tr><td colspan="3">No emergency services found nearby.</td></tr>`;
    return;
  }

  tbody.innerHTML = points.map(p => {
    return `
      <tr>
        <td style="text-transform: capitalize; font-weight: 500;">${p.type}</td>
        <td>${p.name}</td>
        <td style="font-family: monospace;">${p.phone_number}</td>
      </tr>
    `;
  }).join("");
}

function clearSelection() {
  selectedDest = null;
  document.getElementById("detailSection").hidden = true;
  document.getElementById("emptyState").hidden = false;
  document.getElementById("intelPanel").classList.remove("has-selection");
  document.getElementById("sosResult").hidden = true;
  document.getElementById("routeResult").hidden = true;
  document.getElementById("sosMap").src = "about:blank";
  renderDestinations();
}

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------
async function init() {
  try {
    const health = await apiGet("/health");
    setApiStatus(true, `${(health.inference_model || "AI").toUpperCase()} · Online`);

    document.getElementById("statModel").textContent = "Smart Safety Engine";

    const railSub = document.querySelector(".intel-rail-sub");
    if (railSub) railSub.textContent = "Live Risk & SOS Monitoring";

    destinations = await apiGet("/destinations");
    document.getElementById("statDestinations").textContent = destinations.length;
    document.getElementById("statUpdated").textContent = new Date().toLocaleTimeString("en-IN", {
      hour: "2-digit",
      minute: "2-digit",
    });

    renderDestinations();

    if (destinations.length > 0) {
      openDetail(destinations[0].destination_id);
    }
  } catch (err) {
    setApiStatus(false, "Offline");
    document.getElementById("destinationsGrid").innerHTML = `
      <div class="error-message">
        <p><strong>Cannot connect to API</strong></p>
        <p style="margin-top:0.5rem">Run: <code>uvicorn api:app --reload</code></p>
        <p style="margin-top:0.5rem"><a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a></p>
      </div>`;
  }
}

document.getElementById("btnBack").addEventListener("click", clearSelection);
document.getElementById("brandHome").addEventListener("click", (e) => {
  e.preventDefault();
  clearSelection();
  window.scrollTo({ top: 0, behavior: "smooth" });
});
document.getElementById("navDestinations").addEventListener("click", () => {
  document.getElementById("sidebar").scrollIntoView({ behavior: "smooth" });
});

document.getElementById("btnSos").addEventListener("click", async () => {
  if (!selectedDest) return;
  const resultDiv = document.getElementById("sosResult");
  
  resultDiv.hidden = false;
  resultDiv.innerHTML = "Triggering SOS...";
  resultDiv.style.color = "#000";

  // Simulate current user location using standard offset from destination
  try {
    // Get risk zones just to find base coordinates quickly for demo
    const rz = await apiGet(`/safety/risk-zones/${selectedDest.destination_id}`);
    let lat = 0, lon = 0;
    if (rz.length > 0) {
       lat = rz[0].latitude;
       lon = rz[0].longitude;
    }

    const payload = {
      user_id: "tourist_101",
      lat: lat,
      lon: lon,
      emergency_contacts: ["+91-9998887776", "+91-1122334455"]
    };

    const res = await apiPost("/safety/sos", payload);
    
    let html = `<div style="color: #16a34a; margin-bottom: 0.5rem;">&#10004; SOS Sent Successfully!</div>`;
    html += `<div style="font-size: 0.8rem; color: #4b5563;">Alerts dispatched to: ${res.alert_sent_to.join(", ")}</div>`;
    if (res.nearest_police) {
       html += `<div style="font-size: 0.8rem; margin-top: 0.2rem; color: #1e40af;">Police Dispatched: ${res.nearest_police.name}</div>`;
    }
    resultDiv.innerHTML = html;
  } catch (err) {
    resultDiv.innerHTML = `<span style="color: #e11d48;">Error triggering SOS: ${err.message}</span>`;
  }
});

document.getElementById("routeForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!selectedDest) return;

  const resultDiv = document.getElementById("routeResult");
  resultDiv.hidden = false;
  resultDiv.innerHTML = "Analyzing route...";

  const payload = {
    destination_id: selectedDest.destination_id,
    start_lat: parseFloat(document.getElementById("startLat").value),
    start_lon: parseFloat(document.getElementById("startLon").value),
    end_lat: parseFloat(document.getElementById("endLat").value),
    end_lon: parseFloat(document.getElementById("endLon").value)
  };

  try {
    const res = await apiPost("/safety/safe-route", payload);
    
    if (res.is_safe) {
      resultDiv.innerHTML = `<div style="padding: 0.5rem; background: #dcfce7; color: #166534; border-radius: 4px; border: 1px solid #bbf7d0;">&#10004; Route is safe! No risk zones detected.</div>`;
    } else {
      let html = `<div style="padding: 0.5rem; background: #fee2e2; color: #991b1b; border-radius: 4px; border: 1px solid #fecaca;">&#9888; Warning! Route intersects risk zones.</div>`;
      html += `<ul style="margin: 0.5rem 0 0 1.2rem; color: #b91c1c;">`;
      res.warnings.forEach(w => html += `<li>${w}</li>`);
      html += `</ul>`;
      if (res.suggested_waypoints.length > 0) {
         html += `<div style="margin-top: 0.5rem; color: #4338ca;"><strong>Suggested Detour:</strong> Navigate via Lat ${res.suggested_waypoints[0].lat.toFixed(4)}, Lon ${res.suggested_waypoints[0].lon.toFixed(4)}</div>`;
      }
      resultDiv.innerHTML = html;
    }
  } catch(err) {
    resultDiv.innerHTML = `<span style="color: #e11d48;">Error: ${err.message}</span>`;
  }
});

init();

