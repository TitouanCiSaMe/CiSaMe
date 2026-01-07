#!/usr/bin/env python3
"""
Préparation de l'export Nakala pour le projet CiSaMe (VERSION PAR ŒUVRE)

Ce script prépare la structure de dossiers pour l'upload via Heimdall en :
1. Parsant les fiches .docx pour extraire Edi-XX et statut libre de droits
2. Chaque fichier vertical = une œuvre distincte
3. Associant les textes par nom de fichier vertical
4. Créant la structure Libre_de_droits / Non_libre_de_droits
5. Convertissant les fiches .docx → .pdf
6. Générant un rapport de l'export

Usage:
    python prepare_nakala_export.py \
        --fiches ./Fiches_Editions_Metadonnee/ \
        --verticaux ./Verticaux/ \
        --textes ./Textes/ \
        --output ./input/CiSaMe/

Structure de sortie:
    input/CiSaMe/
    ├── Libre_de_droits/
    │   └── Source_Edi-XX/
    │       ├── pages_index.json
    │       ├── vertical.txt
    │       ├── fiche.pdf
    │       └── page_*.txt
    └── Non_libre_de_droits/
        └── ...

Auteur: Projet CiSaMe - Janvier 2025
"""

import os
import re
import glob
import shutil
import subprocess
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("WARNING: python-docx non installé. Installez-le avec: pip install python-docx")


@dataclass
class FicheInfo:
    """Informations extraites d'une fiche .docx"""
    path: str
    edi_id: Optional[str] = None
    titre_oeuvre: Optional[str] = None
    auteur: Optional[str] = None
    libre_de_droits: bool = False


@dataclass
class VerticalInfo:
    """Informations extraites d'un fichier vertical"""
    path: str
    filename: str  # Nom du fichier sans extension
    edi_id: Optional[str] = None
    source: Optional[str] = None
    title: Optional[str] = None


@dataclass
class TextesInfo:
    """Informations extraites d'un dossier de textes"""
    path: str
    dirname: str
    edi_id: Optional[str] = None
    source: Optional[str] = None
    has_pages_index: bool = False


@dataclass
class OeuvreItem:
    """Une œuvre à exporter (= un fichier vertical)"""
    oeuvre_key: str  # Nom du fichier vertical (clé unique)
    edi_id: str
    nom_oeuvre: str
    libre_de_droits: bool = False
    fiche: Optional[FicheInfo] = None
    vertical: Optional[VerticalInfo] = None
    textes: Optional[TextesInfo] = None
    export_path: Optional[str] = None
    exported: bool = False
    errors: List[str] = field(default_factory=list)


class NakalaExportPreparer:
    """Prépare l'export Nakala pour Heimdall (version par œuvre)"""

    def __init__(self, fiches_dir: str, verticaux_dir: str, textes_dir: str,
                 output_dir: str, verbose: bool = True):
        self.fiches_dir = Path(fiches_dir) if fiches_dir else None
        self.verticaux_dir = Path(verticaux_dir) if verticaux_dir else None
        self.textes_dir = Path(textes_dir) if textes_dir else None
        self.output_dir = Path(output_dir)
        self.verbose = verbose

        # Fiches indexées par Edi-XX (une fiche peut correspondre à plusieurs œuvres)
        self.fiches_par_id: Dict[str, FicheInfo] = {}

        # Œuvres indexées par nom de fichier vertical
        self.oeuvres: Dict[str, OeuvreItem] = {}

        # Stats
        self.stats = {
            'fiches_scanned': 0,
            'fiches_with_id': 0,
            'verticaux_scanned': 0,
            'verticaux_with_id': 0,
            'textes_scanned': 0,
            'textes_matched': 0,
            'exported_libre': 0,
            'exported_non_libre': 0,
            'skipped_no_textes': 0,
            'pdf_converted': 0,
            'pdf_failed': 0,
        }

    def log(self, msg: str):
        """Affiche un message si verbose"""
        if self.verbose:
            print(msg)

    # =========================================================================
    # PARSING DES FICHES
    # =========================================================================

    def parse_fiche(self, filepath: Path) -> FicheInfo:
        """Extrait les informations d'une fiche .docx"""
        info = FicheInfo(path=str(filepath))

        if not DOCX_AVAILABLE:
            return info

        try:
            doc = Document(filepath)
            text = '\n'.join([p.text for p in doc.paragraphs])

            # Chercher l'identifiant édition
            match = re.search(r'Identifiant\s+[ée]dition\s*:\s*(Edi-\d+)', text, re.IGNORECASE)
            if match:
                info.edi_id = match.group(1)

            # Chercher le titre de l'œuvre
            titre_match = re.search(r'Titre\s*:\s*([^\n]+)', text)
            if titre_match:
                info.titre_oeuvre = titre_match.group(1).strip().strip('*').strip()

            # Chercher l'auteur
            auteur_match = re.search(r'Auteur\(s\)\s*:\s*([^\n]+)', text)
            if auteur_match:
                info.auteur = auteur_match.group(1).strip()

            # Chercher si libre de droits
            if re.search(r'Libre\s+de\s+droits\s*:\s*Oui', text, re.IGNORECASE):
                info.libre_de_droits = True

        except Exception as e:
            self.log(f"  Erreur lecture {filepath.name}: {e}")

        return info

    def scan_fiches(self):
        """Scanne toutes les fiches .docx et les indexe par Edi-XX"""
        if not self.fiches_dir or not self.fiches_dir.exists():
            self.log("Pas de dossier de fiches spécifié ou inexistant")
            return

        self.log(f"\n{'='*60}")
        self.log(f"SCAN DES FICHES: {self.fiches_dir}")
        self.log(f"{'='*60}")

        for filepath in self.fiches_dir.glob('*.docx'):
            if filepath.name.startswith('~$'):  # Fichiers temporaires Word
                continue

            self.stats['fiches_scanned'] += 1
            info = self.parse_fiche(filepath)

            if info.edi_id:
                self.stats['fiches_with_id'] += 1
                self.fiches_par_id[info.edi_id] = info
                self.log(f"  ✓ {filepath.name} → {info.edi_id} {'[LIBRE]' if info.libre_de_droits else ''}")
            else:
                self.log(f"  ✗ {filepath.name} → Pas d'Edi-XX trouvé")

        self.log(f"\n  Total: {self.stats['fiches_with_id']}/{self.stats['fiches_scanned']} fiches avec ID")

    # =========================================================================
    # PARSING DES VERTICAUX
    # =========================================================================

    def parse_vertical(self, filepath: Path) -> VerticalInfo:
        """Extrait les informations d'un fichier vertical"""
        info = VerticalInfo(path=str(filepath), filename=filepath.stem)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Lire les premières lignes pour trouver <doc>
                for _ in range(100):
                    line = f.readline()
                    if not line:
                        break

                    # Chercher edition_id
                    match = re.search(r'edition_id="(Edi-\d+)"', line)
                    if match:
                        info.edi_id = match.group(1)

                    # Chercher source
                    source_match = re.search(r'source="([^"]+)"', line)
                    if source_match:
                        info.source = source_match.group(1)

                    # Chercher title
                    title_match = re.search(r'title="([^"]+)"', line)
                    if title_match:
                        info.title = title_match.group(1)

                    if info.edi_id:
                        break

        except Exception as e:
            self.log(f"  Erreur lecture {filepath.name}: {e}")

        return info

    def scan_verticaux(self):
        """Scanne tous les fichiers verticaux - chaque vertical = une œuvre"""
        if not self.verticaux_dir or not self.verticaux_dir.exists():
            self.log("Pas de dossier de verticaux spécifié ou inexistant")
            return

        self.log(f"\n{'='*60}")
        self.log(f"SCAN DES VERTICAUX: {self.verticaux_dir}")
        self.log(f"{'='*60}")

        for filepath in sorted(self.verticaux_dir.glob('*.txt')):
            self.stats['verticaux_scanned'] += 1
            info = self.parse_vertical(filepath)

            if info.edi_id:
                self.stats['verticaux_with_id'] += 1

                # Clé unique = nom du fichier sans extension
                nom_fichier = filepath.stem
                nom_oeuvre = info.source or info.title or nom_fichier

                # Créer l'œuvre
                oeuvre = OeuvreItem(
                    oeuvre_key=nom_fichier,
                    edi_id=info.edi_id,
                    nom_oeuvre=nom_oeuvre,
                    vertical=info,
                )

                # Associer la fiche si elle existe pour cet ID
                if info.edi_id in self.fiches_par_id:
                    fiche = self.fiches_par_id[info.edi_id]
                    oeuvre.fiche = fiche
                    oeuvre.libre_de_droits = fiche.libre_de_droits

                self.oeuvres[nom_fichier] = oeuvre
                self.log(f"  ✓ {filepath.name} → {info.edi_id} ({nom_oeuvre[:40]}...)")
            else:
                self.log(f"  ✗ {filepath.name} → Pas d'Edi-XX trouvé")

        self.log(f"\n  Total: {self.stats['verticaux_with_id']}/{self.stats['verticaux_scanned']} verticaux avec ID")

    # =========================================================================
    # PARSING DES TEXTES
    # =========================================================================

    def parse_textes_dir(self, dirpath: Path) -> TextesInfo:
        """Extrait les informations d'un dossier de textes"""
        info = TextesInfo(path=str(dirpath), dirname=dirpath.name)

        # Vérifier si pages_index.json existe
        pages_index_path = dirpath / 'pages_index.json'
        info.has_pages_index = pages_index_path.exists()

        if info.has_pages_index:
            try:
                with open(pages_index_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Extraire l'Edi-XX depuis les métadonnées
                if 'pages' in data and len(data['pages']) > 0:
                    metadata = data['pages'][0].get('metadata', {})

                    # Chercher edition_id
                    edi_id = metadata.get('edition_id')
                    if edi_id:
                        info.edi_id = edi_id

                    # Chercher source
                    info.source = metadata.get('source')

            except Exception as e:
                self.log(f"  Erreur lecture pages_index.json dans {dirpath.name}: {e}")

        return info

    def scan_textes(self):
        """Scanne tous les dossiers de textes et les matche par nom"""
        if not self.textes_dir or not self.textes_dir.exists():
            self.log("Pas de dossier de textes spécifié ou inexistant")
            return

        self.log(f"\n{'='*60}")
        self.log(f"SCAN DES TEXTES: {self.textes_dir}")
        self.log(f"{'='*60}")

        for item in sorted(self.textes_dir.iterdir()):
            if not item.is_dir():
                continue

            self.stats['textes_scanned'] += 1
            info = self.parse_textes_dir(item)
            dirname = item.name

            # Essai 1: Match exact
            if dirname in self.oeuvres:
                self.oeuvres[dirname].textes = info
                self.stats['textes_matched'] += 1
                self.log(f"  ✓ {dirname} → match exact")
                continue

            # Essai 2: Enlever le suffixe _Edi-XX pour matcher
            # Format: nom_fichier_Edi-XX -> nom_fichier
            match_edi = re.match(r'^(.+)_(Edi-\d+)$', dirname)
            if match_edi:
                base_name = match_edi.group(1)
                edi_id = match_edi.group(2)

                if base_name in self.oeuvres:
                    if self.oeuvres[base_name].edi_id == edi_id:
                        self.oeuvres[base_name].textes = info
                        self.stats['textes_matched'] += 1
                        self.log(f"  ✓ {dirname} → {base_name}")
                        continue

                # Essai avec match partiel du nom de base
                matched = False
                for key in self.oeuvres.keys():
                    if key == base_name or key.startswith(base_name) or base_name.startswith(key):
                        if self.oeuvres[key].edi_id == edi_id:
                            self.oeuvres[key].textes = info
                            self.stats['textes_matched'] += 1
                            self.log(f"  ✓ {dirname} → {key} (match partiel)")
                            matched = True
                            break

                if matched:
                    continue

            # Essai 3: Match partiel (ancien comportement)
            matched = False
            for key in self.oeuvres.keys():
                if key.startswith(dirname) or dirname.startswith(key):
                    self.oeuvres[key].textes = info
                    self.stats['textes_matched'] += 1
                    self.log(f"  ✓ {dirname} → {key} (match partiel)")
                    matched = True
                    break

            if not matched:
                self.log(f"  ✗ {dirname} → Pas de match trouvé")

        self.log(f"\n  Total: {self.stats['textes_matched']}/{self.stats['textes_scanned']} dossiers matchés")

    # =========================================================================
    # CONVERSION PDF
    # =========================================================================

    def convert_docx_to_pdf(self, docx_path: Path, output_dir: Path) -> Optional[Path]:
        """Convertit un fichier .docx en .pdf via LibreOffice"""
        try:
            result = subprocess.run([
                'soffice', '--headless', '--convert-to', 'pdf',
                '--outdir', str(output_dir), str(docx_path)
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                pdf_path = output_dir / docx_path.with_suffix('.pdf').name
                if pdf_path.exists():
                    self.stats['pdf_converted'] += 1
                    return pdf_path

            self.stats['pdf_failed'] += 1
            return None

        except subprocess.TimeoutExpired:
            self.log(f"    Timeout conversion {docx_path.name}")
            self.stats['pdf_failed'] += 1
            return None
        except FileNotFoundError:
            self.log("    LibreOffice (soffice) non trouvé!")
            self.stats['pdf_failed'] += 1
            return None
        except Exception as e:
            self.log(f"    Erreur conversion: {e}")
            self.stats['pdf_failed'] += 1
            return None

    # =========================================================================
    # CREATION DE LA STRUCTURE D'EXPORT
    # =========================================================================

    def normalize_filename(self, name: str, max_length: int = 80) -> str:
        """Normalise un nom pour l'utiliser comme nom de dossier"""
        if not name:
            return "Inconnu"
        # Remplacer les caractères problématiques
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        name = re.sub(r'\s+', '_', name)
        name = re.sub(r'_+', '_', name)
        name = name.strip('_')
        # Limiter la longueur
        if len(name) > max_length:
            name = name[:max_length].rstrip('_')
        return name

    def create_export_structure(self):
        """Crée la structure d'export par œuvre"""
        self.log(f"\n{'='*60}")
        self.log(f"CRÉATION DE L'EXPORT: {self.output_dir}")
        self.log(f"{'='*60}")

        # Créer les dossiers de base
        libre_dir = self.output_dir / 'Libre_de_droits'
        non_libre_dir = self.output_dir / 'Non_libre_de_droits'
        libre_dir.mkdir(parents=True, exist_ok=True)
        non_libre_dir.mkdir(parents=True, exist_ok=True)

        for oeuvre_key, oeuvre in sorted(self.oeuvres.items(),
                                          key=lambda x: (int(x[1].edi_id.split('-')[1]), x[0])):

            # Vérifier si on peut exporter (vertical ET textes avec pages_index requis)
            if not oeuvre.textes or not oeuvre.textes.has_pages_index:
                self.stats['skipped_no_textes'] += 1
                oeuvre.errors.append("Pas de textes ou pages_index.json manquant")
                continue

            # Déterminer le dossier de destination
            base_dir = libre_dir if oeuvre.libre_de_droits else non_libre_dir
            folder_name = f"{self.normalize_filename(oeuvre.nom_oeuvre)}_{oeuvre.edi_id}"
            export_path = base_dir / folder_name

            self.log(f"\n  {oeuvre.edi_id} - {oeuvre.nom_oeuvre[:40]}...")
            self.log(f"    → {'Libre' if oeuvre.libre_de_droits else 'Non libre'}")

            try:
                # Créer le dossier
                export_path.mkdir(parents=True, exist_ok=True)
                oeuvre.export_path = str(export_path)

                # 1. Copier le fichier vertical
                if oeuvre.vertical:
                    src = Path(oeuvre.vertical.path)
                    dst = export_path / 'vertical.txt'
                    shutil.copy2(src, dst)
                    self.log(f"    ✓ vertical.txt")

                # 2. Copier le dossier textes (contenu)
                if oeuvre.textes:
                    src_dir = Path(oeuvre.textes.path)
                    for src_file in src_dir.iterdir():
                        if src_file.is_file():
                            dst = export_path / src_file.name
                            shutil.copy2(src_file, dst)
                    self.log(f"    ✓ {len(list(src_dir.glob('*')))} fichiers textes")

                # 3. Convertir et copier la fiche
                if oeuvre.fiche:
                    pdf_path = self.convert_docx_to_pdf(Path(oeuvre.fiche.path), export_path)
                    if pdf_path:
                        # Renommer en fiche.pdf
                        final_path = export_path / 'fiche.pdf'
                        if pdf_path != final_path:
                            pdf_path.rename(final_path)
                        self.log(f"    ✓ fiche.pdf")
                    else:
                        self.log(f"    ⚠ Échec conversion fiche PDF")
                        oeuvre.errors.append("Échec conversion PDF")
                else:
                    self.log(f"    ⚠ Pas de fiche")

                oeuvre.exported = True
                if oeuvre.libre_de_droits:
                    self.stats['exported_libre'] += 1
                else:
                    self.stats['exported_non_libre'] += 1

            except Exception as e:
                self.log(f"    ✗ Erreur: {e}")
                oeuvre.errors.append(str(e))

    # =========================================================================
    # RAPPORT
    # =========================================================================

    def generate_report(self) -> str:
        """Génère le rapport d'export"""
        lines = []
        lines.append("=" * 80)
        lines.append("RAPPORT D'EXPORT NAKALA (PAR ŒUVRE)")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        lines.append("\nSTATISTIQUES")
        lines.append("-" * 40)
        lines.append(f"Fiches scannées: {self.stats['fiches_with_id']}/{self.stats['fiches_scanned']}")
        lines.append(f"Œuvres (verticaux): {self.stats['verticaux_with_id']}/{self.stats['verticaux_scanned']}")
        lines.append(f"Dossiers textes matchés: {self.stats['textes_matched']}/{self.stats['textes_scanned']}")

        lines.append(f"\nEXPORTS CRÉÉS")
        lines.append("-" * 40)
        lines.append(f"Libre de droits: {self.stats['exported_libre']}")
        lines.append(f"Non libre de droits: {self.stats['exported_non_libre']}")
        lines.append(f"Total exportés: {self.stats['exported_libre'] + self.stats['exported_non_libre']}")

        lines.append(f"\nNON EXPORTÉS")
        lines.append("-" * 40)
        lines.append(f"Sans textes/pages_index: {self.stats['skipped_no_textes']}")

        lines.append(f"\nCONVERSION PDF")
        lines.append("-" * 40)
        lines.append(f"Réussies: {self.stats['pdf_converted']}")
        lines.append(f"Échouées: {self.stats['pdf_failed']}")

        # Liste des exports réussis
        exported = [oeuvre for oeuvre in self.oeuvres.values() if oeuvre.exported]
        if exported:
            lines.append(f"\n{'='*80}")
            lines.append(f"EXPORTS RÉUSSIS ({len(exported)})")
            lines.append("=" * 80)

            libres = [oeuvre for oeuvre in exported if oeuvre.libre_de_droits]
            non_libres = [oeuvre for oeuvre in exported if not oeuvre.libre_de_droits]

            if libres:
                lines.append(f"\n[LIBRE DE DROITS] ({len(libres)})")
                for oeuvre in sorted(libres, key=lambda x: int(x.edi_id.split('-')[1])):
                    status = "✓" if not oeuvre.errors else f"⚠ {', '.join(oeuvre.errors)}"
                    lines.append(f"  {oeuvre.edi_id} - {oeuvre.nom_oeuvre[:50]} : {status}")

            if non_libres:
                lines.append(f"\n[NON LIBRE DE DROITS] ({len(non_libres)})")
                for oeuvre in sorted(non_libres, key=lambda x: int(x.edi_id.split('-')[1])):
                    status = "✓" if not oeuvre.errors else f"⚠ {', '.join(oeuvre.errors)}"
                    lines.append(f"  {oeuvre.edi_id} - {oeuvre.nom_oeuvre[:50]} : {status}")

        # Liste des non exportés
        not_exported = [oeuvre for oeuvre in self.oeuvres.values() if not oeuvre.exported]
        if not_exported:
            lines.append(f"\n{'='*80}")
            lines.append(f"NON EXPORTÉS (données manquantes) ({len(not_exported)})")
            lines.append("=" * 80)
            for oeuvre in sorted(not_exported, key=lambda x: int(x.edi_id.split('-')[1])):
                lines.append(f"  {oeuvre.edi_id} - {oeuvre.nom_oeuvre[:50]}")
                for error in oeuvre.errors:
                    lines.append(f"      → {error}")

        lines.append("\n" + "=" * 80)
        lines.append("FIN DU RAPPORT")
        lines.append("=" * 80)

        return '\n'.join(lines)

    # =========================================================================
    # EXÉCUTION PRINCIPALE
    # =========================================================================

    def run(self):
        """Exécute le processus complet"""
        print("\n" + "=" * 60)
        print("PRÉPARATION EXPORT NAKALA (PAR ŒUVRE)")
        print("=" * 60)

        # 1. Scanner les fiches (indexées par Edi-XX)
        self.scan_fiches()

        # 2. Scanner les verticaux (chaque vertical = une œuvre)
        self.scan_verticaux()

        # 3. Scanner et matcher les textes
        self.scan_textes()

        # 4. Créer la structure d'export
        self.create_export_structure()

        # 5. Générer le rapport
        report = self.generate_report()

        # Sauvegarder le rapport
        report_path = self.output_dir / 'rapport_export.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n{report}")
        print(f"\nRapport sauvegardé: {report_path}")

        return self.oeuvres


def main():
    parser = argparse.ArgumentParser(
        description="Prépare l'export Nakala pour Heimdall (version par œuvre)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
    python prepare_nakala_export.py \\
        --fiches ./Fiches_Editions_Metadonnee/ \\
        --verticaux ./Verticaux/ \\
        --textes ./Textes/ \\
        --output ./input/CiSaMe/
        """
    )
    parser.add_argument('--fiches', '-f', required=True,
                        help='Dossier des fiches .docx')
    parser.add_argument('--verticaux', '-v', required=True,
                        help='Dossier des fichiers verticaux .txt')
    parser.add_argument('--textes', '-t', required=True,
                        help='Dossier des sous-dossiers de textes (avec pages_index.json)')
    parser.add_argument('--output', '-o', default='./input/CiSaMe',
                        help='Dossier de sortie (défaut: ./input/CiSaMe)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Mode silencieux')

    args = parser.parse_args()

    preparer = NakalaExportPreparer(
        fiches_dir=args.fiches,
        verticaux_dir=args.verticaux,
        textes_dir=args.textes,
        output_dir=args.output,
        verbose=not args.quiet,
    )

    preparer.run()


if __name__ == '__main__':
    main()
