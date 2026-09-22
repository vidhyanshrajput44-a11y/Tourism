with open("frontend/js/app.js", "r") as f:
    js = f.read()

# I will find the exact index of `function updateScaleMarker(score)` and `function updateBestTime`
start = js.find("function updateScaleMarker")
end = js.find("function updateBestTime")

fixed = """function updateScaleMarker(score) {
  const marker = document.getElementById("scaleMarker");
  if (typeof score !== 'number') {
      marker.style.display = 'none';
      return;
  }
  marker.style.display = 'block';
  marker.style.left = `${Math.min(100, Math.max(0, score))}%`;
}

"""
js = js[:start] + fixed + js[end:]

with open("frontend/js/app.js", "w") as f:
    f.write(js)
