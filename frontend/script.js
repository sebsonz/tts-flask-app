document.getElementById("speakBtn").addEventListener("click", async () => {
    const text = document.getElementById("textInput").value.trim();
    if (!text) {
        alert("Veuillez entrer un texte !");
        return;
    }

    const res = await fetch("/speak", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await res.json();

    if (data.audioUrl) {
        const audio = document.getElementById("audioPlayer");
        audio.src = data.audioUrl;
        audio.play();
    } else {
        alert("Erreur : " + (data.error || "Audio non généré"));
    }
});
