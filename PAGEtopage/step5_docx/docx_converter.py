"""
Convertisseur DOCX vers format vertical

Orchestre le parsing du DOCX et l'enrichissement linguistique
pour produire un fichier au format vertical.
"""

from pathlib import Path
from typing import List, Optional
import logging

from ..config import Config
from ..models import ExtractedPage, AnnotatedPage
from ..step2_enrich.processor import EnrichmentProcessor
from .docx_parser import DocxParser

logger = logging.getLogger(__name__)


class DocxConverter:
    """
    Convertit les fichiers DOCX (issus de latin_analyzer) en format vertical

    Workflow:
        1. Parse le(s) fichier(s) DOCX pour extraire le texte brut
        2. Injecte les metadonnees depuis le config.yaml
        3. Tokenise et lemmatise avec TreeTagger (via EnrichmentProcessor)
        4. Genere le fichier vertical

    Usage:
        config = Config.from_yaml("config.yaml")
        converter = DocxConverter(config)

        # Depuis un fichier DOCX
        pages = converter.convert_file("resultat.docx", "corpus.vertical.txt")

        # Depuis un dossier de fichiers DOCX
        pages = converter.convert_folder("./docx/", "corpus.vertical.txt")
    """

    def __init__(self, config: Config):
        """
        Args:
            config: Configuration du pipeline
        """
        self.config = config
        self.parser = DocxParser(config)
        self.processor = EnrichmentProcessor(config)

        self._converted_count = 0
        self._error_count = 0

    def convert_file(
        self,
        input_path: str | Path,
        output_path: str | Path,
    ) -> List[AnnotatedPage]:
        """
        Convertit un fichier DOCX en format vertical

        Args:
            input_path: Chemin vers le fichier DOCX
            output_path: Chemin de sortie du fichier vertical

        Returns:
            Liste de AnnotatedPage
        """
        logger.info(f"Conversion DOCX -> vertical: {input_path}")

        # 1. Parse le DOCX
        extracted_pages = self.parser.parse_file(input_path)

        if not extracted_pages:
            logger.error("Aucune page extraite du DOCX")
            return []

        # 2. Enrichit (tokenisation + lemmatisation)
        annotated_pages = self._enrich_pages(extracted_pages)

        # 3. Sauvegarde en format vertical
        self.processor.save_vertical(annotated_pages, output_path)

        return annotated_pages

    def convert_folder(
        self,
        input_path: str | Path,
        output_path: str | Path,
        pattern: str = "*.docx",
    ) -> List[AnnotatedPage]:
        """
        Convertit tous les fichiers DOCX d'un dossier en format vertical

        Args:
            input_path: Dossier contenant les fichiers DOCX
            output_path: Chemin de sortie du fichier vertical
            pattern: Pattern glob pour les fichiers

        Returns:
            Liste de AnnotatedPage
        """
        logger.info(f"Conversion dossier DOCX -> vertical: {input_path}")

        # 1. Parse tous les DOCX
        extracted_pages = self.parser.parse_folder(input_path, pattern)

        if not extracted_pages:
            logger.error("Aucune page extraite des fichiers DOCX")
            return []

        # 2. Enrichit
        annotated_pages = self._enrich_pages(extracted_pages)

        # 3. Sauvegarde
        self.processor.save_vertical(annotated_pages, output_path)

        return annotated_pages

    def convert_and_save(
        self,
        input_path: str | Path,
        output_path: str | Path,
        pattern: str = "*.docx",
    ) -> List[AnnotatedPage]:
        """
        Point d'entree unifie : detecte fichier ou dossier

        Args:
            input_path: Fichier DOCX ou dossier
            output_path: Chemin de sortie vertical
            pattern: Pattern glob si dossier

        Returns:
            Liste de AnnotatedPage
        """
        input_path = Path(input_path)

        if input_path.is_file():
            return self.convert_file(input_path, output_path)
        else:
            return self.convert_folder(input_path, output_path, pattern)

    def _enrich_pages(
        self,
        pages: List[ExtractedPage],
    ) -> List[AnnotatedPage]:
        """
        Enrichit les pages extraites via le processeur standard

        Args:
            pages: Liste de ExtractedPage

        Returns:
            Liste de AnnotatedPage
        """
        annotated_pages = []

        for page in pages:
            try:
                annotated = self.processor.process_page(page)
                annotated_pages.append(annotated)
                self._converted_count += 1
            except Exception as e:
                logger.error(f"Erreur sur la page {page.metadata.folio}: {e}")
                self._error_count += 1

        logger.info(
            f"Enrichissement termine: {len(annotated_pages)} pages, "
            f"{self._error_count} erreurs"
        )

        return annotated_pages

    @property
    def converted_count(self) -> int:
        """Nombre de pages converties"""
        return self._converted_count

    @property
    def error_count(self) -> int:
        """Nombre d'erreurs"""
        return self._error_count

    def reset_stats(self) -> None:
        """Reinitialise les statistiques"""
        self._converted_count = 0
        self._error_count = 0


def convert_docx_to_vertical(
    input_path: str | Path,
    output_path: str | Path,
    config: Optional[Config] = None,
    pattern: str = "*.docx",
) -> List[AnnotatedPage]:
    """
    Fonction utilitaire pour convertir un DOCX en format vertical

    Args:
        input_path: Fichier DOCX ou dossier
        output_path: Chemin de sortie vertical
        config: Configuration optionnelle
        pattern: Pattern glob si dossier

    Returns:
        Liste de pages annotees

    Example:
        >>> from PAGEtopage.step5_docx import convert_docx_to_vertical
        >>> from PAGEtopage.config import Config
        >>>
        >>> config = Config.from_yaml("config.yaml")
        >>> pages = convert_docx_to_vertical(
        ...     "resultat_latin_analyzer.docx",
        ...     "corpus.vertical.txt",
        ...     config
        ... )
    """
    if config is None:
        config = Config()

    converter = DocxConverter(config)
    return converter.convert_and_save(input_path, output_path, pattern)
