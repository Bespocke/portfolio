document.getElementById('yes-button').addEventListener('click', function() {
    // Rendre le fond flou
    document.getElementById('background').classList.add('blurred');

    // Animer le titre pour qu'il se déplace vers le haut
    const title = document.getElementById('shiny-title');
    const yesButton = document.getElementById('yes-button');
    const linkButtons = document.getElementById('link-buttons');

    // Animation du titre
    title.style.fontSize = "2em";
    title.style.transform = `translateY(-${window.innerHeight * 0.3}px)`;

    // Masquer le bouton "oui"
    yesButton.style.opacity = "0";
    setTimeout(() => yesButton.style.display = 'none', 500);

    linkButtons.classList.remove('hidden');
    // Animation du conteneur des boutons pour remonter vers le centre
    linkButtons.style.bottom = "40%"; // Remonte au centre de la page

    // Apparition progressive des boutons avec décalage
    const buttons = Array.from(linkButtons.children);
    buttons.forEach((button, index) => {
        setTimeout(() => {
            button.style.opacity = "1";
        }, index * 150); // Délai entre chaque bouton
    });
});


