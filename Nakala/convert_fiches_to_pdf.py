#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour convertir tous les fichiers fiche.docx en fiche.pdf
dans les sous-dossiers de CiSaMe.

Usage:
    python convert_fiches_to_pdf.py [chemin] [--delete-docx] [--dry-run]

Options:
    chemin          Chemin vers le dossier CiSaMe (defaut: ./input/CiSaMe)
    --delete-docx   Supprime les fichiers .docx apres conversion reussie
    --dry-run       Simule sans convertir
"""

import os
import sys
import logging
import argparse
import subprocess
from os.path import join, dirname, realpath, exists
from tqdm import tqdm

logger = logging.getLogger(__name__)

SOFFICE_TIMEOUT = 120  # secondes


def check_soffice_available():
    """Verifie que LibreOffice (soffice) est disponible."""
    try:
        result = subprocess.run(
            ['soffice', '--version'],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def convert_docx_to_pdf(docx_path, output_dir=None):
    """Convertit un fichier .docx en .pdf avec LibreOffice.

    Args:
        docx_path: Chemin vers le fichier .docx.
        output_dir: Dossier de sortie (defaut: meme dossier que le .docx).

    Returns:
        True si la conversion a reussi.
    """
    if output_dir is None:
        output_dir = dirname(docx_path)

    try:
        result = subprocess.run(
            ['soffice', '--headless', '--convert-to', 'pdf',
             '--outdir', output_dir, docx_path],
            capture_output=True, text=True, timeout=SOFFICE_TIMEOUT
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.warning("Timeout conversion (>%ds) : %s", SOFFICE_TIMEOUT, docx_path)
        return False
    except FileNotFoundError:
        logger.error("LibreOffice (soffice) non trouve dans le PATH")
        return False
    except (IOError, OSError) as e:
        logger.error("Erreur conversion %s : %s", docx_path, e)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convertit les fiche.docx en fiche.pdf dans les sous-dossiers'
    )
    parser.add_argument(
        'chemin', nargs='?', default=None,
        help='Chemin vers le dossier CiSaMe (defaut: ./input/CiSaMe)'
    )
    parser.add_argument(
        '--delete-docx', action='store_true',
        help='Supprime les fichiers .docx apres conversion reussie'
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help='Simule sans convertir'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Active les logs de debug'
    )
    args = parser.parse_args()

    # Logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s', stream=sys.stderr)

    # Chemin par defaut
    if args.chemin:
        base_path = args.chemin
    else:
        base_path = join(dirname(realpath(__file__)), 'input', 'CiSaMe')

    if not os.path.isdir(base_path):
        logger.error("Dossier introuvable : %s", base_path)
        sys.exit(1)

    # Verifier que soffice est disponible
    if not args.dry_run and not check_soffice_available():
        logger.error(
            "LibreOffice (soffice) non disponible. "
            "Installez LibreOffice ou ajoutez soffice au PATH."
        )
        sys.exit(1)

    logger.info("Conversion des fiche.docx en fiche.pdf")
    logger.info("Dossier : %s", base_path)
    if args.delete_docx:
        logger.info("Les fichiers .docx seront supprimes apres conversion")
    if args.dry_run:
        logger.info("Mode DRY-RUN : aucune conversion ne sera effectuee")

    # Trouver tous les fiche.docx
    fiches = []
    try:
        for folder in os.listdir(base_path):
            folder_path = join(base_path, folder)
            fiche_docx = join(folder_path, 'fiche.docx')
            if exists(fiche_docx):
                fiches.append(fiche_docx)
    except (IOError, OSError) as e:
        logger.error("Impossible de lister %s : %s", base_path, e)
        sys.exit(1)

    logger.info("%d fichiers fiche.docx trouves", len(fiches))

    if not fiches:
        logger.warning("Aucun fichier a convertir")
        return

    # Convertir
    success = 0
    errors = []
    deleted = 0

    for fiche in tqdm(fiches, desc="Conversion"):
        if args.dry_run:
            logger.debug("[DRY-RUN] %s", fiche)
            success += 1
            continue

        if convert_docx_to_pdf(fiche):
            success += 1
            if args.delete_docx:
                try:
                    os.remove(fiche)
                    deleted += 1
                except (IOError, OSError) as e:
                    logger.warning("Impossible de supprimer %s : %s", fiche, e)
        else:
            errors.append(fiche)

    # Rapport
    logger.info("%d fichiers convertis avec succes", success)
    if args.delete_docx:
        logger.info("%d fichiers .docx supprimes", deleted)
    if errors:
        logger.warning("%d erreurs :", len(errors))
        for e in errors:
            logger.warning("  - %s", e)


if __name__ == '__main__':
    main()
