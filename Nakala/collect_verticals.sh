#!/bin/bash
# Collecte tous les fichiers vertical.txt depuis les sous-dossiers
# et les copie dans un dossier de sortie en les renommant pour éviter les conflits.
#
# Usage: ./collect_verticals.sh [chemin_source] [chemin_destination]

SRC="${1:-$HOME/Documents/Github/nakala-uploader/input/CiSaMe}"
DST="${2:-$HOME/Documents/Github/nakala-uploader/output/verticals}"

if [ ! -d "$SRC" ]; then
    echo "Erreur : dossier source introuvable : $SRC"
    exit 1
fi

mkdir -p "$DST"

count=0
while IFS= read -r -d '' file; do
    # Nom du sous-dossier parent comme préfixe pour éviter les conflits
    parent=$(basename "$(dirname "$file")")
    dest="$DST/${parent}_vertical.txt"
    cp "$file" "$dest"
    echo "Copié : $file -> $dest"
    count=$((count + 1))
done < <(find "$SRC" -type f -name "vertical.txt" -print0)

echo "Terminé : $count fichier(s) copié(s) dans $DST"
