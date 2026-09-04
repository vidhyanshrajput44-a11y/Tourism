with open("frontend/js/ui6.js", "r") as f:
    js = f.read()

new_render = """function renderHotels(hotels, gridEl) {
  if (!hotels || hotels.length === 0) {
    gridEl.innerHTML = `<p style="grid-column: 1 / -1; color: var(--text-muted);">No hotels found.</p>`;
    return;
  }

  gridEl.innerHTML = hotels.map(h => {
    let catColor = h.demand_category === "Low" ? "#15803d" : (h.demand_category === "Medium" ? "#b45309" : "#b91c1c");
    let catBg = h.demand_category === "Low" ? "#dcfce7" : (h.demand_category === "Medium" ? "#fef3c7" : "#fee2e2");
    
    // Use image from backend or fallback to Picsum
    const photoUrl = h.image_url || `https://picsum.photos/seed/${h.hotel_id}/400/200`;

    // MakeMyTrip link
    const mmtLink = h.mmt_link || `https://www.makemytrip.com/hotels/`;

    // Use selectedDest.name as the location if available
    const locationName = selectedDest ? selectedDest.name : "Local";

    return `
      <a href="${mmtLink}" target="_blank" style="text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s; background: white; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 15px -3px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='none'; this.style.boxShadow='none';">
        <div style="height: 160px; background: #e2e8f0 url('${photoUrl}') center/cover; position: relative;">
          <div style="position: absolute; bottom: 8px; left: 8px; background: rgba(0,0,0,0.7); color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem;">
            ₹${h.base_price.toLocaleString('en-IN')} / night
          </div>
        </div>
        <div style="padding: 1rem; flex-grow: 1; display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: start;">
            <h4 style="font-size: 1.1rem; color: var(--text-main); margin-bottom: 0.25rem;">${h.name}</h4>
            <span style="background: ${catBg}; color: ${catColor}; padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; white-space: nowrap; margin-left: 0.5rem;">
              ${h.demand_category}
            </span>
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">
            📍 Near ${locationName} • ${h.star_rating} Star
          </div>
          
          <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem; display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; margin-top: auto;">
            <div style="font-size: 0.85rem; color: var(--text-secondary);">Predicted Occupancy</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: ${catColor};">${h.current_occupancy}%</div>
          </div>
          
          <div style="background: #eef2ff; color: #4338ca; border-radius: 6px; padding: 0.5rem; text-align: center; font-weight: 600; font-size: 0.9rem; margin-top: auto; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            Book on MakeMyTrip
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          </div>
        </div>
      </a>
    `;
  }).join("");
}"""

import re
# Find function renderHotels(hotels, gridEl) { ... }
js = re.sub(r'function renderHotels\(hotels, gridEl\).*?\n\}', new_render, js, flags=re.DOTALL)

with open("frontend/js/ui6.js", "w") as f:
    f.write(js)
print("ui6.js updated")
