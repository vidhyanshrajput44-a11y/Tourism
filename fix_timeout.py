with open("frontend/js/app.js", "r") as f:
    js = f.read()

import re

new_tomtom = """async function fetchTomTomCrowdIndex(lat, lon) {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3000);
        const url = `https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key=${TOMTOM_API_KEY}&point=${lat},${lon}`;
        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(timeoutId);
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
}"""

js = re.sub(r'async function fetchTomTomCrowdIndex.*?return "Data unavailable";\n    }\n}', new_tomtom, js, flags=re.DOTALL)

with open("frontend/js/app.js", "w") as f:
    f.write(js)
