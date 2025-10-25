const textInput = document.getElementById("textInput");
const langSelect = document.getElementById("langSelect");
const voiceSelect = document.getElementById("voiceSelect");
const speedSelect = document.getElementById("speedSelect");
const playBtn = document.getElementById("playBtn");
const downloadBtn = document.getElementById("downloadBtn");
const clearBtn = document.getElementById("clearBtn");
const statusEl = document.getElementById("status");
const audioPlayer = document.getElementById("audioPlayer");
const historyList = document.getElementById("historyList");

let lastAudioUrl = null;
let lastFilename = null;

// helper pour afficher statut
function setStatus(txt, isError = false) {
  statusEl.textContent = txt;
  statusEl.style.color = isError ? "#ff6b6b" : "#2b2b2b";
}

async function fetchHistory() {
  try {
    const res = await fetch("/history");
    const items = await res.json();
    historyList.innerHTML = "";
    if (!items || items.length === 0) {
      historyList.innerHTML = "<li class='empty'>Aucune lecture récente</li>";
      return;
    }
    items.forEach(entry => {
      const li = document.createElement("li");
      li.className = "history-item";
      const textPreview = entry.text.length > 80 ? entry.text.slice(0, 80) + "…" : entry.text;
      li.innerHTML = `
        <div class="h-left">
          <div class="h-text">${escapeHtml(textPreview)}</div>
          <div class="h-meta">${new Date(entry.timestamp).toLocaleString()} • ${entry.lang}</div>
        </div>
        <div class="h-actions">
          <button class="small" data-url="${entry.audio_url}" data-fname="${entry.filename}">▶</button>
          <a class="small" href="${entry.audio_url}" download>⬇</a>
        </div>
      `;
      historyList.appendChild(li);
    });

    // event listeners pour play buttons
    document.querySelectorAll(".history-item .h-actions button").forEach(btn => {
      btn.addEventListener("click", () => {
        const url = btn.getAttribute("data-url");
        playFromUrl(url);
      });
    });
  } catch (e) {
    console.error("History fetch error", e);
  }
}

function escapeHtml(unsafe) {
  return unsafe.replace(/[&<"'>]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[m]));
}

async function ttsRequest(text, lang) {
  const body = { text, lang };
  const res = await fetch("/tts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
}

function applyPlaybackSettings(elem, speed, gender) {
  // Speed multiplie playbackRate
  elem.playbackRate = speed;
  // Simuler pitch/genre en ajustant le playbackRate légèrement
  // female -> slight higher playbackRate, male -> slight lower playbackRate
  if (gender === "female") {
    elem.playbackRate = elem.playbackRate * 1.03;
  } else if (gender === "male") {
    elem.playbackRate = elem.playbackRate * 0.96;
  }
}

async function playFromUrl(url) {
  try {
    audioPlayer.src = url;
    // appliquer settings actuelles
    const speed = parseFloat(speedSelect.value || "1.0");
    const gender = voiceSelect.value || "female";

    // wait until can play
    audioPlayer.oncanplaythrough = () => {
      applyPlaybackSettings(audioPlayer, speed, gender);
      audioPlayer.play().catch(err => {
        console.warn("Play blocked", err);
        setStatus("🔇 Lecture bloquée par le navigateur — cliquez pour autoriser", true);
      });
    };
    audioPlayer.onerror = () => {
      setStatus("Erreur lecture audio", true);
    };
    // load
    audioPlayer.load();
    lastAudioUrl = url;
    lastFilename = url.split("/").pop();
    downloadBtn.disabled = false;
  } catch (e) {
    console.error(e);
    setStatus("Erreur lors de la lecture", true);
  }
}

playBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();
  const lang = langSelect.value;
  if (!text) {
    setStatus("⚠️ Saisis du texte avant de lire", true);
    return;
  }
  setStatus("⏳ Génération en cours...");
  downloadBtn.disabled = true;

  try {
    const result = await ttsRequest(text, lang);
    if (result.error) {
      setStatus("Erreur : " + result.error, true);
      return;
    }
    // serveur renvoie audio_url et filename
    const audioUrl = result.audio_url;
    await fetchHistory(); // refresh history
    setStatus("✅ Audio prêt — lecture...");
    await playFromUrl(audioUrl);
  } catch (e) {
    console.error(e);
    setStatus("Erreur réseau lors de la génération", true);
  }
});

// download: ouvre le fichier (avec attribut download)
downloadBtn.addEventListener("click", () => {
  if (!lastAudioUrl) return;
  const a = document.createElement("a");
  a.href = lastAudioUrl;
  a.download = lastFilename || "tts.mp3";
  document.body.appendChild(a);
  a.click();
  a.remove();
});

// clear textarea
clearBtn.addEventListener("click", () => {
  textInput.value = "";
  setStatus("Prêt");
});

// load initial history on page open
window.addEventListener("load", () => {
  fetchHistory();
  setStatus("Prêt");
});
