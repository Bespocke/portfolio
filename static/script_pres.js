let currentBlockIndex = 0; // Index du bloc actuellement visible
const blocks = document.querySelectorAll('.block'); // Sélectionne tous les blocs

let maxScrollThreshold = 1000; // Valeur maximale que tu souhaites pour le seuil
let minScrollThreshold = 300; // Valeur minimale pour le seuil
let delayOffset = 300;
let scrollThreshold = maxScrollThreshold - (window.innerWidth / 2) + delayOffset; // Ajuste le seuil en fonction de la largeur de la fenêtre

scrollThreshold = Math.max(minScrollThreshold, Math.min(scrollThreshold, maxScrollThreshold));

// Fonction pour vérifier le défilement
function checkScroll() {
    // Vérifie si la position de défilement dépasse le seuil actuel
    if (window.scrollY > scrollThreshold) {
        // Affiche chaque bloc un par un
        if (currentBlockIndex < blocks.length) {
            blocks[currentBlockIndex].classList.add('visible'); // Rendre le bloc visible
            // Ajoute la classe 'right' pour les blocs avec un index impair
            if (currentBlockIndex % 2 === 1) {
                blocks[currentBlockIndex].classList.add('right');
            }
            currentBlockIndex++; // Passer au bloc suivant
            
            // Met à jour le seuil pour le prochain bloc
            scrollThreshold += window.innerHeight * 0.3;
        }
    }
}

// Appelle checkScroll() au chargement de la page pour afficher les blocs déjà visibles
window.addEventListener('load', checkScroll);

// Ajoute un écouteur d'événements pour le défilement
document.addEventListener('scroll', checkScroll);


function toggleMenu() {
    const menu = document.querySelector('.dropdown-menu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}
