function performSearch() {
    const searchTerm = document.getElementById('search-input').value;
    if (searchTerm) {
        // Rediriger vers la page de résultats avec le terme de recherche dans l'URL
        window.location.href = 'results.html?query=' + encodeURIComponent(searchTerm);
    }
}

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




// Dans results.html, récupérer le terme de recherche et afficher les résultats
if (window.location.href.includes('results.html')) {
    const params = new URLSearchParams(window.location.search);
    const query = params.get('query');
    const resultsContainer = document.getElementById('results-container');

    if (query) {
        // Charger le fichier JSON contenant tous les fichiers
        fetch('scrap.json')
            .then(response => response.json())
            .then(files => {
                // Filtrer les fichiers pour ceux qui contiennent le terme de recherche
                const matchedFiles = files.filter(file => 
                    file.toLowerCase().includes(query.toLowerCase())
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
                    headerCell1.style.border = '1px solid #ddd'; // Bordure pour l'en-tête
                    headerCell1.style.padding = '8px'; // Espace intérieur pour l'en-tête
                    headerRow.appendChild(headerCell1);

                    const headerCell2 = document.createElement('th');
                    headerCell2.textContent = 'Fichiers';
                    headerCell2.style.border = '1px solid #ddd'; // Bordure pour l'en-tête
                    headerCell2.style.padding = '8px'; // Espace intérieur pour l'en-tête
                    headerRow.appendChild(headerCell2);
                    
                    table.appendChild(headerRow);

                    // Remplir le tableau avec les données groupées
                    for (const dir in fileGroups) {
                        const row = document.createElement('tr');
                        const dirCell = document.createElement('td');
                        const dirName = dir.substring(dir.lastIndexOf('/') + 1); // Obtenir seulement le nom du dossier
                        dirCell.textContent = dirName; // Afficher le nom du dossier
                        dirCell.style.border = '1px solid #ddd'; // Bordure pour chaque cellule
                        dirCell.style.padding = '8px'; // Espace intérieur

                        const filesCell = document.createElement('td');
                        filesCell.style.border = '1px solid #ddd'; // Bordure pour chaque cellule
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


function toggleMenu() {
    const menu = document.querySelector('.dropdown-menu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}
