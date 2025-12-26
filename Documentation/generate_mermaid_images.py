#!/usr/bin/env python3
"""
Script pour générer des images PNG/SVG haute qualité à partir des fichiers Mermaid (.mmd)

Prérequis:
    npm install -g @mermaid-js/mermaid-cli

Usage:
    python3 generate_mermaid_images.py                    # PNG standard
    python3 generate_mermaid_images.py --hd               # PNG haute qualité (scale 3x)
    python3 generate_mermaid_images.py --4k               # PNG très haute qualité (scale 4x)
    python3 generate_mermaid_images.py --svg              # SVG vectoriel (qualité parfaite)
    python3 generate_mermaid_images.py --width 2000       # Largeur personnalisée
    python3 generate_mermaid_images.py --api              # Via Kroki API (sans installation)
"""

import os
import sys
import json
import base64
import zlib
import subprocess
import urllib.request
import urllib.error
import tempfile
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

# Configuration Mermaid pour meilleure qualité
MERMAID_CONFIG = {
    "theme": "default",
    "themeVariables": {
        "fontSize": "16px",
        "fontFamily": "arial, sans-serif"
    },
    "flowchart": {
        "htmlLabels": True,
        "curve": "basis",
        "useMaxWidth": False,
        "padding": 20
    }
}


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


def generate_with_mmdc(mmd_path: Path, output_format: str = "png",
                       scale: int = 1, width: int = None) -> bool:
    """Génère une image via mmdc (Mermaid CLI) avec options de qualité."""
    output_path = mmd_path.with_suffix(f".{output_format}")

    # Créer un fichier de config temporaire
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(MERMAID_CONFIG, f)
        config_path = f.name

    try:
        cmd = [
            "mmdc",
            "-i", str(mmd_path),
            "-o", str(output_path),
            "-b", "white",
            "-c", config_path,
            "-s", str(scale),
        ]

        if width:
            cmd.extend(["-w", str(width)])

        # Pour PNG, on peut aussi spécifier la qualité via puppeteer
        if output_format == "png":
            cmd.extend(["-p", config_path])  # puppeteer config

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
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
    finally:
        # Nettoyer le fichier temp
        try:
            os.unlink(config_path)
        except:
            pass


def parse_args():
    """Parse les arguments de la ligne de commande."""
    args = {
        "format": "png",
        "scale": 1,
        "width": None,
        "use_api": False,
    }

    if "--svg" in sys.argv:
        args["format"] = "svg"
        args["scale"] = 1  # SVG n'a pas besoin d'échelle
    elif "--hd" in sys.argv:
        args["scale"] = 3
    elif "--4k" in sys.argv:
        args["scale"] = 4

    if "--api" in sys.argv:
        args["use_api"] = True

    # Chercher --width VALUE
    for i, arg in enumerate(sys.argv):
        if arg == "--width" and i + 1 < len(sys.argv):
            try:
                args["width"] = int(sys.argv[i + 1])
            except ValueError:
                pass

    return args


def main():
    # Déterminer le répertoire racine du projet
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # CiSaMe/

    # Options
    args = parse_args()
    output_format = args["format"]
    scale = args["scale"]
    width = args["width"]
    use_api = args["use_api"]

    method = "Kroki API" if use_api else "mmdc (local)"
    quality = "standard"
    if scale == 3:
        quality = "HD (3x)"
    elif scale == 4:
        quality = "4K (4x)"
    elif output_format == "svg":
        quality = "vectoriel (parfait)"

    print(f"🎨 Génération des images Mermaid")
    print(f"📦 Format: {output_format.upper()}")
    print(f"✨ Qualité: {quality}")
    print(f"🔧 Méthode: {method}")
    if width:
        print(f"📐 Largeur: {width}px")
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
            ok = generate_with_mmdc(mmd_path, output_format, scale, width)

        if ok:
            print(f"  ✅ {mmd_path.stem}.{output_format} généré")
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 50)
    print(f"📊 Résultat: {success} succès, {failed} échecs")

    if failed > 0 and not use_api:
        print("\n💡 Conseils:")
        print("   - Essayez --svg pour une qualité vectorielle parfaite")
        print("   - Essayez --hd ou --4k pour des PNG haute résolution")
        print("   - Essayez --api pour utiliser Kroki (sans installation)")


if __name__ == "__main__":
    main()
