async function speak() {
    const text = document.getElementById("text").value.trim();
    const status = document.getElementById("status");

    if (!text) {
        alert("Veuillez saisir un texte !");
        return;
    }

    status.textContent = "⏳ Génération de la voix...";

    try {
        const response = await fetch("/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            const err = await response.json();
            status.textContent = "❌ Erreur : " + (err.error || "inconnue");
            return;
        }

        const blob = await response.blob();
        const audioURL = URL.createObjectURL(blob);
        const audio = new Audio(audioURL);
        audio.play();

        status.textContent = "✅ Lecture terminée !";
    } catch (e) {
        status.textContent = "❌ Erreur de connexion au serveur.";
    }
}
