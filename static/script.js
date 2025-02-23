// Sélectionner tous les liens de défilement
const scrollLinks = document.querySelectorAll('.scroll-link');
const sections = document.querySelectorAll(".section");

// Ajout d'un comportement de scroll fluide sur les liens
scrollLinks.forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();

        // Récupérer l'ID de la section ciblée
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer pour l'animation d'apparition des sections
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
        }
    });
}, { threshold: 0.4 });

sections.forEach(section => observer.observe(section));

// Détection de la section active et mise à jour des liens de navigation
let lastActive = ""; // Stocke la dernière section active pour éviter des mises à jour inutiles

window.addEventListener("scroll", () => {
    requestAnimationFrame(() => {
        let current = "";

        // Calcul de la position de la page et détection de la section active
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;

            // Ajuster le seuil en modifiant cette ligne
            if (window.scrollY >= sectionTop - sectionHeight / 5) {
                current = section.getAttribute("id");
            }
        });

        // Vérifier si on est tout en bas de la page et activer la dernière section
        const lastSection = sections[sections.length - 1];
        const lastSectionTop = lastSection.offsetTop;
        const lastSectionHeight = lastSection.offsetHeight;

        if (window.scrollY + window.innerHeight >= lastSectionTop + lastSectionHeight) {
            current = lastSection.getAttribute("id");
        }

        // Si on est tout en haut de la page, ne pas activer de liens
        if (window.scrollY < 10) {
            current = null; // Utilisez `null` pour éviter d'ajouter une chaîne vide
        }

        // Mise à jour des liens de navigation
        if (current !== lastActive) {
            lastActive = current;
            scrollLinks.forEach(link => {
                link.classList.remove("active");
                if (current && link.getAttribute("href").includes(current)) { // Ajoutez la vérification `current`
                    link.classList.add("active");
                }
            });
        }
    });
});

document.querySelectorAll('.side-img').forEach(img => {
    img.style.opacity = "0";
    img.style.transform = "translateY(20px)";
});

const observerImg = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";
            entry.target.style.transition = "opacity 0.6s ease-out, transform 0.6s ease-out";
        }
    });
}, { threshold: 0.3 });

document.querySelectorAll('.side-img').forEach(img => observerImg.observe(img));
      