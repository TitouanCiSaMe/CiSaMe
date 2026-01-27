#!/usr/bin/env python3
"""
Script pour :
1. Supprimer les fichiers de 0 octet (fichiers vides)
2. Optionnellement déplacer les fichiers des sous-dossiers "textes" vers leur parent
3. Générer un log des suppressions

Usage:
    # Supprimer les fichiers vides dans toute la structure
    python flatten_textes.py /chemin/vers/export --dry-run

    # Supprimer les fichiers vides ET aplatir les dossiers "textes"
    python flatten_textes.py /chemin/vers/export --flatten --dry-run
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


def remove_empty_files(root_path: str, dry_run: bool = False):
    """
    Parcourt récursivement root_path et supprime tous les fichiers de 0 octet.

    Args:
        root_path: Chemin racine à parcourir
        dry_run: Si True, simule sans modifier les fichiers

    Returns:
        Liste des fichiers supprimés
    """
    root = Path(root_path).resolve()
    fichiers_vides = []

    # Trouver tous les fichiers vides
    for filepath in root.rglob("*"):
        if filepath.is_file() and filepath.stat().st_size == 0:
            fichiers_vides.append(filepath)
            print(f"  [VIDE] {filepath.relative_to(root)}")
            if not dry_run:
                try:
                    filepath.unlink()
                except Exception as e:
                    print(f"    Erreur: {e}")

    return fichiers_vides


def flatten_textes_folders(root_path: str, dry_run: bool = False):
    """
    Parcourt récursivement root_path, trouve les dossiers "textes",
    déplace leur contenu vers le parent.

    Args:
        root_path: Chemin racine à parcourir
        dry_run: Si True, simule sans modifier les fichiers

    Returns:
        Tuple (fichiers_deplaces, dossiers_supprimes)
    """
    root = Path(root_path).resolve()
    fichiers_deplaces = []
    dossiers_supprimes = []

    # Trouver tous les dossiers "textes"
    textes_folders = [f for f in root.rglob("textes") if f.is_dir()]

    print(f"\nDossiers 'textes' trouvés : {len(textes_folders)}")

    for textes_dir in textes_folders:
        parent_dir = textes_dir.parent
        print(f"\nTraitement : {textes_dir.relative_to(root)}")

        # Parcourir les fichiers dans le dossier textes
        for item in list(textes_dir.iterdir()):
            if item.is_file():
                # Déplacer vers le parent
                dest = parent_dir / item.name

                # Gérer les conflits de noms
                if dest.exists():
                    base = item.stem
                    ext = item.suffix
                    counter = 1
                    max_counter = 10000
                    while dest.exists() and counter < max_counter:
                        dest = parent_dir / f"{base}_{counter}{ext}"
                        counter += 1
                    if counter >= max_counter:
                        print(f"    Erreur: trop de conflits pour {item.name}")
                        continue

                fichiers_deplaces.append((item, dest))
                print(f"  [DÉPLACEMENT] {item.name} -> {parent_dir.name}/")
                if not dry_run:
                    try:
                        shutil.move(str(item), str(dest))
                    except Exception as e:
                        print(f"    Erreur: {e}")

        # Supprimer le dossier textes s'il est vide
        if not dry_run:
            try:
                if textes_dir.exists() and not any(textes_dir.iterdir()):
                    textes_dir.rmdir()
                    dossiers_supprimes.append(textes_dir)
                    print(f"  [SUPPRESSION] Dossier vide : {textes_dir.name}/")
            except Exception as e:
                print(f"    Erreur: {e}")

    return fichiers_deplaces, dossiers_supprimes


def main(root_path: str, flatten: bool = False, dry_run: bool = False):
    """
    Fonction principale

    Args:
        root_path: Chemin racine à traiter
        flatten: Si True, aplatit aussi les dossiers "textes"
        dry_run: Si True, simule sans modifier
    """
    root = Path(root_path).resolve()

    if not root.exists():
        print(f"Erreur : Le chemin '{root}' n'existe pas.")
        return

    print(f"{'=== MODE SIMULATION ===' if dry_run else '=== TRAITEMENT ==='}")
    print(f"Racine : {root}")

    # 1. Supprimer les fichiers vides
    print(f"\n--- Recherche des fichiers vides ---")
    fichiers_vides = remove_empty_files(root_path, dry_run)

    # 2. Aplatir les dossiers textes si demandé
    fichiers_deplaces = []
    dossiers_supprimes = []
    if flatten:
        print(f"\n--- Aplatissement des dossiers 'textes' ---")
        fichiers_deplaces, dossiers_supprimes = flatten_textes_folders(root_path, dry_run)

    # Écrire le log
    if not dry_run and (fichiers_vides or fichiers_deplaces):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = root / f"log_nettoyage_{timestamp}.txt"

        with open(log_path, 'w', encoding='utf-8') as log:
            log.write(f"=== LOG DES OPÉRATIONS ===\n")
            log.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Racine : {root}\n\n")

            log.write(f"=== FICHIERS VIDES SUPPRIMÉS ({len(fichiers_vides)}) ===\n")
            for f in fichiers_vides:
                log.write(f"  {f}\n")

            if flatten:
                log.write(f"\n=== FICHIERS DÉPLACÉS ({len(fichiers_deplaces)}) ===\n")
                for src, dst in fichiers_deplaces:
                    log.write(f"  {src} -> {dst}\n")

                log.write(f"\n=== DOSSIERS 'textes' SUPPRIMÉS ({len(dossiers_supprimes)}) ===\n")
                for d in dossiers_supprimes:
                    log.write(f"  {d}\n")

        print(f"\nLog enregistre : {log_path}")

    # Résumé
    print(f"\n{'=== RÉSUMÉ (DRY RUN) ===' if dry_run else '=== RÉSUMÉ ==='}")
    print(f"  Fichiers vides {'à supprimer' if dry_run else 'supprimés'} : {len(fichiers_vides)}")
    if flatten:
        print(f"  Fichiers {'à déplacer' if dry_run else 'déplacés'} : {len(fichiers_deplaces)}")
        print(f"  Dossiers 'textes' {'à supprimer' if dry_run else 'supprimés'} : {len(dossiers_supprimes)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Supprime les fichiers vides et optionnellement aplatit les dossiers 'textes'.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
    # Voir les fichiers vides sans les supprimer
    python flatten_textes.py /chemin/vers/export --dry-run

    # Supprimer les fichiers vides
    python flatten_textes.py /chemin/vers/export

    # Supprimer les fichiers vides ET aplatir les dossiers "textes"
    python flatten_textes.py /chemin/vers/export --flatten
        """
    )
    parser.add_argument(
        "chemin",
        help="Chemin racine à traiter"
    )
    parser.add_argument(
        "--flatten", "-f",
        action="store_true",
        help="Déplace aussi les fichiers des dossiers 'textes' vers leur parent"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Simule les opérations sans modifier les fichiers"
    )

    args = parser.parse_args()
    main(args.chemin, flatten=args.flatten, dry_run=args.dry_run)
