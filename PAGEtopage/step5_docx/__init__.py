"""
Etape 5 : Conversion DOCX vers format vertical

Permet de convertir les fichiers DOCX produits par latin_analyzer
en format vertical enrichi (lemmatisation + POS tagging).

Le texte est extrait du DOCX, les metadonnees proviennent du config.yaml,
et l'enrichissement est realise par le processeur standard (TreeTagger).
"""

from .docx_converter import DocxConverter
from .docx_parser import DocxParser

__all__ = ['DocxConverter', 'DocxParser']
