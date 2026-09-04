// Lightweight auth guard for UI 1-7
(async function() {
  const token = localStorage.getItem("footprint_session");
  
  // If no token, redirect to login immediately
  if (!token) {
    window.location.href = "index.html";
    return;
  }
  
  // Verify token is still valid with backend
  try {
    const res = await fetch("http://127.0.0.1:8000/auth/me", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });
    
    if (!res.ok) {
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
    
    // allow page to continue loading
    // Optionally we could inject a "Logout" button into the nav if we want,
    // but the prompt asked for minimal changes. The hub.html will have the main logout.
  } catch (err) {
    console.error("Auth verification failed", err);
  }
})();
