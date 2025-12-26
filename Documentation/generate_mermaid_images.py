#!/usr/bin/env python3
"""
Script pour générer des images PNG à partir des fichiers Mermaid (.mmd)

Prérequis:
    npm install -g @mermaid-js/mermaid-cli

    OU utiliser l'API Kroki (pas besoin d'installation):
    python3 generate_mermaid_images.py --api

Usage:
    python3 generate_mermaid_images.py           # Utilise mmdc (local)
    python3 generate_mermaid_images.py --api     # Utilise Kroki API
    python3 generate_mermaid_images.py --svg     # Génère des SVG au lieu de PNG
"""

import os
import sys
import base64
import zlib
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# Fichiers Mermaid à convertir
MMD_FILES = [
    "Modules_projet/Decret_Gratien/flowchart-decret-gratien.mmd",
    "Modules_projet/Module_1/flowchart-module1.mmd",
    "Modules_projet/Module_2/flowchart-module2.mmd",
    "Modules_projet/Module_3/flowchart-module3.mmd",
    "Modules_projet/Module_4/flowchart-module4.mmd",
    "Modules_projet/Module_5/flowchart-module5.mmd",
    "Modules_projet/Module_6_PAGEtopage/flowchart-module6-pagetopage.mmd",
    "Modules_projet/Module_7_NoSketch_Engine/flowchart-module7-nosketch.mmd",
    "Modules_projet/Module_8_Diffusion_Donnees/flowchart-module8-diffusion.mmd",
    "Modules_projet/Module_9_Visualisation_Requetes/flowchart-module9-visualisation.mmd",
    "Modules_projet/Module_Metadonnees/flowchart-metadonnees.mmd",
    "Modules_projet/Vue_Ensemble/flowchart-pipeline-complet-integre.mmd",
]


def encode_kroki(content: str) -> str:
    """Encode le contenu pour l'API Kroki (deflate + base64url)."""
    compressed = zlib.compress(content.encode('utf-8'), 9)
    return base64.urlsafe_b64encode(compressed).decode('ascii')


def generate_with_kroki(mmd_path: Path, output_format: str = "png") -> bool:
    """Génère une image via l'API Kroki."""
    content = mmd_path.read_text(encoding='utf-8')
    encoded = encode_kroki(content)
    url = f"https://kroki.io/mermaid/{output_format}/{encoded}"

    output_path = mmd_path.with_suffix(f".{output_format}")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as response:
            output_path.write_bytes(response.read())
        return True
    except Exception as e:
        print(f"  ❌ Erreur Kroki: {e}")
        return False


def generate_with_mmdc(mmd_path: Path, output_format: str = "png") -> bool:
    """Génère une image via mmdc (Mermaid CLI)."""
    output_path = mmd_path.with_suffix(f".{output_format}")

    try:
        result = subprocess.run(
            ["mmdc", "-i", str(mmd_path), "-o", str(output_path), "-b", "white"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            print(f"  ❌ Erreur mmdc: {result.stderr}")
            return False
        return True
    except FileNotFoundError:
        print("  ❌ mmdc non trouvé. Installez avec: npm install -g @mermaid-js/mermaid-cli")
        return False
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False


def main():
    # Déterminer le répertoire racine du projet
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # CiSaMe/

    # Options
    use_api = "--api" in sys.argv
    output_format = "svg" if "--svg" in sys.argv else "png"
    method = "Kroki API" if use_api else "mmdc (local)"

    print(f"🎨 Génération des images Mermaid ({output_format.upper()})")
    print(f"📦 Méthode: {method}")
    print("=" * 50)

    success = 0
    failed = 0

    for mmd_file in MMD_FILES:
        mmd_path = project_root / mmd_file
        print(f"\n📄 {mmd_file}")

        if not mmd_path.exists():
            print(f"  ⚠️  Fichier non trouvé")
            failed += 1
            continue

        if use_api:
            ok = generate_with_kroki(mmd_path, output_format)
        else:
            ok = generate_with_mmdc(mmd_path, output_format)

        if ok:
            print(f"  ✅ {mmd_path.stem}.{output_format} généré")
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 50)
    print(f"📊 Résultat: {success} succès, {failed} échecs")

    if failed > 0 and not use_api:
        print("\n💡 Astuce: Essayez avec --api pour utiliser Kroki (pas besoin d'installation)")
        print("   python3 generate_mermaid_images.py --api")


if __name__ == "__main__":
    main()
