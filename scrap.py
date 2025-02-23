#! /Users/a./Documents/cours/ensta\ b/1A/projets_persos/portfolio/pyt/bin/python

import os
import json

# Chemin vers le dossier "res" dans le même répertoire que le script
FOLDER_PATH = os.path.join(os.path.dirname(__file__), 'res')

# Extensions de fichiers à inclure
VALID_EXTENSIONS = {
    '.pdf', '.docx', '.txt', '.pptx', '.xlsx', '.csv',  # Documents classiques
    '.py', '.ml',  # Fichiers Python et OCaml
    '.markdown', '.md',  # Fichiers Markdown
    '.html', '.css',  # Fichiers web
    '.ppt',  # Ancien format PowerPoint
    '.docx',  # Ancien format Word
    '.ods',  # Fichiers OpenDocument Spreadsheet
    '.odt',  # Fichiers OpenDocument Text
}

# Fonction pour lister tous les fichiers dans "res" avec leur chemin relatif
def list_files_in_folder(folder_path):
    files_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Exclure les fichiers non souhaités
            if file == '.DS_Store' or '__pycache__' in root:
                continue
            
            # Vérifier l'extension du fichier
            _, ext = os.path.splitext(file)
            if ext.lower() not in VALID_EXTENSIONS:
                continue
            
            # Chemin relatif du fichier par rapport au dossier "res"
            relative_path = os.path.relpath(os.path.join(root, file), folder_path)
            files_list.append(relative_path)
    return files_list

# Obtenir la liste des fichiers
all_files = list_files_in_folder(FOLDER_PATH)

# Enregistrer la liste des fichiers dans un fichier JSON
with open('scrap.json', 'w') as json_file:
    json.dump(all_files, json_file, indent=4)

print(f"Fichier 'scrap.json' généré avec succès dans le répertoire courant.")
