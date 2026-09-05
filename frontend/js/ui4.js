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
async function apiGet(path, timeoutMs=5000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(`${API_BASE}${path}`, { signal: controller.signal });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(id);
  }
}

async function apiPost(path, body, timeoutMs=5000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `API error: ${res.status}`);
    }
    return await res.json();
  } finally {
    clearTimeout(id);
  }
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

  document.getElementById("hiddenGemsState").hidden = true;
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

  // UI 4 Local Market Data Fetch
  fetchLocalMarket(destId, "");
  fetchAltLocalMarket(destId);
}

async function fetchLocalMarket(destId, category) {
  const grid = document.getElementById("localBusinessesGrid");
  const errDiv = document.getElementById("localBizError");
  errDiv.hidden = true;
  grid.innerHTML = `<div class="loading-state" style="grid-column: 1 / -1;">Loading local businesses...</div>`;

  try {
    const url = category ? `/local/businesses/${destId}?category=${category}` : `/local/businesses/${destId}`;
    const businesses = await apiGet(url);
    renderBusinesses(businesses, grid);
  } catch (err) {
    grid.innerHTML = "";
    errDiv.textContent = `Error loading businesses: ${err.message}`;
    errDiv.hidden = false;
  }
}

async function fetchAltLocalMarket(destId) {
  const grid = document.getElementById("altBusinessesGrid");
  const errDiv = document.getElementById("altBizError");
  errDiv.hidden = true;
  grid.innerHTML = `<div class="loading-state" style="grid-column: 1 / -1;">Discovering alternatives...</div>`;

  try {
    const businesses = await apiGet(`/local/businesses-near-alternative/${destId}`);
    if (!businesses || businesses.length === 0) {
       grid.innerHTML = `<p style="grid-column: 1 / -1; color: var(--text-muted);">No alternative businesses found.</p>`;
       return;
    }
    renderBusinesses(businesses, grid);
  } catch (err) {
    grid.innerHTML = "";
    errDiv.textContent = `Error loading alternatives: ${err.message}`;
    errDiv.hidden = false;
  }
}

function renderBusinesses(businesses, gridEl) {
  if (!businesses || businesses.length === 0) {
    gridEl.innerHTML = `<p style="grid-column: 1 / -1; color: var(--text-muted);">No businesses found in this category.</p>`;
    return;
  }

  gridEl.innerHTML = businesses.map(b => {
    const dataStr = encodeURIComponent(JSON.stringify(b));
    return `
      <div style="background: white; border: 1px solid var(--border); border-radius: 8px; padding: 1rem; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;" onclick="showBizDetails(this)" data-biz="${dataStr}" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
        <div style="display: flex; justify-content: space-between; align-items: start;">
          <h4 style="font-size: 1.1rem; color: var(--text-main); margin-bottom: 0.25rem;">${b.name}</h4>
          <span style="background: #fef3c7; color: #b45309; padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.8rem; font-weight: bold;">★ ${b.rating}</span>
        </div>
        <div style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">${b.category} • ${b.price_range}</div>
        <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 1rem; line-height: 1.4;">${b.description}</p>
        <div style="font-size: 0.85rem; color: var(--brand); font-weight: 500;">📞 ${b.contact_info}</div>
      </div>
    `;
  }).join("");
}

window.showBizDetails = function(el) {
  try {
    const b = JSON.parse(decodeURIComponent(el.getAttribute("data-biz")));
    document.getElementById("modalBizName").textContent = b.name;
    document.getElementById("modalBizRating").textContent = "★ " + b.rating;
    document.getElementById("modalBizCategory").textContent = b.category;
    document.getElementById("modalBizDesc").textContent = b.description;
    
    // Check if the fields exist (they will with our updated Python code)
    document.getElementById("modalBizOpen").textContent = b.opening_time || "09:00 AM";
    document.getElementById("modalBizClose").textContent = b.closing_time || "08:00 PM";
    
    document.getElementById("modalBizPrice").textContent = "Price: " + b.price_range;
    document.getElementById("modalBizContact").href = "tel:" + b.contact_info.replace(/[^0-9+]/g, '');
    
    const modal = document.getElementById("bizModal");
    modal.style.display = "flex";
  } catch(e) {
    console.error("Error parsing business data", e);
  }
};


function clearSelection() {
  selectedDest = null;
  document.getElementById("detailSection").hidden = true;
  document.getElementById("hiddenGemsState").hidden = false;
  document.getElementById("intelPanel").classList.remove("has-selection");
  renderDestinations();
}

// ---------------------------------------------------------------------------
// Init & Hidden Gems
// ---------------------------------------------------------------------------
async function fetchHiddenGems() {
  const grid = document.getElementById("hiddenGemsGrid");
  const errDiv = document.getElementById("hiddenGemsError");
  try {
    const gems = await apiGet("/local/hidden-gems?exclude_top=3");
    if (!gems || gems.length === 0) {
      grid.innerHTML = `<p style="grid-column: 1 / -1;">No hidden gems found.</p>`;
      return;
    }
    grid.innerHTML = gems.map(g => {
      const bgImg = destImageUrl(g.destination_id, 400, 300);
      return `
        <div class="card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column; cursor: pointer;" onclick="openDetail('${g.destination_id}')">
          <div style="height: 160px; background: #e2e8f0 url('${bgImg}') center/cover; position: relative;">
            <div style="position: absolute; top: 0.75rem; right: 0.75rem; background: rgba(255,255,255,0.9); padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: bold; color: #15803d;">
              ${g.crowd_category} Crowd
            </div>
            <img src="${bgImg}" alt="${g.name}" style="display:none;" onerror="this.previousElementSibling.style.display='none';" />
          </div>
          <div style="padding: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <h3 style="font-size: 1.25rem; margin: 0; color: var(--text-main);">${g.name}</h3>
              <span style="font-weight: bold; color: #b45309; font-size: 0.9rem;">★ ${g.quality_rating}</span>
            </div>
            <p style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 1rem;">${g.reason}</p>
            <div style="font-size: 0.8rem; color: var(--brand); font-weight: 500;">Gem Score: ${g.hidden_gem_score}</div>
          </div>
        </div>
      `;
    }).join("");
  } catch (err) {
    grid.innerHTML = "";
    errDiv.textContent = `Error discovering hidden gems: ${err.message}`;
    errDiv.hidden = false;
  }
}

async function init() {
  try {
    const health = await apiGet("/health");
    setApiStatus(true, `${(health.inference_model || "AI").toUpperCase()} · Online`);

    document.getElementById("statModel").textContent = "Local Connect Engine";

    const railSub = document.querySelector(".intel-rail-sub");
    if (railSub) railSub.textContent = "Discover Authentic Experiences";

    destinations = await apiGet("/destinations");
    document.getElementById("statDestinations").textContent = destinations.length;
    document.getElementById("statUpdated").textContent = new Date().toLocaleTimeString("en-IN", {
      hour: "2-digit",
      minute: "2-digit",
    });

    renderDestinations();
    fetchHiddenGems();

  } catch (err) {
    setApiStatus(false, "Offline");
    document.getElementById("destinationsGrid").innerHTML = `
      <div class="error-message">
        <p><strong>Cannot connect to API</strong></p>
        <p style="margin-top:0.5rem">Run: <code>uvicorn api:app --reload</code></p>
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

// Category tabs click handler
document.getElementById("categoryTabs").addEventListener("click", (e) => {
  if (e.target.tagName === "BUTTON") {
    document.querySelectorAll("#categoryTabs button").forEach(b => b.classList.remove("active"));
    e.target.classList.add("active");
    if (selectedDest) {
       fetchLocalMarket(selectedDest.destination_id, e.target.getAttribute("data-cat"));
    }
  }
});

init();
