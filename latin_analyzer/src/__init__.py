"""
Analyseur de textes latins médiévaux - Version 2.4.0

Package pour l'analyse automatique de textes latins médiévaux avec :
- PyCollatinus (latin classique, optionnel)
- Dictionnaire Du Cange (latin médiéval)
- Système de scoring multi-critères
- Colorisation à 3 niveaux (rouge/orange/noir)
- Support XML Pages (extraction MainZone)
- Préservation des pages/folios dans le DOCX

Auteur: CiSaMe
Version: 2.4.0
"""

from .latin_analyzer_v2 import LatinAnalyzer
from .page_xml_parser import PageXMLParser

__version__ = "2.4.0"
__all__ = ["LatinAnalyzer", "PageXMLParser"]
