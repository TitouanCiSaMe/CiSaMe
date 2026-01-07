#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour convertir tous les fichiers fiche.docx en fiche.pdf
dans les sous-dossiers de CiSaMe.

Usage:
    ./convert_fiches_to_pdf.py [chemin_vers_CiSaMe] [--delete-docx]
    
Options:
    --delete-docx   Supprime les fichiers .docx après conversion réussie
    
Par défaut, utilise ./input/CiSaMe
"""

import os
import subprocess
import sys
from os.path import join, dirname, realpath, exists
from tqdm import tqdm


def convert_docx_to_pdf(docx_path):
    """Convertit un fichier .docx en .pdf avec LibreOffice"""
    output_dir = dirname(docx_path)
    result = subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', output_dir, docx_path
    ], capture_output=True, text=True)
    return result.returncode == 0


def main():
    # Options
    delete_docx = '--delete-docx' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    
    # Chemin par défaut ou argument
    cwd = dirname(realpath(__file__))
    default_path = join(cwd, 'input', 'CiSaMe')
    base_path = args[0] if args else default_path
    
    print(f"\n{'='*60}")
    print(f"📄 Conversion des fiche.docx en fiche.pdf")
    print(f"{'='*60}")
    print(f"📁 Dossier : {base_path}")
    if delete_docx:
        print(f"🗑️  Les fichiers .docx seront supprimés après conversion")
    print()
    
    # Trouver tous les fiche.docx
    fiches = []
    for folder in os.listdir(base_path):
        folder_path = join(base_path, folder)
        fiche_docx = join(folder_path, 'fiche.docx')
        if exists(fiche_docx):
            fiches.append(fiche_docx)
    
    print(f"📋 {len(fiches)} fichiers fiche.docx trouvés\n")
    
    if not fiches:
        print("❌ Aucun fichier à convertir")
        return
    
    # Convertir
    success = 0
    errors = []
    deleted = 0
    
    for fiche in tqdm(fiches, desc="Conversion"):
        if convert_docx_to_pdf(fiche):
            success += 1
            if delete_docx:
                os.remove(fiche)
                deleted += 1
        else:
            errors.append(fiche)
    
    print(f"\n{'='*60}")
    print(f"✅ {success} fichiers convertis avec succès")
    if delete_docx:
        print(f"🗑️  {deleted} fichiers .docx supprimés")
    if errors:
        print(f"❌ {len(errors)} erreurs :")
        for e in errors:
            print(f"   - {e}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
