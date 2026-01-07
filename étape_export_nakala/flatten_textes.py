#!/usr/bin/env python3
"""
Script pour :
1. Déplacer les fichiers des sous-dossiers "textes" vers leur dossier parent
2. Supprimer les fichiers de 0 octet
3. Générer un log des suppressions
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

def flatten_textes_folders(root_path: str, dry_run: bool = False):
    """
    Parcourt récursivement root_path, trouve les dossiers "textes",
    déplace leur contenu vers le parent et supprime les fichiers vides.
    
    Args:
        root_path: Chemin racine à parcourir
        dry_run: Si True, simule sans modifier les fichiers
    """
    root = Path(root_path).resolve()
    
    if not root.exists():
        print(f"Erreur : Le chemin '{root}' n'existe pas.")
        return
    
    # Fichier log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = root / f"log_suppressions_{timestamp}.txt"
    
    fichiers_deplaces = []
    fichiers_supprimes_vides = []
    dossiers_textes_supprimes = []
    erreurs = []
    
    # Trouver tous les dossiers "textes"
    textes_folders = list(root.rglob("textes"))
    textes_folders = [f for f in textes_folders if f.is_dir()]
    
    print(f"Dossiers 'textes' trouvés : {len(textes_folders)}")
    
    for textes_dir in textes_folders:
        parent_dir = textes_dir.parent
        print(f"\nTraitement : {textes_dir}")
        
        # Parcourir les fichiers dans le dossier textes
        for item in list(textes_dir.iterdir()):
            if item.is_file():
                # Vérifier si fichier vide
                if item.stat().st_size == 0:
                    fichiers_supprimes_vides.append(str(item))
                    print(f"  [SUPPRESSION] Fichier vide : {item.name}")
                    if not dry_run:
                        try:
                            item.unlink()
                        except Exception as e:
                            erreurs.append(f"Erreur suppression {item}: {e}")
                else:
                    # Déplacer vers le parent
                    dest = parent_dir / item.name
                    
                    # Gérer les conflits de noms
                    if dest.exists():
                        base = item.stem
                        ext = item.suffix
                        counter = 1
                        while dest.exists():
                            dest = parent_dir / f"{base}_{counter}{ext}"
                            counter += 1
                    
                    fichiers_deplaces.append(f"{item} -> {dest}")
                    print(f"  [DÉPLACEMENT] {item.name} -> {parent_dir.name}/")
                    if not dry_run:
                        try:
                            shutil.move(str(item), str(dest))
                        except Exception as e:
                            erreurs.append(f"Erreur déplacement {item}: {e}")
        
        # Supprimer le dossier textes s'il est vide
        if not dry_run:
            try:
                if textes_dir.exists() and not any(textes_dir.iterdir()):
                    textes_dir.rmdir()
                    dossiers_textes_supprimes.append(str(textes_dir))
                    print(f"  [SUPPRESSION] Dossier vide : {textes_dir.name}/")
            except Exception as e:
                erreurs.append(f"Erreur suppression dossier {textes_dir}: {e}")
    
    # Écrire le log
    if not dry_run:
        with open(log_path, 'w', encoding='utf-8') as log:
            log.write(f"=== LOG DES OPÉRATIONS ===\n")
            log.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Racine : {root}\n\n")
            
            log.write(f"=== FICHIERS VIDES SUPPRIMÉS ({len(fichiers_supprimes_vides)}) ===\n")
            for f in fichiers_supprimes_vides:
                log.write(f"  {f}\n")
            
            log.write(f"\n=== FICHIERS DÉPLACÉS ({len(fichiers_deplaces)}) ===\n")
            for f in fichiers_deplaces:
                log.write(f"  {f}\n")
            
            log.write(f"\n=== DOSSIERS 'textes' SUPPRIMÉS ({len(dossiers_textes_supprimes)}) ===\n")
            for d in dossiers_textes_supprimes:
                log.write(f"  {d}\n")
            
            if erreurs:
                log.write(f"\n=== ERREURS ({len(erreurs)}) ===\n")
                for e in erreurs:
                    log.write(f"  {e}\n")
        
        print(f"\n✓ Log enregistré : {log_path}")
    
    # Résumé
    print(f"\n{'=== RÉSUMÉ (DRY RUN) ===' if dry_run else '=== RÉSUMÉ ==='}")
    print(f"  Fichiers déplacés : {len(fichiers_deplaces)}")
    print(f"  Fichiers vides supprimés : {len(fichiers_supprimes_vides)}")
    print(f"  Dossiers 'textes' supprimés : {len(dossiers_textes_supprimes)}")
    if erreurs:
        print(f"  Erreurs : {len(erreurs)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Déplace les fichiers des dossiers 'textes' vers leur parent et supprime les fichiers vides."
    )
    parser.add_argument(
        "chemin",
        help="Chemin racine à traiter"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Simule les opérations sans modifier les fichiers"
    )
    
    args = parser.parse_args()
    flatten_textes_folders(args.chemin, dry_run=args.dry_run)
