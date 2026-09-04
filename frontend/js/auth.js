// auth.js - Handles login on index.html and session logic on ui1.html
const BASE_URL = "http://127.0.0.1:8000";

// Only run landing page logic if we are on index.html
if (window.location.pathname.endsWith("index.html") || window.location.pathname === "/" || window.location.pathname.endsWith("frontend/")) {
  
  // Check if already logged in -> redirect to main app (ui1.html)
  const token = localStorage.getItem("footprint_session");
  if (token) {
    fetch(`${BASE_URL}/auth/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    })
    .then(r => r.ok ? window.location.replace("ui1.html") : localStorage.removeItem("footprint_session"))
    .catch(() => {});
  }

  // Tabs logic
  const tabLogin = document.getElementById("tabLogin");
  const tabSignup = document.getElementById("tabSignup");
  const signupFields = document.getElementById("signupFields");
  const authTitle = document.getElementById("authTitle");
  const authSubtitle = document.getElementById("authSubtitle");
  let isSignup = false;

  if (tabLogin && tabSignup) {
    tabLogin.addEventListener("click", () => {
      isSignup = false;
      tabLogin.classList.add("active");
      tabSignup.classList.remove("active");
      signupFields.style.display = "none";
      authTitle.textContent = "Welcome Back";
      authSubtitle.textContent = "Log in to access your dashboard";
    });

    tabSignup.addEventListener("click", () => {
      isSignup = true;
      tabSignup.classList.add("active");
      tabLogin.classList.remove("active");
      signupFields.style.display = "block";
      authTitle.textContent = "Create Account";
      authSubtitle.textContent = "Sign up to start your journey";
    });
  }

  // Mobile OTP Logic
  let currentPhone = "";
  
  const reqForm = document.getElementById("otpRequestForm");
  if (reqForm) {
    reqForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const phone = document.getElementById("phoneInput").value.trim();
      const errEl = document.getElementById("reqError");
      const btn = document.getElementById("btnRequestOtp");
      errEl.style.display = "none";
      btn.disabled = true;
      btn.textContent = "Sending...";

      try {
        
        let reqBody = { phone_number: phone, is_signup: isSignup };
        if (isSignup) {
          reqBody.name = document.getElementById("nameInput").value.trim();
          reqBody.email = document.getElementById("emailInput").value.trim();
        }

        const res = await fetch(`${BASE_URL}/auth/otp/request`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(reqBody)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Failed to send OTP");

        currentPhone = phone;
        document.getElementById("panelRequest").style.display = "none";
        document.getElementById("panelVerify").style.display = "block";
        
        // Show demo hint if in demo mode
        if (data.demo_otp) {
          document.getElementById("demoOtpHint").textContent = `DEMO MODE: Your OTP is ${data.demo_otp}`;
        }
      } catch (err) {
        errEl.textContent = err.message;
        errEl.style.display = "block";
      } finally {
        btn.disabled = false;
        btn.textContent = "Send OTP";
      }
    });
  }

  const verForm = document.getElementById("otpVerifyForm");
  if (verForm) {
    verForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const otp = document.getElementById("otpInput").value.trim();
      const errEl = document.getElementById("verError");
      const btn = document.getElementById("btnVerifyOtp");
      errEl.style.display = "none";
      btn.disabled = true;
      btn.textContent = "Verifying...";

      try {
        const res = await fetch(`${BASE_URL}/auth/otp/verify`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ phone_number: currentPhone, otp_code: otp })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Invalid OTP");

        localStorage.setItem("footprint_session", data.session_token);
        window.location.href = "ui1.html";
      } catch (err) {
        errEl.textContent = err.message;
        errEl.style.display = "block";
      } finally {
        btn.disabled = false;
        btn.textContent = "Verify & Login";
      }
    });
  }

  const btnBack = document.getElementById("btnBackToPhone");
  if (btnBack) {
    btnBack.addEventListener("click", (e) => {
      e.preventDefault();
      document.getElementById("panelVerify").style.display = "none";
      document.getElementById("panelRequest").style.display = "block";
      document.getElementById("otpInput").value = "";
    });
  }
}

// Google Sign-In Callback
function handleGoogleCredentialResponse(response) {
  const errEl = document.getElementById("googleError");
  if (errEl) errEl.style.display = "none";
  
  fetch(`${BASE_URL}/auth/google/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_token: response.credential })
  })
  .then(res => res.json().then(data => ({ok: res.ok, data})))
  .then(({ok, data}) => {
    if (!ok) throw new Error(data.detail || "Google authentication failed");
    localStorage.setItem("footprint_session", data.session_token);
    window.location.href = "ui1.html";
  })
  .catch(err => {
    if (errEl) {
      errEl.textContent = err.message;
      errEl.style.display = "block";
    }
  });
}

// Hub logic
if (window.location.pathname.endsWith("hub.html")) {
  const btnLogout = document.getElementById("btnLogout");
  if (btnLogout) {
    btnLogout.addEventListener("click", () => {
      localStorage.removeItem("footprint_session");
      window.location.replace("index.html");
    });
  }

  // Load user name
  const token = localStorage.getItem("footprint_session");
  if (token) {
    fetch(`${BASE_URL}/auth/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => {
      if (data.user && data.user.name) {
        document.getElementById("userName").textContent = `Welcome, ${data.user.name}`;
      }
    })
    .catch(() => {});
  }
}
