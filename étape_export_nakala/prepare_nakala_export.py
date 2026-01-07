#!/usr/bin/env python3
"""
Préparation de l'export Nakala pour le projet CiSaMe

Ce script prépare la structure de dossiers pour l'upload via Heimdall en :
1. Parsant les fiches .docx pour extraire Edi-XX et statut libre de droits
2. Associant les verticaux et textes (sortie PAGEtopage) par Edi-XX
3. Créant la structure Libre_de_droits / Non_libre_de_droits
4. Convertissant les fiches .docx → .pdf
5. Générant un rapport de l'export

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
    edi_id: Optional[str] = None
    source: Optional[str] = None


@dataclass
class TextesInfo:
    """Informations extraites d'un dossier de textes"""
    path: str
    edi_id: Optional[str] = None
    source: Optional[str] = None
    has_pages_index: bool = False


@dataclass
class ExportItem:
    """Un item complet à exporter"""
    edi_id: str
    source: str
    libre_de_droits: bool
    fiche: Optional[FicheInfo] = None
    vertical: Optional[VerticalInfo] = None
    textes: Optional[TextesInfo] = None
    export_path: Optional[str] = None
    exported: bool = False
    errors: List[str] = field(default_factory=list)


class NakalaExportPreparer:
    """Prépare l'export Nakala pour Heimdall"""

    def __init__(self, fiches_dir: str, verticaux_dir: str, textes_dir: str,
                 output_dir: str, verbose: bool = True):
        self.fiches_dir = Path(fiches_dir) if fiches_dir else None
        self.verticaux_dir = Path(verticaux_dir) if verticaux_dir else None
        self.textes_dir = Path(textes_dir) if textes_dir else None
        self.output_dir = Path(output_dir)
        self.verbose = verbose

        # Index par Edi-XX
        self.fiches_index: Dict[str, FicheInfo] = {}
        self.verticaux_index: Dict[str, VerticalInfo] = {}
        self.textes_index: Dict[str, TextesInfo] = {}

        # Items à exporter
        self.export_items: Dict[str, ExportItem] = {}

        # Stats
        self.stats = {
            'fiches_scanned': 0,
            'fiches_with_id': 0,
            'verticaux_scanned': 0,
            'verticaux_with_id': 0,
            'textes_scanned': 0,
            'textes_with_id': 0,
            'exported_libre': 0,
            'exported_non_libre': 0,
            'skipped_no_vertical': 0,
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
        """Scanne toutes les fiches .docx"""
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
                self.fiches_index[info.edi_id] = info
                self.log(f"  ✓ {filepath.name} → {info.edi_id} {'[LIBRE]' if info.libre_de_droits else ''}")
            else:
                self.log(f"  ✗ {filepath.name} → Pas d'Edi-XX trouvé")

        self.log(f"\n  Total: {self.stats['fiches_with_id']}/{self.stats['fiches_scanned']} fiches avec ID")

    # =========================================================================
    # PARSING DES VERTICAUX
    # =========================================================================

    def parse_vertical(self, filepath: Path) -> VerticalInfo:
        """Extrait les informations d'un fichier vertical"""
        info = VerticalInfo(path=str(filepath))

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

                    if info.edi_id:
                        break

        except Exception as e:
            self.log(f"  Erreur lecture {filepath.name}: {e}")

        return info

    def scan_verticaux(self):
        """Scanne tous les fichiers verticaux"""
        if not self.verticaux_dir or not self.verticaux_dir.exists():
            self.log("Pas de dossier de verticaux spécifié ou inexistant")
            return

        self.log(f"\n{'='*60}")
        self.log(f"SCAN DES VERTICAUX: {self.verticaux_dir}")
        self.log(f"{'='*60}")

        # Chercher les .txt et .vertical.txt
        patterns = ['*.txt', '*.vertical.txt']
        files = set()
        for pattern in patterns:
            files.update(self.verticaux_dir.glob(pattern))

        for filepath in sorted(files):
            self.stats['verticaux_scanned'] += 1
            info = self.parse_vertical(filepath)

            if info.edi_id:
                self.stats['verticaux_with_id'] += 1
                # Si plusieurs verticaux pour le même ID, garder tous
                if info.edi_id not in self.verticaux_index:
                    self.verticaux_index[info.edi_id] = info
                    self.log(f"  ✓ {filepath.name} → {info.edi_id}")
                else:
                    self.log(f"  ⚠ {filepath.name} → {info.edi_id} (doublon, ignoré)")
            else:
                self.log(f"  ✗ {filepath.name} → Pas d'Edi-XX trouvé")

        self.log(f"\n  Total: {self.stats['verticaux_with_id']}/{self.stats['verticaux_scanned']} verticaux avec ID")

    # =========================================================================
    # PARSING DES TEXTES
    # =========================================================================

    def parse_textes_dir(self, dirpath: Path) -> TextesInfo:
        """Extrait les informations d'un dossier de textes"""
        info = TextesInfo(path=str(dirpath))

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
        else:
            # Essayer de lire depuis les fichiers .txt
            for txt_file in list(dirpath.glob('page_*.txt'))[:1]:
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        content = f.read(2000)

                    match = re.search(r'Edition\s+ID\s*:\s*(Edi-\d+)', content)
                    if match:
                        info.edi_id = match.group(1)

                    source_match = re.search(r'Source\s*:\s*([^\n]+)', content)
                    if source_match:
                        info.source = source_match.group(1).strip()

                except Exception as e:
                    pass

        return info

    def scan_textes(self):
        """Scanne tous les dossiers de textes"""
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

            if info.edi_id:
                self.stats['textes_with_id'] += 1
                self.textes_index[info.edi_id] = info
                status = "✓" if info.has_pages_index else "⚠ (sans pages_index.json)"
                self.log(f"  {status} {item.name} → {info.edi_id}")
            else:
                self.log(f"  ✗ {item.name} → Pas d'Edi-XX trouvé")

        self.log(f"\n  Total: {self.stats['textes_with_id']}/{self.stats['textes_scanned']} dossiers avec ID")

    # =========================================================================
    # ASSOCIATION ET CREATION DES ITEMS
    # =========================================================================

    def build_export_items(self):
        """Construit la liste des items à exporter"""
        self.log(f"\n{'='*60}")
        self.log("ASSOCIATION DES DONNÉES")
        self.log(f"{'='*60}")

        # Collecter tous les Edi-XX uniques
        all_ids = set(self.fiches_index.keys()) | set(self.verticaux_index.keys()) | set(self.textes_index.keys())

        for edi_id in sorted(all_ids, key=lambda x: int(x.split('-')[1])):
            fiche = self.fiches_index.get(edi_id)
            vertical = self.verticaux_index.get(edi_id)
            textes = self.textes_index.get(edi_id)

            # Déterminer le nom source
            source = "Inconnu"
            if textes and textes.source:
                source = textes.source
            elif vertical and vertical.source:
                source = vertical.source
            elif fiche and fiche.titre_oeuvre:
                source = fiche.titre_oeuvre

            # Déterminer si libre de droits
            libre = fiche.libre_de_droits if fiche else False

            item = ExportItem(
                edi_id=edi_id,
                source=source,
                libre_de_droits=libre,
                fiche=fiche,
                vertical=vertical,
                textes=textes,
            )

            # Vérifier ce qui manque
            if not vertical:
                item.errors.append("Pas de fichier vertical")
            if not textes:
                item.errors.append("Pas de dossier textes")
            if not textes or not textes.has_pages_index:
                item.errors.append("Pas de pages_index.json")

            self.export_items[edi_id] = item

        # Afficher le résumé
        complete = sum(1 for item in self.export_items.values()
                      if item.vertical and item.textes and item.textes.has_pages_index)
        self.log(f"\n  Total: {len(self.export_items)} Edi-XX uniques")
        self.log(f"  Complets (vertical + textes + pages_index): {complete}")

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
        """Crée la structure d'export"""
        self.log(f"\n{'='*60}")
        self.log(f"CRÉATION DE L'EXPORT: {self.output_dir}")
        self.log(f"{'='*60}")

        # Créer les dossiers de base
        libre_dir = self.output_dir / 'Libre_de_droits'
        non_libre_dir = self.output_dir / 'Non_libre_de_droits'
        libre_dir.mkdir(parents=True, exist_ok=True)
        non_libre_dir.mkdir(parents=True, exist_ok=True)

        for edi_id, item in sorted(self.export_items.items(),
                                   key=lambda x: int(x[0].split('-')[1])):

            # Vérifier si on peut exporter (vertical ET textes avec pages_index requis)
            if not item.vertical:
                self.stats['skipped_no_vertical'] += 1
                continue
            if not item.textes or not item.textes.has_pages_index:
                self.stats['skipped_no_textes'] += 1
                continue

            # Déterminer le dossier de destination
            base_dir = libre_dir if item.libre_de_droits else non_libre_dir
            folder_name = f"{self.normalize_filename(item.source)}_{edi_id}"
            export_path = base_dir / folder_name

            self.log(f"\n  {edi_id} - {item.source[:40]}...")
            self.log(f"    → {'Libre' if item.libre_de_droits else 'Non libre'}")

            try:
                # Créer le dossier
                export_path.mkdir(parents=True, exist_ok=True)
                item.export_path = str(export_path)

                # 1. Copier le fichier vertical
                if item.vertical:
                    src = Path(item.vertical.path)
                    dst = export_path / 'vertical.txt'
                    shutil.copy2(src, dst)
                    self.log(f"    ✓ vertical.txt")

                # 2. Copier le dossier textes (contenu)
                if item.textes:
                    src_dir = Path(item.textes.path)
                    for src_file in src_dir.iterdir():
                        if src_file.is_file():
                            dst = export_path / src_file.name
                            shutil.copy2(src_file, dst)
                    self.log(f"    ✓ {len(list(src_dir.glob('*')))} fichiers textes")

                # 3. Convertir et copier la fiche
                if item.fiche:
                    pdf_path = self.convert_docx_to_pdf(Path(item.fiche.path), export_path)
                    if pdf_path:
                        # Renommer en fiche.pdf
                        final_path = export_path / 'fiche.pdf'
                        if pdf_path != final_path:
                            pdf_path.rename(final_path)
                        self.log(f"    ✓ fiche.pdf")
                    else:
                        self.log(f"    ⚠ Échec conversion fiche PDF")
                        item.errors.append("Échec conversion PDF")
                else:
                    self.log(f"    ⚠ Pas de fiche")

                item.exported = True
                if item.libre_de_droits:
                    self.stats['exported_libre'] += 1
                else:
                    self.stats['exported_non_libre'] += 1

            except Exception as e:
                self.log(f"    ✗ Erreur: {e}")
                item.errors.append(str(e))

    # =========================================================================
    # RAPPORT
    # =========================================================================

    def generate_report(self) -> str:
        """Génère le rapport d'export"""
        lines = []
        lines.append("=" * 80)
        lines.append("RAPPORT D'EXPORT NAKALA")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        lines.append("\nSTATISTIQUES")
        lines.append("-" * 40)
        lines.append(f"Fiches scannées: {self.stats['fiches_with_id']}/{self.stats['fiches_scanned']}")
        lines.append(f"Verticaux scannés: {self.stats['verticaux_with_id']}/{self.stats['verticaux_scanned']}")
        lines.append(f"Dossiers textes scannés: {self.stats['textes_with_id']}/{self.stats['textes_scanned']}")

        lines.append(f"\nEXPORTS CRÉÉS")
        lines.append("-" * 40)
        lines.append(f"Libre de droits: {self.stats['exported_libre']}")
        lines.append(f"Non libre de droits: {self.stats['exported_non_libre']}")
        lines.append(f"Total exportés: {self.stats['exported_libre'] + self.stats['exported_non_libre']}")

        lines.append(f"\nNON EXPORTÉS")
        lines.append("-" * 40)
        lines.append(f"Sans vertical: {self.stats['skipped_no_vertical']}")
        lines.append(f"Sans textes/pages_index: {self.stats['skipped_no_textes']}")

        lines.append(f"\nCONVERSION PDF")
        lines.append("-" * 40)
        lines.append(f"Réussies: {self.stats['pdf_converted']}")
        lines.append(f"Échouées: {self.stats['pdf_failed']}")

        # Liste des exports réussis
        exported = [item for item in self.export_items.values() if item.exported]
        if exported:
            lines.append(f"\n{'='*80}")
            lines.append("EXPORTS RÉUSSIS")
            lines.append("=" * 80)

            libres = [item for item in exported if item.libre_de_droits]
            non_libres = [item for item in exported if not item.libre_de_droits]

            if libres:
                lines.append("\n[LIBRE DE DROITS]")
                for item in libres:
                    status = "✓" if not item.errors else f"⚠ {', '.join(item.errors)}"
                    lines.append(f"  {item.edi_id} - {item.source[:50]} : {status}")

            if non_libres:
                lines.append("\n[NON LIBRE DE DROITS]")
                for item in non_libres:
                    status = "✓" if not item.errors else f"⚠ {', '.join(item.errors)}"
                    lines.append(f"  {item.edi_id} - {item.source[:50]} : {status}")

        # Liste des non exportés
        not_exported = [item for item in self.export_items.values() if not item.exported]
        if not_exported:
            lines.append(f"\n{'='*80}")
            lines.append("NON EXPORTÉS (données manquantes)")
            lines.append("=" * 80)
            for item in not_exported:
                lines.append(f"  {item.edi_id} - {item.source[:50]}")
                for error in item.errors:
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
        print("PRÉPARATION EXPORT NAKALA")
        print("=" * 60)

        # 1. Scanner les sources
        self.scan_fiches()
        self.scan_verticaux()
        self.scan_textes()

        # 2. Associer les données
        self.build_export_items()

        # 3. Créer la structure d'export
        self.create_export_structure()

        # 4. Générer le rapport
        report = self.generate_report()

        # Sauvegarder le rapport
        report_path = self.output_dir / 'rapport_export.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n{report}")
        print(f"\nRapport sauvegardé: {report_path}")

        return self.export_items


def main():
    parser = argparse.ArgumentParser(
        description="Prépare l'export Nakala pour Heimdall",
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
