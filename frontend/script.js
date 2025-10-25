const speakBtn = document.getElementById("speakBtn");
const stopBtn = document.getElementById("stopBtn");
const downloadBtn = document.getElementById("downloadBtn");
const textInput = document.getElementById("textInput");
const languageSelect = document.getElementById("languageSelect");
const voiceSelect = document.getElementById("voiceSelect");
const audioPlayer = document.getElementById("audioPlayer");

let currentAudio = "";

speakBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();
  const voice = voiceSelect.value;

  if (!text) {
    alert("Veuillez écrire un texte à lire !");
    return;
  }

  const response = await fetch("/speak", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice })
  });

  const data = await response.json();

  if (data.audio) {
    currentAudio = data.audio;
    audioPlayer.src = `/audio/${data.audio}`;
    audioPlayer.play();
  } else {
    alert("Erreur : " + data.error);
  }
});

stopBtn.addEventListener("click", () => {
  audioPlayer.pause();
  audioPlayer.currentTime = 0;
});

downloadBtn.addEventListener("click", () => {
  if (currentAudio) {
    window.open(`/audio/${currentAudio}`, "_blank");
  } else {
    alert("Aucun audio à télécharger !");
  }
});
