import re

with open("frontend/js/auth-guard.js", "r") as f:
    content = f.read()

# Add logic to extract user name and inject it
find_str = """    if (!res.ok) {
      // Invalid/expired token
      localStorage.removeItem("footprint_session");
      window.location.href = "index.html";
    }
    
    // Auth is valid, allow page to continue loading"""

replace_str = """    if (!res.ok) {
      // Invalid/expired token
      localStorage.removeItem("footprint_session");
      window.location.href = "index.html";
      return;
    }
    
    // Auth is valid, extract data
    const data = await res.json();
    if (data.user && data.user.name) {
      // Small timeout to ensure DOM is ready
      setTimeout(() => {
        const nameEl = document.getElementById("navUserName");
        if (nameEl) {
          nameEl.textContent = "Hi, " + data.user.name;
        }
      }, 100);
    }
    
    // allow page to continue loading"""

content = content.replace(find_str, replace_str)

with open("frontend/js/auth-guard.js", "w") as f:
    f.write(content)

print("Auth guard updated.")
