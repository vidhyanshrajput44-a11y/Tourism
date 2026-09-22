// Lightweight auth guard for UI 1-7
(async function() {
  const token = localStorage.getItem("footprint_session");
  
  if (!token) {
    console.log("No footprint_session token found; running in guest mode.");
    return;
  }
  
  // Verify token is still valid with backend
  try {
    const apiBase = window.location.origin.includes("8000") ? window.location.origin : "http://127.0.0.1:8000";
    const res = await fetch(`${apiBase}/auth/me`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });
    
    if (!res.ok) {
      console.warn("Invalid footprint_session token.");
      return;
    }
    
    // Auth is valid, extract data
    const data = await res.json();
    if (data.user && data.user.name) {
      setTimeout(() => {
        const nameEl = document.getElementById("navUserName");
        if (nameEl) {
          nameEl.textContent = "Hi, " + data.user.name;
        }
      }, 100);
    }
  } catch (err) {
    console.error("Auth verification failed", err);
  }
})();
