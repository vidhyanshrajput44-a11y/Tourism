with open("frontend/js/app.js", "r") as f:
    js = f.read()

js = js.replace("""  } catch (err) {
    setApiStatus(false, "Offline");
    document.getElementById("destinationsGrid").innerHTML = `
      <div class="error-message">
        <p><strong>Cannot connect to API</strong></p>
        <p style="margin-top:0.5rem">Run: <code>uvicorn api:app --reload</code></p>
        <p style="margin-top:0.5rem"><a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a></p>
      </div>`;
  }""", """  } catch (err) {
    console.error("Init Error:", err);
    try { setApiStatus(false, "Offline"); } catch(e) {}
    try {
      document.getElementById("destinationsGrid").innerHTML = `
        <div class="error-message">
          <p><strong>API Error: ${err.message}</strong></p>
        </div>`;
    } catch(e) {}
  }""")

with open("frontend/js/app.js", "w") as f:
    f.write(js)
print("Patched app.js")
