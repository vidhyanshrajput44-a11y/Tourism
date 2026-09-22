with open("frontend/js/app.js", "r") as f:
    js = f.read()

import re
# The broken block starts with `function destImageUrl` and goes until `}` that is followed by `function setHeroImage`
fixed = """function destImageUrl(destId, width, height) {
  const meta = DEST_IMAGES[destId];
  if (meta && meta.photoUrl) return meta.photoUrl;
  if (!meta) return `https://picsum.photos/seed/${destId}/${width}/${height}`;
  // Unique sig per destination prevents browser/CDN serving a stale cached image
  return `https://images.unsplash.com/${meta.photo}?auto=format&fit=crop&w=${width}&h=${height}&q=80&ixlib=rb-4.0.3&sig=${encodeURIComponent(destId)}`;
}"""

js = re.sub(r'function destImageUrl.*?\}\s*function setHeroImage', fixed + '\n\nfunction setHeroImage', js, flags=re.DOTALL)

with open("frontend/js/app.js", "w") as f:
    f.write(js)
