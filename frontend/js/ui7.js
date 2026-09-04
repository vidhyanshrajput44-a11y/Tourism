let conversationHistory = [];
let conversationId = "conv_" + Math.random().toString(36).substr(2, 9);

async function fetchSampleQuestions() {
  const container = document.getElementById("sampleQuestions");
  try {
    const questions = await apiGet("/chat/sample-questions");
    container.innerHTML = questions.map(q => `
      <button class="sample-q-btn" style="background: white; border: 1px solid var(--border); padding: 0.5rem 1rem; border-radius: 999px; font-size: 0.85rem; color: var(--text-main); cursor: pointer; transition: all 0.2s; white-space: nowrap;">
        ${q}
      </button>
    `).join("");

    // Add click listeners
    document.querySelectorAll(".sample-q-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const input = document.getElementById("chatInput");
        input.value = btn.textContent.trim();
        document.getElementById("chatForm").dispatchEvent(new Event("submit"));
      });
    });
  } catch (err) {
    console.error("Failed to load sample questions:", err);
  }
}

function appendMessage(role, text, sources = []) {
  const historyEl = document.getElementById("chatHistory");
  const isUser = role === "user";
  
  const bubbleDiv = document.createElement("div");
  bubbleDiv.style.display = "flex";
  bubbleDiv.style.gap = "1rem";
  bubbleDiv.style.maxWidth = "85%";
  if (isUser) {
    bubbleDiv.style.marginLeft = "auto";
    bubbleDiv.style.flexDirection = "row-reverse";
  }

  // Avatar
  const avatarDiv = document.createElement("div");
  avatarDiv.style.width = "36px";
  avatarDiv.style.height = "36px";
  avatarDiv.style.borderRadius = "50%";
  avatarDiv.style.display = "flex";
  avatarDiv.style.alignItems = "center";
  avatarDiv.style.justifyContent = "center";
  avatarDiv.style.flexShrink = "0";
  
  if (isUser) {
    avatarDiv.style.background = "#e2e8f0";
    avatarDiv.style.color = "#475569";
    avatarDiv.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`;
  } else {
    avatarDiv.style.background = "var(--brand)";
    avatarDiv.style.color = "white";
    avatarDiv.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>`;
  }

  // Message Box
  const msgBox = document.createElement("div");
  msgBox.style.background = isUser ? "var(--brand)" : "white";
  msgBox.style.color = isUser ? "white" : "var(--text-main)";
  msgBox.style.border = isUser ? "none" : "1px solid var(--border)";
  msgBox.style.padding = "1rem 1.25rem";
  msgBox.style.borderRadius = isUser ? "12px 12px 0 12px" : "0 12px 12px 12px";
  msgBox.style.fontSize = "0.95rem";
  msgBox.style.lineHeight = "1.5";
  msgBox.style.boxShadow = "0 1px 2px rgba(0,0,0,0.05)";
  
  // Render markdown-ish breaks (simple replacement)
  msgBox.innerHTML = text.replace(/\n/g, "<br>");
  
  // Add sources pills if assistant
  if (!isUser && sources.length > 0) {
    const sourcesDiv = document.createElement("div");
    sourcesDiv.style.marginTop = "0.75rem";
    sourcesDiv.style.paddingTop = "0.75rem";
    sourcesDiv.style.borderTop = "1px solid #e2e8f0";
    sourcesDiv.style.display = "flex";
    sourcesDiv.style.flexWrap = "wrap";
    sourcesDiv.style.gap = "0.4rem";
    
    const label = document.createElement("span");
    label.textContent = "Sources:";
    label.style.fontSize = "0.75rem";
    label.style.color = "var(--text-muted)";
    label.style.display = "flex";
    label.style.alignItems = "center";
    sourcesDiv.appendChild(label);
    
    sources.forEach(src => {
      const pill = document.createElement("span");
      pill.textContent = src;
      pill.style.background = "#f1f5f9";
      pill.style.color = "#475569";
      pill.style.padding = "0.1rem 0.5rem";
      pill.style.borderRadius = "999px";
      pill.style.fontSize = "0.7rem";
      pill.style.fontWeight = "600";
      sourcesDiv.appendChild(pill);
    });
    
    msgBox.appendChild(sourcesDiv);
  }

  bubbleDiv.appendChild(avatarDiv);
  bubbleDiv.appendChild(msgBox);
  
  historyEl.appendChild(bubbleDiv);
  historyEl.scrollTop = historyEl.scrollHeight;
  
  // Save to history
  conversationHistory.push({ role, content: text });
}

document.getElementById("chatForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const inputEl = document.getElementById("chatInput");
  const text = inputEl.value.trim();
  if (!text) return;
  
  const errDiv = document.getElementById("chatError");
  errDiv.hidden = true;
  
  // Hide sample questions on first message
  document.getElementById("sampleQuestions").hidden = true;
  
  // User message
  appendMessage("user", text);
  inputEl.value = "";
  
  // Show typing indicator
  const btnSend = document.getElementById("btnSend");
  btnSend.disabled = true;
  btnSend.style.opacity = "0.5";
  btnSend.innerHTML = "Thinking...";
  
  try {
    const response = await apiPost("/chat/message", {
      user_query: text,
      conversation_id: conversationId,
      conversation_history: conversationHistory.slice(0, -1) // exclude the just-added user message
    });
    
    appendMessage("assistant", response.answer, response.sources_used);
  } catch (err) {
    errDiv.textContent = `Error: ${err.message}`;
    errDiv.hidden = false;
  } finally {
    btnSend.disabled = false;
    btnSend.style.opacity = "1";
    btnSend.innerHTML = `Send <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>`;
  }
});

document.getElementById("btnRefreshKb").addEventListener("click", async (e) => {
  const btn = e.currentTarget;
  const originalHtml = btn.innerHTML;
  btn.innerHTML = `Syncing...`;
  btn.disabled = true;
  
  try {
    await apiPost("/chat/refresh-knowledge-base", {});
    setTimeout(() => {
      btn.innerHTML = `✅ Synced`;
      document.getElementById("statUpdated").textContent = new Date().toLocaleTimeString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
      });
      setTimeout(() => {
        btn.innerHTML = originalHtml;
        btn.disabled = false;
      }, 2000);
    }, 1000);
  } catch (err) {
    alert("Failed to sync knowledge base");
    btn.innerHTML = originalHtml;
    btn.disabled = false;
  }
});

async function init() {
  try {
    const health = await apiGet("/health");
    setApiStatus(true, `RAG ENGINE · Online`);
    
    document.getElementById("statUpdated").textContent = new Date().toLocaleTimeString("en-IN", {
      hour: "2-digit",
      minute: "2-digit",
    });

    fetchSampleQuestions();

  } catch (err) {
    setApiStatus(false, "Offline");
    document.getElementById("chatError").textContent = "Cannot connect to API. Run uvicorn api:app --reload";
    document.getElementById("chatError").hidden = false;
  }
}

init();

// --- API Helpers (copied from shared logic) ---
async function apiGet(endpoint) {
  const res = await fetch(`http://127.0.0.1:8000${endpoint}`);
  if (!res.ok) throw new Error(`API error: ${res.statusText}`);
  return await res.json();
}

async function apiPost(endpoint, payload) {
  const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return await res.json();
}

function setApiStatus(isOnline, text) {
  const statusEl = document.getElementById("apiStatus");
  if (!statusEl) return;
  statusEl.className = isOnline ? "nav-status online" : "nav-status offline";
  statusEl.querySelector(".status-label").textContent = text;
}
