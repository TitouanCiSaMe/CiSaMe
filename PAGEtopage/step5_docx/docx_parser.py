"""
Parseur de fichiers DOCX produits par latin_analyzer

Extrait le texte brut depuis les fichiers DOCX colores generes par
latin_analyzer, en ignorant l'en-tete (titre, legende, separateur).
"""

import re
from pathlib import Path
from typing import List, Optional
import logging

from docx import Document

from ..models import ExtractedPage, PageMetadata
from ..config import Config

logger = logging.getLogger(__name__)

# Textes a ignorer dans l'en-tete du DOCX latin_analyzer
HEADER_MARKERS = [
    "Analyse de texte latin",
    "Légende",
    "Noir =",
    "Orange =",
    "Rouge =",
]

# Separateur (ligne de underscores)
SEPARATOR_PATTERN = re.compile(r'^[_\-=]{10,}$')


class DocxParser:
    """
    Parse les fichiers DOCX issus de latin_analyzer

    Extrait le texte en ignorant l'en-tete de validation (titre, legende,
    separateur) et cree des ExtractedPage avec les metadonnees du config.yaml.

    Usage:
        config = Config.from_yaml("config.yaml")
        parser = DocxParser(config)
        pages = parser.parse_file("resultat.docx")
    """

    def __init__(self, config: Config):
        """
        Args:
            config: Configuration du pipeline (pour les metadonnees du corpus)
        """
        self.config = config

    def parse_file(self, file_path: str | Path) -> List[ExtractedPage]:
        """
        Parse un fichier DOCX et retourne des ExtractedPage

        Chaque fichier DOCX produit une seule ExtractedPage. Le folio
        est derive du nom de fichier.

        Args:
            file_path: Chemin vers le fichier DOCX

        Returns:
            Liste contenant une ExtractedPage
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Fichier non trouve: {file_path}")

        logger.info(f"Parsing du fichier DOCX: {file_path.name}")

        doc = Document(str(file_path))
        lines = self._extract_text_lines(doc)

        if not lines:
            logger.warning(f"Aucun texte extrait de {file_path.name}")
            return []

        logger.info(f"  {len(lines)} lignes de texte extraites")

        # Cree les metadonnees
        metadata = PageMetadata(
            folio=file_path.stem,
            page_number=1,
            running_title=self.config.corpus.title or "No running title",
            corpus_metadata=self.config.corpus.to_dict(),
        )

        page = ExtractedPage(
            metadata=metadata,
            lines=lines,
        )

        return [page]

    def parse_folder(
        self,
        folder_path: str | Path,
        pattern: str = "*.docx"
    ) -> List[ExtractedPage]:
        """
        Parse tous les fichiers DOCX d'un dossier

        Chaque fichier DOCX produit une ExtractedPage avec un page_number
        incremental.

        Args:
            folder_path: Dossier contenant les fichiers DOCX
            pattern: Pattern glob pour les fichiers

        Returns:
            Liste de ExtractedPage
        """
        folder_path = Path(folder_path)

        if not folder_path.exists():
            raise FileNotFoundError(f"Dossier non trouve: {folder_path}")

        if not folder_path.is_dir():
            raise NotADirectoryError(f"N'est pas un dossier: {folder_path}")

        files = sorted(folder_path.glob(pattern))

        if not files:
            logger.warning(
                f"Aucun fichier DOCX trouve avec le pattern '{pattern}' "
                f"dans {folder_path}"
            )
            return []

        logger.info(f"Parsing de {len(files)} fichiers DOCX depuis {folder_path}")

        all_pages = []
        for i, file_path in enumerate(files, start=1):
            try:
                pages = self.parse_file(file_path)
                # Met a jour le page_number
                for page in pages:
                    page.metadata.page_number = i
                all_pages.extend(pages)
            except Exception as e:
                logger.error(f"Erreur lors du parsing de {file_path}: {e}")

        logger.info(f"Total: {len(all_pages)} pages extraites depuis {len(files)} fichiers")
        return all_pages

    def _extract_text_lines(self, doc: Document) -> List[str]:
        """
        Extrait les lignes de texte du document en ignorant l'en-tete

        L'en-tete du DOCX latin_analyzer contient :
        - Un titre ("Analyse de texte latin medieval")
        - Une legende (Noir = ..., Orange = ..., Rouge = ...)
        - Un separateur (ligne de underscores)

        Args:
            doc: Document python-docx

        Returns:
            Liste des lignes de texte (sans l'en-tete)
        """
        lines = []
        header_passed = False

        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()

            if not text:
                continue

            # Tant que l'en-tete n'est pas passe, on cherche le separateur
            if not header_passed:
                if self._is_header_content(text):
                    continue
                if SEPARATOR_PATTERN.match(text):
                    header_passed = True
                    continue
                # Si on ne reconnait pas de marqueur d'en-tete et pas de
                # separateur, c'est peut-etre un docx sans en-tete standard.
                # On considere que le texte commence directement.
                header_passed = True

            # Texte normal apres l'en-tete
            if header_passed and text:
                lines.append(text)

        return lines

    @staticmethod
    def _is_header_content(text: str) -> bool:
        """
        Verifie si le texte fait partie de l'en-tete latin_analyzer

        Args:
            text: Texte du paragraphe

        Returns:
            True si c'est du contenu d'en-tete
        """
        for marker in HEADER_MARKERS:
            if marker in text:
                return True
        return False
