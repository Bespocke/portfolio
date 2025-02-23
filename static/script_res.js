
// Ajouter un écouteur d'événements sur le champ de saisie
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(event) {
            // Vérifier si la touche "Entrée" a été pressée
            if (event.key === 'Enter') {
                event.preventDefault(); // Éviter le comportement par défaut
                performSearch(); // Appeler la fonction de recherche
            }
        });
    }
});


const sections = document.querySelectorAll(".section");

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



function performSearch() {
    const searchTerm = document.getElementById('search-input').value;
    const resultsContainer = document.getElementById('results-container');
    
    if (searchTerm) {
        // Appliquer l'animation visible dès qu'une recherche est effectuée
        resultsContainer.classList.add('visible');
        
        // Charger le fichier JSON contenant tous les fichiers
        fetch('scrap.json')
            .then(response => response.json())
            .then(files => {
                // Filtrer les fichiers pour ceux qui contiennent le terme de recherche
                const matchedFiles = files.filter(file => 
                    file.toLowerCase().includes(searchTerm.toLowerCase())
                );

                // Effacer les anciens résultats
                resultsContainer.innerHTML = '';

                if (matchedFiles.length > 0) {
                    // Regrouper les fichiers par dossier
                    const fileGroups = matchedFiles.reduce((acc, file) => {
                        const dir = file.substring(0, file.lastIndexOf('/')); // Extraire le dossier
                        if (!acc[dir]) {
                            acc[dir] = []; // Créer un tableau pour ce dossier
                        }
                        acc[dir].push(file); // Ajouter le fichier au tableau correspondant
                        return acc;
                    }, {});

                    // Créer un tableau HTML pour afficher les résultats
                    const table = document.createElement('table');
                    table.style.borderCollapse = 'collapse'; // Pour avoir des bordures sans espaces
                    table.style.width = '100%'; // Largeur du tableau à 100%

                    // Créer l'en-tête du tableau
                    const headerRow = document.createElement('tr');
                    const headerCell1 = document.createElement('th');
                    headerCell1.textContent = 'Dossier';
                    headerCell1.style.border = '2px solid #445a70'; // Bordure pour l'en-tête
                    headerCell1.style.padding = '8px'; // Espace intérieur pour l'en-tête
                    headerRow.appendChild(headerCell1);

                    const headerCell2 = document.createElement('th');
                    headerCell2.textContent = 'Fichiers';
                    headerCell2.style.border = '2px solid #445a70'; // Bordure pour l'en-tête
                    headerCell2.style.padding = '8px'; // Espace intérieur pour l'en-tête
                    headerRow.appendChild(headerCell2);

                    table.appendChild(headerRow);

                    // Remplir le tableau avec les données groupées
                    for (const dir in fileGroups) {
                        const row = document.createElement('tr');
                        const dirCell = document.createElement('td');
                        const dirName = dir.substring(dir.lastIndexOf('/') + 1); // Obtenir seulement le nom du dossier
                        dirCell.textContent = dirName; // Afficher le nom du dossier
                        dirCell.style.border = '2px solid #445a70'; // Bordure pour chaque cellule
                        dirCell.style.padding = '8px'; // Espace intérieur

                        const filesCell = document.createElement('td');
                        filesCell.style.border = '2px solid #445a70'; // Bordure pour chaque cellule
                        filesCell.style.padding = '8px'; // Espace intérieur

                        // Créer les liens de fichiers
                        const fileLinks = fileGroups[dir].map(filePath => {
                            const fileName = filePath.split('/').pop(); // Extraire le nom du fichier
                            const link = document.createElement('a');   // Créer un élément <a> pour le lien
                            link.textContent = fileName;                // Afficher seulement le nom du fichier
                            link.href = 'res/' + filePath;              // Associer le lien au chemin relatif
                            link.target = '_blank';                     // Ouvrir dans un nouvel onglet
                            link.style.textDecoration = 'none';         // Style de lien

                            return link; // Retourner le lien
                        });

                        // Ajouter les liens de fichiers dans la cellule
                        fileLinks.forEach(link => {
                            filesCell.appendChild(link);
                            filesCell.appendChild(document.createElement('br')); // Saut de ligne entre les fichiers
                        });

                        row.appendChild(dirCell);
                        row.appendChild(filesCell);
                        table.appendChild(row);
                    }

                    // Ajouter le tableau à l'élément de résultats
                    resultsContainer.appendChild(table);
                } else {
                    // Message si aucun fichier trouvé
                    resultsContainer.textContent = 'Aucun fichier trouvé.';
                }
            })
            .catch(error => {
                console.error('Erreur lors du chargement des fichiers:', error);
                resultsContainer.textContent = 'Erreur lors du chargement des fichiers.';
            });
    }
}
