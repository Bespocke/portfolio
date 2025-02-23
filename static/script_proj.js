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

document.addEventListener("DOMContentLoaded", () => {
    const animationSection = document.getElementById("animation");
    const imgElement = document.getElementById("animated-image");
    const totalFrames = 55; // Nombre total d'images extraites avec ffmpeg
    let currentFrame = 1;
    let animationActive = false;
    let animationPlayed = false; // Flag pour s'assurer que l'animation ne se joue qu'une seule fois

    function changeImage(frame) {
        imgElement.src = `static/images/frames/frame_${String(frame).padStart(3, '0')}.png`;
    }

    function checkAnimationTrigger() {
        const rect = animationSection.getBoundingClientRect();
        const extraPixels = 10; // Nombre de pixels supplémentaires visibles avant de déclencher l’animation

        if (!animationPlayed && rect.top >= -extraPixels && rect.bottom <= window.innerHeight + extraPixels) {
            animationActive = true;
            animationPlayed = true; // L'animation ne se joue qu'une seule fois
        }
    }

    window.addEventListener("scroll", () => {
        checkAnimationTrigger();
    });

    window.addEventListener("wheel", (event) => {
        if (animationActive) {
            event.preventDefault();
            const delta = event.deltaY;

            if (delta > 0 && currentFrame < totalFrames) {
                currentFrame++;
                changeImage(currentFrame);
            } else if (delta < 0 && currentFrame > 1) {
                currentFrame--;
                changeImage(currentFrame);
            }

            // Lorsque l’animation est terminée, rétablir le scroll normal
            if (currentFrame === totalFrames) {
                animationActive = false; // Désactiver l’animation une fois terminée
            }
        }
    }, { passive: false }); // Ajout de `passive: false` pour éviter les avertissements de performance
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
      