with open("frontend/js/app.js", "r") as f:
    js = f.read()

import re

clear_logic = """
  document.getElementById("forecastChart").innerHTML = "";
  document.getElementById("forecastTable").innerHTML = "";
  document.getElementById("detailConfidence").textContent = "—";
  document.getElementById("bestTimeDate").textContent = "—";
  document.getElementById("bestTimeDetail").textContent = "Analyzing 7-day forecast…";
  document.getElementById("bestTimeScore").textContent = "—";
  
  try {
"""

js = js.replace('  try {\n    const forecast = await apiGet(`/forecast/${destId}`);', clear_logic + '    const forecast = await apiGet(`/forecast/${destId}`);')

with open("frontend/js/app.js", "w") as f:
    f.write(js)
