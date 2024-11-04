let currentBlockIndex = 0;
const blocks = document.querySelectorAll('.block');
const introBlock = document.querySelector('.intro-block'); // Sélectionner le bloc d'introduction
const presentationBlock = document.querySelector('.presentation'); // Sélectionner le bloc de présentation
const introBlockHeight = introBlock.offsetHeight; // Récupérer la hauteur du bloc d'introduction
const presentationBlockHeight = presentationBlock.offsetHeight; // Récupérer la hauteur du bloc de présentation
const subblock = document.querySelector('.subtitles'); // Sélectionner sub
const subheight = subblock.offsetHeight; // Récupérer la hauteur du bloc de sub


// Fonction pour calculer le scrollThreshold en fonction de la hauteur de chaque bloc
function getScrollThreshold() {
    if (currentBlockIndex < blocks.length) {
        const blockHeight = blocks[currentBlockIndex].getBoundingClientRect().height; // Hauteur du bloc actuel
        let threshold = blockHeight; // Ajouter un supplément de 50 pixels

        // Ajustement pour le bloc 5 (indice 4)
        if (currentBlockIndex === 4) { // Les indices commencent à 0, donc 4 est le 5ème bloc
            threshold += blockHeight + subheight; // Ajouter la hauteur complète du bloc "Parcours"
        }

        // Ajout de la hauteur du bloc d'introduction et du bloc de présentation pour le premier bloc
        if (currentBlockIndex === 0) {
            threshold += introBlockHeight / 2; // Ajoute la hauteur du bloc d'introduction
            threshold += presentationBlockHeight; // Ajoute la hauteur du bloc de présentation
        }

        return threshold; // Retourne le seuil calculé
    }
    return 0; // Retourne 0 si tous les blocs ont été affichés
}

// Initialise le scrollThreshold
let scrollThreshold = getScrollThreshold();

// Fonction pour vérifier le défilement
function checkScroll() {
    if (window.scrollY > scrollThreshold) {
        if (currentBlockIndex < blocks.length) {
            blocks[currentBlockIndex].classList.add('visible'); // Rendre le bloc visible
            currentBlockIndex++; // Passer au bloc suivant

            // Recalcule le scrollThreshold pour le bloc suivant
            scrollThreshold += getScrollThreshold();
        }
    }
}

// Met à jour le scrollThreshold lors du redimensionnement de l'écran
window.addEventListener('resize', () => {
    scrollThreshold = getScrollThreshold();
});

// Ajoute un écouteur d'événements pour le défilement
document.addEventListener('scroll', checkScroll);




function toggleMenu() {
    const menu = document.querySelector('.dropdown-menu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}
