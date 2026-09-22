import re

with open("frontend/js/app.js", "r") as f:
    js = f.read()

# 1. Add TomTom API Key & functions
tomtom_code = """
const TOMTOM_API_KEY = "01LQYrezFaLQbsmT3SoD4XVwxUfsmqsk"; // used only for Kempty Falls and Robber's Cave

function traffic_to_crowd_signal(currentSpeed, freeFlowSpeed) {
    if (freeFlowSpeed == null || freeFlowSpeed === 0 || currentSpeed == null) return null;
    let ratio = currentSpeed / freeFlowSpeed;
    ratio = Math.max(0, Math.min(1, ratio));
    return Math.round((1 - ratio) * 100);
}

async function fetchTomTomCrowdIndex(lat, lon) {
    try {
        const url = `https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key=${TOMTOM_API_KEY}&point=${lat},${lon}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("TomTom API failed");
        const data = await response.json();
        
        if (data && data.flowSegmentData) {
            const crowdIndex = traffic_to_crowd_signal(
                data.flowSegmentData.currentSpeed,
                data.flowSegmentData.freeFlowSpeed
            );
            if (crowdIndex !== null) return crowdIndex;
        }
        console.warn(`Low coverage for TomTom at ${lat},${lon}.`);
        return "Data unavailable";
    } catch (e) {
        console.warn(`Error fetching TomTom data for ${lat},${lon}:`, e);
        return "Data unavailable";
    }
}
"""

if "TOMTOM_API_KEY" not in js:
    js = js.replace('const API_BASE = window.location.origin.includes("8000")\n  ? window.location.origin\n  : "http://127.0.0.1:8000";', 'const API_BASE = window.location.origin.includes("8000")\n  ? window.location.origin\n  : "http://127.0.0.1:8000";\n' + tomtom_code)

# 2. Update DEST_IMAGES
dest_imgs_update = """  kempty_falls: {
    photoUrl: "images/kempty_falls.jpg",
    alt: "Kempty Falls, Mussoorie",
    credit: "Local Image",
    creditUrl: "#"
  },
  robbers_cave: {
    photoUrl: "images/robbers_cave.jpg",
    alt: "Robber's Cave, Dehradun",
    credit: "Local Image",
    creditUrl: "#"
  },"""
if "kempty_falls" not in js:
    js = js.replace('  mysore_palace: {', dest_imgs_update + '\n  mysore_palace: {')

# 3. Update destImageUrl
new_destImageUrl = """function destImageUrl(destId, width, height) {
  const meta = DEST_IMAGES[destId];
  if (meta && meta.photoUrl) return meta.photoUrl;
  if (!meta) return `https://picsum.photos/seed/${destId}/${width}/${height}`;
  // Unique sig per destination prevents browser/CDN serving a stale cached image
  return `https://images.unsplash.com/${meta.photo}?auto=format&fit=crop&w=${width}&h=${height}&q=80&ixlib=rb-4.0.3&sig=${encodeURIComponent(destId)}`;
}"""
js = re.sub(r'function destImageUrl.*?}', new_destImageUrl, js, flags=re.DOTALL, count=1)

# 4. Update init() to push destinations
init_add = """
    const kempty_crowd = await fetchTomTomCrowdIndex(30.4598, 78.1652);
    destinations.push({
        destination_id: "kempty_falls",
        name: "Kempty Falls",
        city: "Mussoorie",
        state: "Uttarakhand",
        max_capacity: 10000,
        current_crowd_score: kempty_crowd,
        current_crowd_category: typeof kempty_crowd === 'number' ? (kempty_crowd < 40 ? "Low" : (kempty_crowd < 70 ? "Medium" : "High")) : "N/A",
        lat: 30.4598,
        lon: 78.1652
    });

    const robbers_crowd = await fetchTomTomCrowdIndex(30.3777, 78.0346);
    destinations.push({
        destination_id: "robbers_cave",
        name: "Robber's Cave",
        city: "Dehradun",
        state: "Uttarakhand",
        max_capacity: 5000,
        current_crowd_score: robbers_crowd,
        current_crowd_category: typeof robbers_crowd === 'number' ? (robbers_crowd < 40 ? "Low" : (robbers_crowd < 70 ? "Medium" : "High")) : "N/A",
        lat: 30.3777,
        lon: 78.0346
    });
"""
if "kempty_falls" not in js.split('destinations = await apiGet("/destinations");')[1]:
    js = js.replace('destinations = await apiGet("/destinations");', 'destinations = await apiGet("/destinations");\n' + init_add)

# 5. Fix score rendering to handle strings like "Data unavailable"
score_replace = '<span class="score">${typeof d.current_crowd_score === \'number\' ? d.current_crowd_score + \'<span class="score-max">/100</span>\' : `<span style="font-size:12px;font-weight:normal;">${d.current_crowd_score}</span>`}</span>'
js = re.sub(r'<span class="score">\$\{d\.current_crowd_score\}<span class="score-max">/100</span></span>', score_replace, js)

# 6. Add map init logic
map_logic = """
let ui1Map = null;
let ui1Marker = null;

function initUi1Map(lat, lon, title) {
    if (!document.getElementById("ui1Map")) return;
    if (!ui1Map) {
        ui1Map = L.map('ui1Map').setView([lat, lon], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(ui1Map);
    } else {
        ui1Map.setView([lat, lon], 13);
    }
    
    if (ui1Marker) {
        ui1Marker.remove();
    }
    ui1Marker = L.marker([lat, lon]).addTo(ui1Map).bindPopup(`<b>${title}</b>`).openPopup();
}
"""
if "ui1Map = null" not in js:
    js = js + '\n' + map_logic

# Modify openDetail to call initUi1Map
open_detail_hook = """
  if (selectedDest.lat && selectedDest.lon) {
      document.querySelector('.map-card').hidden = false;
      setTimeout(() => initUi1Map(selectedDest.lat, selectedDest.lon, selectedDest.name), 100);
  } else {
      const mapCard = document.querySelector('.map-card');
      if (mapCard) mapCard.hidden = true;
  }
"""
if "initUi1Map" not in js.split('function openDetail')[1]:
    js = js.replace('setHeroImage(selectedDest.destination_id);', 'setHeroImage(selectedDest.destination_id);\n' + open_detail_hook)

with open("frontend/js/app.js", "w") as f:
    f.write(js)
print("Patched app.js successfully")
