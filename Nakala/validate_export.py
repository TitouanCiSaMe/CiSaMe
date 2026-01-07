#!/usr/bin/env python3
"""
Validation des données avant export Nakala

Ce script vérifie la cohérence des données avant de lancer l'export :
- Vérifie que chaque Edi-XX a bien un vertical, des textes et une fiche
- Valide le format des pages_index.json
- Détecte les incohérences entre les sources de données
- Génère un rapport de validation

Usage:
    python validate_export.py \
        --fiches ./Fiches_Editions_Metadonnee/ \
        --verticaux ./Verticaux/ \
        --textes ./Textes/

Auteur: Projet CiSaMe - Janvier 2025
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


@dataclass
class ValidationResult:
    """Résultat de validation pour un Edi-XX"""
    edi_id: str
    has_fiche: bool = False
    has_vertical: bool = False
    has_textes: bool = False
    has_pages_index: bool = False
    fiche_libre: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return self.has_fiche and self.has_vertical and self.has_textes and self.has_pages_index

    @property
    def is_exportable(self) -> bool:
        """Exportable si vertical + textes + pages_index"""
        return self.has_vertical and self.has_textes and self.has_pages_index

    @property
    def status(self) -> str:
        if self.is_complete:
            return "COMPLET"
        elif self.is_exportable:
            return "EXPORTABLE (sans fiche)"
        else:
            return "INCOMPLET"


class ExportValidator:
    """Validateur des données pour export Nakala"""

    REQUIRED_METADATA_FIELDS = ['source', 'author', 'type']
    OPTIONAL_METADATA_FIELDS = ['date', 'edition_id']

    def __init__(self, fiches_dir: str, verticaux_dir: str, textes_dir: str):
        self.fiches_dir = Path(fiches_dir) if fiches_dir else None
        self.verticaux_dir = Path(verticaux_dir) if verticaux_dir else None
        self.textes_dir = Path(textes_dir) if textes_dir else None

        self.results: Dict[str, ValidationResult] = {}

        # Index des données trouvées
        self.fiches_data: Dict[str, dict] = {}
        self.verticaux_data: Dict[str, dict] = {}
        self.textes_data: Dict[str, dict] = {}

    def extract_edi_from_fiche(self, filepath: Path) -> Optional[dict]:
        """Extrait les données d'une fiche .docx"""
        if not DOCX_AVAILABLE:
            return None

        try:
            doc = Document(filepath)
            text = '\n'.join([p.text for p in doc.paragraphs])

            data = {
                'path': str(filepath),
                'edi_id': None,
                'titre': None,
                'auteur': None,
                'libre': False,
            }

            # Extraire Edi-XX
            match = re.search(r'Identifiant\s+[ée]dition\s*:\s*(Edi-\d+)', text, re.IGNORECASE)
            if match:
                data['edi_id'] = match.group(1)

            # Extraire titre
            titre_match = re.search(r'Titre\s*:\s*([^\n]+)', text)
            if titre_match:
                data['titre'] = titre_match.group(1).strip()

            # Extraire auteur
            auteur_match = re.search(r'Auteur\(s\)\s*:\s*([^\n]+)', text)
            if auteur_match:
                data['auteur'] = auteur_match.group(1).strip()

            # Libre de droits
            if re.search(r'Libre\s+de\s+droits\s*:\s*Oui', text, re.IGNORECASE):
                data['libre'] = True

            return data

        except Exception as e:
            return {'path': str(filepath), 'error': str(e)}

    def extract_edi_from_vertical(self, filepath: Path) -> Optional[dict]:
        """Extrait les données d'un fichier vertical"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(5000)

            data = {
                'path': str(filepath),
                'edi_id': None,
                'source': None,
                'author': None,
            }

            # Extraire edition_id
            match = re.search(r'edition_id="(Edi-\d+)"', content)
            if match:
                data['edi_id'] = match.group(1)

            # Extraire source
            source_match = re.search(r'source="([^"]+)"', content)
            if source_match:
                data['source'] = source_match.group(1)

            # Extraire author
            author_match = re.search(r'author="([^"]+)"', content)
            if author_match:
                data['author'] = author_match.group(1)

            return data

        except Exception as e:
            return {'path': str(filepath), 'error': str(e)}

    def extract_edi_from_textes(self, dirpath: Path) -> Optional[dict]:
        """Extrait les données d'un dossier de textes"""
        data = {
            'path': str(dirpath),
            'edi_id': None,
            'source': None,
            'has_pages_index': False,
            'pages_index_valid': False,
            'metadata_fields': [],
            'page_count': 0,
        }

        # Vérifier pages_index.json
        pages_index_path = dirpath / 'pages_index.json'
        if pages_index_path.exists():
            data['has_pages_index'] = True

            try:
                with open(pages_index_path, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)

                if 'pages' in index_data and len(index_data['pages']) > 0:
                    data['pages_index_valid'] = True
                    data['page_count'] = len(index_data['pages'])

                    metadata = index_data['pages'][0].get('metadata', {})
                    data['metadata_fields'] = list(metadata.keys())
                    data['edi_id'] = metadata.get('edition_id')
                    data['source'] = metadata.get('source')

            except json.JSONDecodeError as e:
                data['error'] = f"JSON invalide: {e}"
            except Exception as e:
                data['error'] = str(e)

        # Compter les fichiers page_*.txt
        page_files = list(dirpath.glob('page_*.txt'))
        if not data['page_count']:
            data['page_count'] = len(page_files)

        return data

    def scan_all(self):
        """Scanne toutes les sources de données"""
        print("Scan des fiches...")
        if self.fiches_dir and self.fiches_dir.exists():
            for filepath in self.fiches_dir.glob('*.docx'):
                if filepath.name.startswith('~$'):
                    continue
                data = self.extract_edi_from_fiche(filepath)
                if data and data.get('edi_id'):
                    self.fiches_data[data['edi_id']] = data

        print("Scan des verticaux...")
        if self.verticaux_dir and self.verticaux_dir.exists():
            for filepath in self.verticaux_dir.glob('*.txt'):
                data = self.extract_edi_from_vertical(filepath)
                if data and data.get('edi_id'):
                    self.verticaux_data[data['edi_id']] = data

        print("Scan des textes...")
        if self.textes_dir and self.textes_dir.exists():
            for dirpath in self.textes_dir.iterdir():
                if not dirpath.is_dir():
                    continue
                data = self.extract_edi_from_textes(dirpath)
                if data and data.get('edi_id'):
                    self.textes_data[data['edi_id']] = data

    def validate(self):
        """Effectue la validation"""
        # Collecter tous les Edi-XX
        all_ids = set(self.fiches_data.keys()) | set(self.verticaux_data.keys()) | set(self.textes_data.keys())

        for edi_id in all_ids:
            result = ValidationResult(edi_id=edi_id)

            fiche = self.fiches_data.get(edi_id)
            vertical = self.verticaux_data.get(edi_id)
            textes = self.textes_data.get(edi_id)

            # Vérifier la présence
            result.has_fiche = fiche is not None
            result.has_vertical = vertical is not None
            result.has_textes = textes is not None

            if fiche:
                result.fiche_libre = fiche.get('libre', False)
                if fiche.get('error'):
                    result.errors.append(f"Erreur fiche: {fiche['error']}")

            if vertical:
                if vertical.get('error'):
                    result.errors.append(f"Erreur vertical: {vertical['error']}")

            if textes:
                result.has_pages_index = textes.get('has_pages_index', False)

                if not result.has_pages_index:
                    result.errors.append("Pas de pages_index.json")
                elif not textes.get('pages_index_valid'):
                    result.errors.append("pages_index.json invalide ou vide")
                else:
                    # Vérifier les champs requis
                    metadata_fields = textes.get('metadata_fields', [])
                    for field in self.REQUIRED_METADATA_FIELDS:
                        if field not in metadata_fields:
                            result.warnings.append(f"Champ manquant dans pages_index: {field}")

                if textes.get('error'):
                    result.errors.append(f"Erreur textes: {textes['error']}")

            # Vérifier la cohérence des sources
            sources = []
            if fiche and fiche.get('titre'):
                sources.append(('fiche', fiche['titre']))
            if vertical and vertical.get('source'):
                sources.append(('vertical', vertical['source']))
            if textes and textes.get('source'):
                sources.append(('textes', textes['source']))

            if len(sources) > 1:
                # Vérifier si les sources sont cohérentes (simpliste)
                source_values = [s[1] for s in sources]
                if len(set(source_values)) > 1:
                    result.warnings.append(f"Sources différentes: {sources}")

            self.results[edi_id] = result

    def generate_report(self) -> str:
        """Génère le rapport de validation"""
        lines = []
        lines.append("=" * 80)
        lines.append("RAPPORT DE VALIDATION - EXPORT NAKALA")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        # Statistiques globales
        total = len(self.results)
        complete = sum(1 for r in self.results.values() if r.is_complete)
        exportable = sum(1 for r in self.results.values() if r.is_exportable)
        incomplete = total - exportable

        libres_exportables = sum(1 for r in self.results.values() if r.is_exportable and r.fiche_libre)
        non_libres_exportables = sum(1 for r in self.results.values() if r.is_exportable and not r.fiche_libre)

        lines.append("\nSTATISTIQUES GLOBALES")
        lines.append("-" * 40)
        lines.append(f"Total Edi-XX trouvés: {total}")
        lines.append(f"  - Complets (fiche + vertical + textes): {complete}")
        lines.append(f"  - Exportables (vertical + textes): {exportable}")
        lines.append(f"  - Non exportables: {incomplete}")
        lines.append(f"\nPar statut de droits (exportables):")
        lines.append(f"  - Libre de droits: {libres_exportables}")
        lines.append(f"  - Non libre de droits: {non_libres_exportables}")

        lines.append("\nSOURCES SCANNÉES")
        lines.append("-" * 40)
        lines.append(f"Fiches avec Edi-XX: {len(self.fiches_data)}")
        lines.append(f"Verticaux avec Edi-XX: {len(self.verticaux_data)}")
        lines.append(f"Dossiers textes avec Edi-XX: {len(self.textes_data)}")

        # Items complets
        complete_items = [r for r in self.results.values() if r.is_complete]
        if complete_items:
            lines.append(f"\n{'='*80}")
            lines.append("ITEMS COMPLETS (prêts pour export)")
            lines.append("=" * 80)
            for result in sorted(complete_items, key=lambda x: int(x.edi_id.split('-')[1])):
                status = "[LIBRE]" if result.fiche_libre else "[NON LIBRE]"
                lines.append(f"  ✓ {result.edi_id} {status}")

        # Items exportables mais sans fiche
        exportable_no_fiche = [r for r in self.results.values() if r.is_exportable and not r.has_fiche]
        if exportable_no_fiche:
            lines.append(f"\n{'='*80}")
            lines.append("EXPORTABLES SANS FICHE (à compléter)")
            lines.append("=" * 80)
            for result in sorted(exportable_no_fiche, key=lambda x: int(x.edi_id.split('-')[1])):
                lines.append(f"  ⚠ {result.edi_id}")

        # Items non exportables
        non_exportable = [r for r in self.results.values() if not r.is_exportable]
        if non_exportable:
            lines.append(f"\n{'='*80}")
            lines.append("NON EXPORTABLES (données manquantes)")
            lines.append("=" * 80)
            for result in sorted(non_exportable, key=lambda x: int(x.edi_id.split('-')[1])):
                missing = []
                if not result.has_vertical:
                    missing.append("vertical")
                if not result.has_textes:
                    missing.append("textes")
                if not result.has_pages_index:
                    missing.append("pages_index.json")
                lines.append(f"  ✗ {result.edi_id} - Manque: {', '.join(missing)}")

        # Warnings et erreurs
        items_with_warnings = [r for r in self.results.values() if r.warnings]
        if items_with_warnings:
            lines.append(f"\n{'='*80}")
            lines.append("AVERTISSEMENTS")
            lines.append("=" * 80)
            for result in items_with_warnings:
                lines.append(f"\n  {result.edi_id}:")
                for warning in result.warnings:
                    lines.append(f"    ⚠ {warning}")

        items_with_errors = [r for r in self.results.values() if r.errors]
        if items_with_errors:
            lines.append(f"\n{'='*80}")
            lines.append("ERREURS")
            lines.append("=" * 80)
            for result in items_with_errors:
                lines.append(f"\n  {result.edi_id}:")
                for error in result.errors:
                    lines.append(f"    ✗ {error}")

        lines.append("\n" + "=" * 80)
        lines.append("FIN DU RAPPORT")
        lines.append("=" * 80)

        return '\n'.join(lines)

    def run(self) -> str:
        """Exécute la validation complète"""
        self.scan_all()
        self.validate()
        return self.generate_report()


def main():
    parser = argparse.ArgumentParser(
        description="Valide les données avant export Nakala"
    )
    parser.add_argument('--fiches', '-f', required=True,
                        help='Dossier des fiches .docx')
    parser.add_argument('--verticaux', '-v', required=True,
                        help='Dossier des fichiers verticaux .txt')
    parser.add_argument('--textes', '-t', required=True,
                        help='Dossier des sous-dossiers de textes')
    parser.add_argument('--output', '-o', default=None,
                        help='Fichier de sortie pour le rapport (optionnel)')

    args = parser.parse_args()

    validator = ExportValidator(
        fiches_dir=args.fiches,
        verticaux_dir=args.verticaux,
        textes_dir=args.textes,
    )

    report = validator.run()
    print(report)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nRapport sauvegardé: {args.output}")


if __name__ == '__main__':
    main()
