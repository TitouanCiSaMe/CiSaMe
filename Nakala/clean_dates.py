#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour nettoyer les fichiers pages_index.json :
remplace les dates vides ("") par null dans les fichiers JSON.
"""

import os
import json
from os.path import join

def clean_empty_dates(base_path):
    """Parcourt tous les dossiers et nettoie les dates vides dans pages_index.json"""
    
    modified_count = 0
    
    for folder in os.listdir(base_path):
        folder_path = join(base_path, folder)
        json_path = join(folder_path, 'pages_index.json')
        
        if not os.path.isfile(json_path):
            continue
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        
        for page in data.get('pages', []):
            # Vérifie au niveau page (format sans 'metadata')
            if 'date' in page and page['date'] == '':
                page['date'] = None
                modified = True
            
            # Vérifie au niveau metadata (format avec 'metadata')
            if 'metadata' in page and 'date' in page['metadata']:
                if page['metadata']['date'] == '':
                    page['metadata']['date'] = None
                    modified = True
        
        if modified:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[MODIFIÉ] {folder}")
            modified_count += 1
    
    print(f"\nTerminé : {modified_count} fichier(s) modifié(s)")


if __name__ == '__main__':
    import sys
    from os.path import dirname, realpath
    
    cwd = dirname(realpath(__file__))
    default_path = join(cwd, 'input', 'CiSaMe')
    
    # Permet de passer un chemin en argument
    base_path = sys.argv[1] if len(sys.argv) > 1 else default_path
    
    print(f"Nettoyage des dates vides dans : {base_path}\n")
    clean_empty_dates(base_path)
