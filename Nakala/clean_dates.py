#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour nettoyer les fichiers pages_index.json :
remplace les dates vides ("") par null dans les fichiers JSON.

Usage:
    python clean_dates.py [chemin] [--dry-run] [--recursive]
"""

import os
import sys
import json
import logging
import argparse
from os.path import join

logger = logging.getLogger(__name__)


def clean_empty_dates(base_path, dry_run=False, recursive=False):
    """Parcourt les dossiers et nettoie les dates vides dans pages_index.json.

    Args:
        base_path: Chemin racine à parcourir.
        dry_run: Si True, ne modifie pas les fichiers.
        recursive: Si True, parcourt récursivement les sous-dossiers.

    Returns:
        Nombre de fichiers modifiés.
    """
    modified_count = 0

    if recursive:
        walker = os.walk(base_path)
    else:
        # Un seul niveau
        try:
            entries = os.listdir(base_path)
        except (IOError, OSError) as e:
            logger.error("Impossible de lister %s : %s", base_path, e)
            return 0
        walker = [(base_path, [d for d in entries if os.path.isdir(join(base_path, d))], [])]

    for dirpath, dirnames, _filenames in walker:
        for folder in dirnames:
            json_path = join(dirpath, folder, 'pages_index.json')

            if not os.path.isfile(json_path):
                continue

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                logger.warning("JSON invalide dans %s : %s", json_path, e)
                continue
            except (IOError, OSError) as e:
                logger.warning("Impossible de lire %s : %s", json_path, e)
                continue

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
                if dry_run:
                    logger.info("[DRY-RUN] %s", join(folder, 'pages_index.json'))
                else:
                    try:
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        logger.info("[MODIFIE] %s", join(folder, 'pages_index.json'))
                    except (IOError, OSError) as e:
                        logger.error("Impossible d'ecrire %s : %s", json_path, e)
                        continue
                modified_count += 1

    logger.info("Termine : %d fichier(s) modifie(s)", modified_count)
    return modified_count


def main():
    parser = argparse.ArgumentParser(
        description='Nettoie les dates vides dans les fichiers pages_index.json'
    )
    parser.add_argument(
        'chemin', nargs='?', default=None,
        help='Chemin racine a parcourir (defaut: ./input/CiSaMe)'
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help='Simule sans modifier les fichiers'
    )
    parser.add_argument(
        '--recursive', '-r', action='store_true',
        help='Parcourt recursivement les sous-dossiers'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Active les logs de debug'
    )
    args = parser.parse_args()

    # Logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s', stream=sys.stderr)

    # Chemin par défaut
    if args.chemin:
        base_path = args.chemin
    else:
        from os.path import dirname, realpath
        base_path = join(dirname(realpath(__file__)), 'input', 'CiSaMe')

    if not os.path.isdir(base_path):
        logger.error("Dossier introuvable : %s", base_path)
        sys.exit(1)

    logger.info("Nettoyage des dates vides dans : %s", base_path)
    if args.dry_run:
        logger.info("Mode DRY-RUN : aucune modification ne sera ecrite")

    clean_empty_dates(base_path, dry_run=args.dry_run, recursive=args.recursive)


if __name__ == '__main__':
    main()
