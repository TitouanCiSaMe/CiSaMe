"""
Parseur de fichiers DOCX produits par latin_analyzer

Extrait le texte brut depuis les fichiers DOCX colores generes par
latin_analyzer, en ignorant l'en-tete (titre, legende, separateur).

Supporte les DOCX multi-pages avec en-tetes de page/folio
(format: ──── Folio: X | Page: Y | Titre ────).
"""

import re
from pathlib import Path
from typing import List, Optional, Dict
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

# En-tete de page/folio insere par latin_analyzer v2.4+
# Format: ──── Folio: filename | Page: N | running_title ────
PAGE_HEADER_PATTERN = re.compile(r'^─{2,}\s+(.+?)\s+─{2,}$')

# Sous-patterns pour extraire folio, page, titre depuis le contenu de l'en-tete
_FOLIO_PATTERN = re.compile(r'Folio:\s*([^|]+)')
_PAGE_PATTERN = re.compile(r'Page:\s*(\d+)')


def _parse_page_header(text: str) -> Optional[dict]:
    """
    Parse un en-tete de page/folio et retourne les metadonnees.

    Args:
        text: Texte du paragraphe

    Returns:
        Dict {folio, page_number, running_title} ou None si pas un en-tete
    """
    m = PAGE_HEADER_PATTERN.match(text)
    if not m:
        return None

    inner = m.group(1)
    parts = [p.strip() for p in inner.split("|")]

    folio = None
    page_number = None
    title_parts = []

    for part in parts:
        folio_m = _FOLIO_PATTERN.match(part)
        page_m = _PAGE_PATTERN.match(part)
        if folio_m:
            folio = folio_m.group(1).strip()
        elif page_m:
            page_number = int(page_m.group(1))
        elif part:
            title_parts.append(part)

    return {
        "folio": folio,
        "page_number": page_number,
        "running_title": " ".join(title_parts) if title_parts else None,
    }


class DocxParser:
    """
    Parse les fichiers DOCX issus de latin_analyzer

    Extrait le texte en ignorant l'en-tete de validation (titre, legende,
    separateur) et cree des ExtractedPage avec les metadonnees du config.yaml.

    Supporte les DOCX contenant plusieurs pages/folios (latin_analyzer v2.4+)
    grace aux en-tetes de page inseres dans le document.

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

        Si le DOCX contient des en-tetes de page (latin_analyzer v2.4+),
        chaque section devient une ExtractedPage separee.
        Sinon, le fichier entier produit une seule ExtractedPage.

        Args:
            file_path: Chemin vers le fichier DOCX

        Returns:
            Liste de ExtractedPage
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Fichier non trouve: {file_path}")

        logger.info(f"Parsing du fichier DOCX: {file_path.name}")

        doc = Document(str(file_path))
        sections = self._extract_page_sections(doc)

        if not sections:
            logger.warning(f"Aucun texte extrait de {file_path.name}")
            return []

        pages = []
        for i, section in enumerate(sections, start=1):
            folio = section.get("folio") or file_path.stem
            page_num = section.get("page_number") or i
            running_title = (
                section.get("running_title")
                or self.config.corpus.title
                or "No running title"
            )

            metadata = PageMetadata(
                folio=folio,
                page_number=page_num,
                running_title=running_title,
                corpus_metadata=self.config.corpus.to_dict(),
            )

            pages.append(ExtractedPage(
                metadata=metadata,
                lines=section["lines"],
            ))

        logger.info(f"  {len(pages)} page(s), {sum(len(s['lines']) for s in sections)} lignes")
        return pages

    def parse_folder(
        self,
        folder_path: str | Path,
        pattern: str = "*.docx"
    ) -> List[ExtractedPage]:
        """
        Parse tous les fichiers DOCX d'un dossier

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
        page_counter = 1
        for file_path in files:
            try:
                pages = self.parse_file(file_path)
                for page in pages:
                    page.metadata.page_number = page_counter
                    page_counter += 1
                all_pages.extend(pages)
            except Exception as e:
                logger.error(f"Erreur lors du parsing de {file_path}: {e}")

        logger.info(f"Total: {len(all_pages)} pages extraites depuis {len(files)} fichiers")
        return all_pages

    def _extract_page_sections(self, doc: Document) -> List[Dict]:
        """
        Extrait les sections de texte du document, en gerant les en-tetes
        de page/folio et en ignorant l'en-tete latin_analyzer.

        Chaque section est un dict avec:
            - lines: Liste des lignes de texte
            - folio: Nom du folio (ou None)
            - page_number: Numero de page (ou None)
            - running_title: Titre courant (ou None)

        Args:
            doc: Document python-docx

        Returns:
            Liste de sections (au moins une si du texte existe)
        """
        header_passed = False
        sections = []
        current_section = {
            "lines": [],
            "folio": None,
            "page_number": None,
            "running_title": None,
        }

        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()

            if not text:
                continue

            # Phase 1: ignorer l'en-tete latin_analyzer
            if not header_passed:
                if self._is_header_content(text):
                    continue
                if SEPARATOR_PATTERN.match(text):
                    header_passed = True
                    continue
                # Pas d'en-tete reconnu => le texte commence directement
                header_passed = True

            # Phase 2: detecter les en-tetes de page/folio
            page_info = _parse_page_header(text)
            if page_info is not None:
                # Sauvegarder la section precedente si elle a du texte
                if current_section["lines"]:
                    sections.append(current_section)

                current_section = {
                    "lines": [],
                    "folio": page_info["folio"],
                    "page_number": page_info["page_number"],
                    "running_title": page_info["running_title"],
                }
                continue

            # Phase 3: texte normal
            if header_passed and text:
                current_section["lines"].append(text)

        # Derniere section
        if current_section["lines"]:
            sections.append(current_section)

        return sections

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
