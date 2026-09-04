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
};

function destImageUrl(destId, width, height) {
  const meta = DEST_IMAGES[destId];
  if (!meta) return "";
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

  freshImg.onload = () => heroEl.classList.remove("hero-fallback");
  freshImg.onerror = () => heroEl.classList.add("hero-fallback");

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
// Detail / intelligence panel
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
  document.getElementById("gaugeScore").textContent = score;
  updateScaleMarker(score);

  const cls = levelClass(selectedDest.current_crowd_category, score);
  const badge = document.getElementById("detailBadge");
  badge.textContent = displayLevel(selectedDest.current_crowd_category, score);
  badge.className = `crowd-badge ${cls}`;

  document.getElementById("detailCapacity").textContent =
    formatNumber(selectedDest.max_capacity);

  setHeroImage(selectedDest.destination_id);

  renderDestinations();

  const today = new Date().toISOString().split("T")[0];
  const dateInput = document.getElementById("predictDate");
  dateInput.min = today;
  const maxDate = new Date();
  maxDate.setDate(maxDate.getDate() + 30);
  dateInput.max = maxDate.toISOString().split("T")[0];
  dateInput.value = today;

  document.getElementById("predictResult").hidden = true;

  if (window.innerWidth <= 768) {
    document.getElementById("intelPanel").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  try {
    const forecast = await apiGet(`/forecast/${destId}`);
    currentForecast = forecast;
    renderForecast(forecast);

    const todayForecast = forecast[0];
    if (todayForecast) {
      document.getElementById("detailConfidence").textContent =
        `${Math.round(todayForecast.confidence * 100)}%`;
    }

    updateBestTime(forecast);
  } catch (err) {
    console.error(err);
  }
}

function renderForecast(forecast) {
  const chart = document.getElementById("forecastChart");
  const tbody = document.getElementById("forecastTable");

  chart.innerHTML = forecast
    .map((f) => {
      const height = Math.max(6, (f.crowd_score / 100) * 140);
      const cls = levelClass(f.crowd_category, f.crowd_score);
      const dayShort = f.day_of_week.slice(0, 3);
      const dateShort = f.date.slice(5);
      return `
      <div class="bar-col${f.is_weekend ? " bar-weekend" : ""}">
        <div class="bar-wrap">
          <span class="bar-score">${f.crowd_score}</span>
          <div class="bar ${cls}" style="height:${height}px" title="Index: ${f.crowd_score}"></div>
        </div>
        <span class="bar-label">${dateShort}</span>
        <span class="bar-day">${dayShort}</span>
      </div>`;
    })
    .join("");

  tbody.innerHTML = forecast
    .map((f) => {
      const cls = levelClass(f.crowd_category, f.crowd_score);
      const level = displayLevel(f.crowd_category, f.crowd_score);
      return `
    <tr class="${f.is_weekend ? "weekend-row" : ""}">
      <td>${f.date}</td>
      <td>${f.day_of_week}${f.is_holiday ? " · Holiday" : ""}</td>
      <td>${formatNumber(f.predicted_footfall)}</td>
      <td><strong>${f.crowd_score}</strong></td>
      <td><span class="crowd-badge ${cls}">${level}</span></td>
    </tr>`;
    })
    .join("");
}

// ---------------------------------------------------------------------------
// Custom prediction (unchanged API)
// ---------------------------------------------------------------------------
async function handlePredict(e) {
  e.preventDefault();
  if (!selectedDest) return;

  const dateVal = document.getElementById("predictDate").value;
  const weather = document.getElementById("predictWeather").value;

  try {
    const result = await apiPost("/predict", {
      destination_id: selectedDest.destination_id,
      date: dateVal,
      weather_condition: weather,
    });

    document.getElementById("predictResult").hidden = false;
    document.getElementById("resultDate").textContent = result.date;
    document.getElementById("resultFootfall").textContent =
      `Expected footfall: ${formatNumber(result.predicted_footfall)} · Crowd index: ${result.crowd_score}/100`;

    const cls = levelClass(result.crowd_category, result.crowd_score);
    const badge = document.getElementById("resultBadge");
    badge.textContent = displayLevel(result.crowd_category, result.crowd_score);
    badge.className = `crowd-badge ${cls}`;
  } catch (err) {
    alert(err.message || "Prediction failed. Is the API running?");
  }
}

function clearSelection() {
  selectedDest = null;
  document.getElementById("detailSection").hidden = true;
  document.getElementById("emptyState").hidden = false;
  document.getElementById("intelPanel").classList.remove("has-selection");
  renderDestinations();
}

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------
async function init() {
  try {
    const health = await apiGet("/health");
    setApiStatus(true, `${(health.inference_model || "AI").toUpperCase()} · Online`);

    document.getElementById("statModel").textContent =
      (health.inference_model || "AI").toUpperCase();

    const railSub = document.querySelector(".intel-rail-sub");
    if (railSub) railSub.textContent = (health.inference_model || "XGBoost").toUpperCase();

    destinations = await apiGet("/destinations");
    document.getElementById("statDestinations").textContent = destinations.length;
    document.getElementById("statUpdated").textContent = new Date().toLocaleTimeString("en-IN", {
      hour: "2-digit",
      minute: "2-digit",
    });

    renderDestinations();

    // Open first destination by default — image + forecast visible immediately
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
document.getElementById("predictForm").addEventListener("submit", handlePredict);

init();
