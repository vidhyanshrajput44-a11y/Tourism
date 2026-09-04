import re

with open("frontend/js/auth.js", "r") as f:
    content = f.read()

# Replace tab logic
tab_logic_old = """  // Tabs logic
  const tabMobile = document.getElementById("tabMobile");
  const tabGoogle = document.getElementById("tabGoogle");
  const panelMobile = document.getElementById("panelMobile");
  const panelGoogle = document.getElementById("panelGoogle");

  if(tabMobile) {
    tabMobile.addEventListener("click", () => {
      tabMobile.classList.add("active");
      tabGoogle.classList.remove("active");
      panelMobile.classList.add("active");
      panelGoogle.classList.remove("active");
    });
  }

  if(tabGoogle) {
    tabGoogle.addEventListener("click", () => {
      tabGoogle.classList.add("active");
      tabMobile.classList.remove("active");
      panelGoogle.classList.add("active");
      panelMobile.classList.remove("active");
    });
  }"""
tab_logic_new = """  // Tabs logic
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
  }"""
content = content.replace(tab_logic_old, tab_logic_new)

# Replace OTP request logic
req_old = """        const res = await fetch(`${BASE_URL}/auth/otp/request`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ phone_number: phone })
        });"""
req_new = """        
        let reqBody = { phone_number: phone, is_signup: isSignup };
        if (isSignup) {
          reqBody.name = document.getElementById("nameInput").value.trim();
          reqBody.email = document.getElementById("emailInput").value.trim();
        }

        const res = await fetch(`${BASE_URL}/auth/otp/request`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(reqBody)
        });"""
content = content.replace(req_old, req_new)

# Replace panel hiding logic during OTP verify transition
panel_old = """        reqForm.style.display = "none";
        document.getElementById("otpVerifyForm").style.display = "block";"""
panel_new = """        document.getElementById("panelRequest").style.display = "none";
        document.getElementById("panelVerify").style.display = "block";"""
content = content.replace(panel_old, panel_new)

back_old = """      document.getElementById("otpVerifyForm").style.display = "none";
      document.getElementById("otpRequestForm").style.display = "block";"""
back_new = """      document.getElementById("panelVerify").style.display = "none";
      document.getElementById("panelRequest").style.display = "block";"""
content = content.replace(back_old, back_new)


with open("frontend/js/auth.js", "w") as f:
    f.write(content)
print("Auth.js updated.")
