with open("frontend/js/app.js", "r") as f:
    js = f.read()

open_detail_hook = """
  if (selectedDest.lat && selectedDest.lon) {
      const mapCard = document.querySelector('.map-card');
      if (mapCard) mapCard.hidden = false;
      setTimeout(() => initUi1Map(selectedDest.lat, selectedDest.lon, selectedDest.name), 100);
  } else {
      const mapCard = document.querySelector('.map-card');
      if (mapCard) mapCard.hidden = true;
  }
"""

if "mapCard.hidden" not in js:
    js = js.replace('setHeroImage(selectedDest.destination_id);', 'setHeroImage(selectedDest.destination_id);\n' + open_detail_hook)
    with open("frontend/js/app.js", "w") as f:
        f.write(js)
    print("Hook added")
else:
    print("Already added")
