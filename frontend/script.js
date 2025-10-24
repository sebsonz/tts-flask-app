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

        audio.oncanplaythrough = () => {
            audio.play().then(() => {
                status.textContent = "✅ Lecture terminée !";
            }).catch(err => {
                status.textContent = "🔇 Lecture bloquée par le navigateur. Cliquez pour autoriser le son.";
                console.log(err);
            });
        };

        audio.onerror = () => {
            status.textContent = "❌ Erreur de lecture audio.";
        };

    } catch (e) {
        status.textContent = "❌ Erreur de connexion au serveur.";
        console.error(e);
    }
}
