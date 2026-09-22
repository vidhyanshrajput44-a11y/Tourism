with open("frontend/js/app.js", "r") as f:
    js = f.read()

import re

fixed = """function updateScaleMarker(score) {
  const marker = document.getElementById("scaleMarker");
  if (typeof score !== 'number') {
      marker.style.display = 'none';
      return;
  }
  marker.style.display = 'block';
  marker.style.left = `${Math.min(100, Math.max(0, score))}%`;
}"""

js = re.sub(r'function updateScaleMarker.*?\}\%\`;\n\}', fixed, js, flags=re.DOTALL)

with open("frontend/js/app.js", "w") as f:
    f.write(js)
