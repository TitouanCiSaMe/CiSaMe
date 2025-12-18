#!/usr/bin/env python3
"""
Script de fusion de fichiers texte pour NoSketch-Engine
Fusionne tous les fichiers d'un dossier en un seul fichier
"""
import os
import argparse
from pathlib import Path


def fusion_fichiers_texte_dossier(dossier, fichier_sortie, extension=".txt", separateur=""):
    """
    Fusionne tous les fichiers texte d'un dossier en un seul fichier.

    Args:
        dossier (str): Chemin vers le dossier contenant les fichiers à fusionner
        fichier_sortie (str): Chemin vers le fichier de sortie
        extension (str): Extension des fichiers à fusionner (.txt par défaut)
        separateur (str): Texte à insérer entre le contenu de chaque fichier
    """
    try:
        # Convertir en Path pour meilleure gestion des chemins
        dossier_path = Path(dossier)

        if not dossier_path.exists():
            print(f"❌ Erreur : Le dossier '{dossier}' n'existe pas")
            return False

        if not dossier_path.is_dir():
            print(f"❌ Erreur : '{dossier}' n'est pas un dossier")
            return False

        # Obtenir la liste des fichiers dans le dossier avec l'extension spécifiée
        fichiers = sorted([f for f in dossier_path.iterdir()
                          if f.is_file() and f.suffix == extension])

        if not fichiers:
            print(f"❌ Aucun fichier avec l'extension {extension} trouvé dans {dossier}")
            return False

        print(f"📁 Dossier source : {dossier}")
        print(f"📊 {len(fichiers)} fichier(s) trouvé(s) avec l'extension {extension}")

        # Déterminer le chemin de sortie
        fichier_sortie_path = Path(fichier_sortie)
        if not fichier_sortie_path.is_absolute():
            fichier_sortie_path = dossier_path / fichier_sortie

        print(f"📝 Fichier de sortie : {fichier_sortie_path}")
        print(f"🔄 Fusion en cours...")

        total_size = 0
        with open(fichier_sortie_path, 'w', encoding='utf-8') as destination:
            for i, fichier in enumerate(fichiers, 1):
                try:
                    with open(fichier, 'r', encoding='utf-8') as source:
                        print(f"  [{i}/{len(fichiers)}] {fichier.name}")
                        contenu = source.read()
                        destination.write(contenu)
                        total_size += len(contenu)

                        # Ajouter le séparateur sauf pour le dernier fichier
                        if i < len(fichiers):
                            destination.write(separateur)

                except Exception as e:
                    print(f"⚠️  Erreur lors de la lecture du fichier {fichier.name}: {str(e)}")

        print(f"\n✅ Fusion réussie !")
        print(f"   📦 {len(fichiers)} fichiers fusionnés")
        print(f"   💾 Taille totale : {total_size:,} caractères")
        print(f"   📄 Fichier créé : {fichier_sortie_path}")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la fusion: {str(e)}")
        return False


def main():
    """Point d'entrée CLI du script"""
    parser = argparse.ArgumentParser(
        description="Fusion de fichiers texte pour NoSketch-Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Fusion de tous les .txt d'un dossier
  python Fusion_txt_NoSketch.py -i ./fichiers_verticaux/ -o Corpus.txt

  # Fusion avec séparateur personnalisé
  python Fusion_txt_NoSketch.py -i ./fichiers/ -o Corpus.txt -s "\\n\\n---\\n\\n"

  # Fusion de fichiers .vertical.txt
  python Fusion_txt_NoSketch.py -i ./output/ -o Corpus.txt -e .vertical.txt
        """
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Dossier contenant les fichiers à fusionner'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Fichier de sortie (nom ou chemin complet)'
    )

    parser.add_argument(
        '-e', '--extension',
        default='.txt',
        help='Extension des fichiers à fusionner (défaut: .txt)'
    )

    parser.add_argument(
        '-s', '--separator',
        default='',
        help='Séparateur à insérer entre les fichiers (défaut: vide)'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("📦 FUSION DE FICHIERS POUR NOSKETCH-ENGINE")
    print("=" * 70)

    success = fusion_fichiers_texte_dossier(
        dossier=args.input,
        fichier_sortie=args.output,
        extension=args.extension,
        separateur=args.separator
    )

    print("=" * 70)

    if not success:
        exit(1)


if __name__ == "__main__":
    main()
