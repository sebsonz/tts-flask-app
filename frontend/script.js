async function convertText() {
    const text = document.getElementById("text-input").value.trim();
    const player = document.getElementById("audio-player");
    const status = document.getElementById("status");

    if (!text) {
        status.innerText = "Veuillez entrer du texte.";
        return;
    }

    status.innerText = "Génération audio en cours...";
    player.src = "";

    try {
        const response = await fetch("/speak", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            status.innerText = "Erreur lors de la génération de la voix.";
            return;
        }

        const blob = await response.blob();
        const audioUrl = URL.createObjectURL(blob);
        player.src = audioUrl;
        player.play();

        status.innerText = "✅ Audio prêt !";
    } catch (error) {
        status.innerText = "Erreur réseau.";
        console.error(error);
    }
}
