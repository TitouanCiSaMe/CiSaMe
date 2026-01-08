"""
Générateur d'index et métadonnées

Génère les fichiers d'index JSON, mapping images, etc.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import logging

from ..models import AnnotatedPage

logger = logging.getLogger(__name__)


class IndexGenerator:
    """
    Génère les fichiers d'index et métadonnées

    Produit:
    - pages_index.json : Index de toutes les pages
    """

    def __init__(self, output_folder: Path):
        """
        Args:
            output_folder: Dossier de sortie
        """
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def generate_all(
        self,
        pages: List[AnnotatedPage],
        page_files: Dict[str, str]
    ) -> None:
        """
        Génère tous les fichiers d'index

        Args:
            pages: Liste des pages annotées
            page_files: Mapping {folio: chemin_fichier_sortie}
        """
        self.generate_pages_index(pages, page_files)

    def generate_pages_index(
        self,
        pages: List[AnnotatedPage],
        page_files: Dict[str, str]
    ) -> Path:
        """
        Génère l'index JSON des pages

        Args:
            pages: Liste des pages
            page_files: Mapping folio → fichier

        Returns:
            Chemin du fichier créé
        """
        index = {
            "generated_at": datetime.now().isoformat(),
            "total_pages": len(pages),
            "pages": []
        }

        for page in pages:
            meta = page.metadata
            corpus_meta = meta.corpus_metadata

            page_entry = {
                "folio": meta.folio,
                "page_number": meta.page_number,
                "running_title": meta.running_title,
                "is_empty": page.is_empty,
                "sentence_count": len(page.sentences),
                "token_count": sum(len(s.tokens) for s in page.sentences),
                "output_file": page_files.get(meta.folio, ""),
            }

            # Ajoute les métadonnées du corpus au niveau racine
            page_entry.update(corpus_meta)

            # Ajoute la structure 'metadata' pour compatibilité Nakala/Heimdall
            # Note: 'source' dans metadata correspond au titre (champ 'title' du corpus)
            # car l'algo Nakala utilise metadata['source'] pour créer le titre
            page_entry["metadata"] = {
                "source": corpus_meta.get("title", ""),
                "author": corpus_meta.get("author", ""),
                "type": corpus_meta.get("type", ""),
                "date": corpus_meta.get("date", ""),
                "edition_id": corpus_meta.get("edition_id", ""),
            }

            index["pages"].append(page_entry)

        output_path = self.output_folder / "pages_index.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

        logger.info(f"Index des pages généré: {output_path}")
        return output_path


def generate_index(
    pages: List[AnnotatedPage],
    page_files: Dict[str, str],
    output_folder: Path
) -> None:
    """
    Fonction utilitaire pour générer tous les index

    Args:
        pages: Liste des pages
        page_files: Mapping folio → fichier
        output_folder: Dossier de sortie
    """
    generator = IndexGenerator(output_folder)
    generator.generate_all(pages, page_files)
