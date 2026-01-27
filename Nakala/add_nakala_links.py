#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour enrichir les fichiers vertical.txt avec les URLs Nakala.
Utilise le fichier cisame.xml généré par heimdall pour récupérer les DOI
et les chemins des fichiers vertical.txt, puis interroge l'API Nakala
pour obtenir les hash des fichiers.

Ajoute deux attributs dans les balises <doc> :
- link : lien vers la page sur Nakala (icône image)
- fiche : lien vers la fiche.docx sur Nakala (icône audio)

Usage:
    ./add_nakala_links.py cisame.xml [--test] [--dry-run]

Options:
    cisame.xml  Fichier XML généré par heimdall après l'upload
    --test      Utilise l'API de test (apitest.nakala.fr) au lieu de la prod
    --dry-run   Affiche les modifications sans écrire les fichiers

Variables d'environnement:
    NAKALA_API_KEY  Clé API Nakala (obligatoire)
"""

import os
import re
import sys
import logging
import argparse
from os.path import basename
from xml.sax.saxutils import quoteattr

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    import defusedxml.ElementTree as ET
except ImportError:
    logging.warning(
        "Le module 'defusedxml' n'est pas installé. "
        "Utilisation de xml.etree.ElementTree (moins sécurisé). "
        "Installez defusedxml : pip install defusedxml"
    )
    import xml.etree.ElementTree as ET

from tqdm import tqdm


# === CONFIGURATION ===
BASE_URL_PROD = 'https://api.nakala.fr'
BASE_URL_TEST = 'https://apitest.nakala.fr'
NAKALA_URL_PROD = 'https://nakala.fr'
NAKALA_URL_TEST = 'https://test.nakala.fr'

# Constantes
FICHE_FILENAME = 'fiche.pdf'
VERTICAL_FILENAME = 'vertical.txt'
HTTP_TIMEOUT = 30  # secondes
HTTP_RETRIES = 3
HTTP_BACKOFF_FACTOR = 0.5

# Regex pré-compilées
DOC_TAG_PATTERN = re.compile(r'<doc [^>]+>')
PAGE_NUM_PATTERN = re.compile(r'page_(\d+)')
PAGE_NUM_ATTR_PATTERN = re.compile(r'page_number="(\d+)"')

# Logger
logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure le logging avec le niveau approprié."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s',
        stream=sys.stderr
    )


def create_http_session(api_key):
    """Crée une session HTTP avec retry automatique et timeout."""
    session = requests.Session()
    retry_strategy = Retry(
        total=HTTP_RETRIES,
        backoff_factor=HTTP_BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('https://', adapter)
    session.headers.update({'X-API-KEY': api_key})
    return session


def get_api_urls(test=False):
    """Retourne les URLs API et front selon l'environnement."""
    if test:
        return BASE_URL_TEST, NAKALA_URL_TEST
    return BASE_URL_PROD, NAKALA_URL_PROD


def parse_hera_xml(xml_path):
    """Parse le fichier XML heimdall pour extraire les DOI, titres et chemins des verticaux.

    Args:
        xml_path: Chemin vers le fichier XML cisame.xml.

    Returns:
        Liste de dicts avec les clés: doi, title, files, vertical_path.
    """
    if not os.path.isfile(xml_path):
        logger.error("Fichier XML introuvable : %s", xml_path)
        return []

    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as e:
        logger.error("Erreur de parsing XML dans %s : %s", xml_path, e)
        return []

    root = tree.getroot()

    items = []
    titles_seen = {}

    for item in root.findall('.//item[@eid="item"]'):
        doi = None
        title = None
        files = []
        vertical_path = None

        for metadata in item.findall('metadata'):
            pid = metadata.get('pid')
            value = metadata.text

            if value is None:
                continue

            if pid == 'identifier' and metadata.get('aid') == 'doi':
                doi = value.strip()
            elif pid == 'title':
                title = value.strip()
            elif pid == 'file':
                files.append(value)
                if value.endswith(VERTICAL_FILENAME):
                    vertical_path = value

        if doi and title:
            # Détection de collisions de titres
            if title in titles_seen:
                logger.warning(
                    "Titre en double détecté : '%s' (DOI: %s et %s). "
                    "Le second écrasera le premier dans le mapping.",
                    title, titles_seen[title], doi
                )
            titles_seen[title] = doi

            # Validation du chemin vertical
            if vertical_path:
                vertical_path = os.path.normpath(vertical_path)

            items.append({
                'doi': doi,
                'title': title,
                'files': files,
                'vertical_path': vertical_path
            })
        else:
            logger.debug(
                "Item ignoré (doi=%s, title=%s)", doi, title
            )

    logger.info("%d items trouvés dans le XML", len(items))
    return items


def get_doi_files_hashes(doi, session, api_url):
    """Récupère les hash SHA1 des fichiers pour un DOI donné.

    Args:
        doi: Identifiant DOI Nakala.
        session: Session requests configurée.
        api_url: URL de base de l'API Nakala.

    Returns:
        Dict {nom_fichier: sha1}.

    Raises:
        requests.RequestException: En cas d'erreur réseau/API.
    """
    url = f'{api_url}/datas/{doi}'
    response = session.get(url, timeout=HTTP_TIMEOUT)
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError as e:
        logger.error("Réponse JSON invalide pour DOI %s : %s", doi, e)
        return {}

    files = {}
    for f in data.get('files', []):
        name = f.get('name', '')
        sha1 = f.get('sha1', '')
        if name and sha1:
            files[name] = sha1

    return files


def extract_page_number(filename):
    """Extrait le numéro de page d'un nom de fichier (ex: page_0158_xxx.txt -> 158).

    Args:
        filename: Nom ou chemin du fichier.

    Returns:
        Numéro de page (int) ou None si non trouvé.
    """
    match = PAGE_NUM_PATTERN.match(basename(filename))
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            logger.warning("Numéro de page invalide dans : %s", filename)
            return None
    return None


def build_page_url_mapping(items, session, api_url, nakala_url):
    """Construit un mapping (title, page_number) -> URL Nakala pour les pages et les fiches.

    Args:
        items: Liste d'items parsés depuis le XML.
        session: Session HTTP configurée.
        api_url: URL de base API Nakala.
        nakala_url: URL de base front Nakala.

    Returns:
        Tuple (page_mapping, fiche_mapping, stats) où stats contient les compteurs.
    """
    page_mapping = {}
    fiche_mapping = {}
    api_successes = 0
    api_failures = 0

    logger.info("Récupération des hash depuis l'API Nakala...")

    for item in tqdm(items, desc="DOI traités"):
        doi = item['doi']
        title = item['title']

        try:
            file_hashes = get_doi_files_hashes(doi, session, api_url)
            api_successes += 1
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 'N/A'
            if status in (401, 403):
                logger.error(
                    "Erreur d'authentification pour DOI %s (HTTP %s). "
                    "Vérifiez votre clé API.", doi, status
                )
            else:
                logger.warning("Erreur HTTP pour DOI %s (HTTP %s) : %s", doi, status, e)
            api_failures += 1
            continue
        except requests.exceptions.ConnectionError as e:
            logger.warning("Erreur de connexion pour DOI %s : %s", doi, e)
            api_failures += 1
            continue
        except requests.exceptions.Timeout:
            logger.warning("Timeout pour DOI %s (>%ds)", doi, HTTP_TIMEOUT)
            api_failures += 1
            continue
        except requests.exceptions.RequestException as e:
            logger.warning("Erreur réseau pour DOI %s : %s", doi, e)
            api_failures += 1
            continue

        for filename, sha1 in file_hashes.items():
            page_num = extract_page_number(filename)
            if page_num is not None:
                url = f"{nakala_url}/{doi}#{sha1}"
                key = (title, page_num)
                page_mapping[key] = url

            if filename == FICHE_FILENAME:
                url = f"{nakala_url}/{doi}#{sha1}"
                fiche_mapping[title] = url

    stats = {
        'api_successes': api_successes,
        'api_failures': api_failures,
        'page_links': len(page_mapping),
        'fiche_links': len(fiche_mapping),
    }

    logger.info("%d liens page -> URL construits", len(page_mapping))
    logger.info("%d liens fiche -> URL construits", len(fiche_mapping))
    if api_failures:
        logger.warning("%d appels API ont échoué", api_failures)

    return page_mapping, fiche_mapping, stats


def escape_url_for_attr(url):
    """Échappe une URL pour insertion dans un attribut XML.

    Utilise quoteattr qui gère les caractères &, <, >, " et '.

    Args:
        url: URL à échapper.

    Returns:
        URL échappée avec guillemets (ex: '"https://..."').
    """
    return quoteattr(url)


def add_links_to_vertical(vertical_path, xml_title, page_mapping, fiche_mapping, dry_run=False):
    """Ajoute les attributs link et fiche dans un fichier vertical.

    Args:
        vertical_path: Chemin vers le fichier vertical.txt.
        xml_title: Titre de l'item dans le XML (clé de matching).
        page_mapping: Dict (title, page_num) -> URL.
        fiche_mapping: Dict title -> URL fiche.
        dry_run: Si True, n'écrit pas les modifications.

    Returns:
        Nombre de balises <doc> modifiées.
    """
    try:
        with open(vertical_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, OSError) as e:
        logger.error("Impossible de lire %s : %s", vertical_path, e)
        return 0
    except UnicodeDecodeError as e:
        logger.error("Erreur d'encodage dans %s : %s", vertical_path, e)
        return 0

    lines_modified = 0

    def replace_doc(match):
        nonlocal lines_modified

        full_tag = match.group(0)
        new_tag = full_tag
        tag_modified = False

        # Extraire page_number
        page_match = PAGE_NUM_ATTR_PATTERN.search(full_tag)

        # Ajouter link (page) si absent
        if 'link=' not in new_tag and page_match:
            try:
                page_num = int(page_match.group(1))
            except ValueError:
                logger.warning(
                    "page_number invalide dans %s : %s",
                    vertical_path, page_match.group(1)
                )
                return new_tag

            key = (xml_title, page_num)
            if key in page_mapping:
                url = page_mapping[key]
                safe_url = escape_url_for_attr(url)
                new_tag = new_tag.replace('<doc ', f'<doc link={safe_url} ', 1)
                tag_modified = True

        # Ajouter fiche si absent
        if 'fiche=' not in new_tag and xml_title in fiche_mapping:
            url = fiche_mapping[xml_title]
            safe_url = escape_url_for_attr(url)
            new_tag = new_tag.replace('<doc ', f'<doc fiche={safe_url} ', 1)
            tag_modified = True

        if tag_modified:
            lines_modified += 1

        return new_tag

    new_content = DOC_TAG_PATTERN.sub(replace_doc, content)

    if lines_modified > 0:
        if dry_run:
            logger.info("[DRY-RUN] %s : %d <doc> modifiés", vertical_path, lines_modified)
        else:
            try:
                with open(vertical_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logger.info("%s : %d <doc> modifiés", vertical_path, lines_modified)
            except (IOError, OSError) as e:
                logger.error("Impossible d'écrire %s : %s", vertical_path, e)
                return 0
    else:
        logger.debug("%s : aucune modification", vertical_path)

    return lines_modified


def process_vertical_files(items, page_mapping, fiche_mapping, dry_run=False):
    """Traite les fichiers vertical.txt dont les chemins sont extraits du XML.

    Args:
        items: Liste d'items parsés depuis le XML.
        page_mapping: Dict (title, page_num) -> URL.
        fiche_mapping: Dict title -> URL fiche.
        dry_run: Si True, n'écrit pas les modifications.

    Returns:
        Dict avec les statistiques de traitement.
    """
    total_modified = 0
    files_processed = 0
    files_skipped = 0

    for item in items:
        vertical_path = item.get('vertical_path')
        xml_title = item.get('title')

        if not vertical_path:
            logger.warning(
                "Pas de fichier vertical.txt pour l'item '%s' (DOI: %s)",
                xml_title, item.get('doi')
            )
            files_skipped += 1
            continue

        if not os.path.isfile(vertical_path):
            logger.warning(
                "Fichier vertical introuvable : %s (item: '%s')",
                vertical_path, xml_title
            )
            files_skipped += 1
            continue

        modified = add_links_to_vertical(
            vertical_path, xml_title, page_mapping, fiche_mapping, dry_run
        )
        total_modified += modified
        files_processed += 1

    return {
        'total_modified': total_modified,
        'files_processed': files_processed,
        'files_skipped': files_skipped,
    }


def print_summary(items_count, vertical_count, api_stats, file_stats, dry_run=False):
    """Affiche un rapport de synthèse en fin d'exécution."""
    sep = '=' * 60
    logger.info("")
    logger.info(sep)
    logger.info("RAPPORT DE SYNTHESE")
    logger.info(sep)
    logger.info("Items dans le XML           : %d", items_count)
    logger.info("Fichiers vertical trouvés   : %d", vertical_count)
    logger.info("Appels API réussis          : %d", api_stats.get('api_successes', 0))
    logger.info("Appels API échoués          : %d", api_stats.get('api_failures', 0))
    logger.info("Liens page construits       : %d", api_stats.get('page_links', 0))
    logger.info("Liens fiche construits      : %d", api_stats.get('fiche_links', 0))
    logger.info("Fichiers traités            : %d", file_stats.get('files_processed', 0))
    logger.info("Fichiers ignorés            : %d", file_stats.get('files_skipped', 0))
    logger.info("Balises <doc> enrichies     : %d", file_stats.get('total_modified', 0))
    if dry_run:
        logger.info("Mode                        : DRY-RUN (aucune écriture)")
    logger.info(sep)


def main():
    parser = argparse.ArgumentParser(
        description='Enrichir les fichiers vertical avec les URLs Nakala'
    )
    parser.add_argument(
        'xml_file', type=str,
        help='Fichier XML généré par heimdall (cisame.xml)'
    )
    parser.add_argument(
        '--test', action='store_true',
        help="Utiliser l'API de test"
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Afficher sans modifier'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Activer les logs de debug'
    )
    args = parser.parse_args()

    # Logging
    setup_logging(verbose=args.verbose)

    # Clé API depuis variable d'environnement
    api_key = os.environ.get('NAKALA_API_KEY')
    if not api_key:
        logger.error(
            "Variable d'environnement NAKALA_API_KEY non définie. "
            "Définissez-la avec : export NAKALA_API_KEY='votre-clé'"
        )
        sys.exit(1)

    # Validation du fichier XML
    if not os.path.isfile(args.xml_file):
        logger.error("Fichier XML introuvable : %s", args.xml_file)
        sys.exit(1)

    # Configuration
    api_url, nakala_url = get_api_urls(args.test)

    logger.info("Enrichissement des fichiers vertical avec liens Nakala")
    logger.info("Fichier XML : %s", args.xml_file)
    logger.info("API : %s", api_url)
    logger.info("URLs Nakala : %s", nakala_url)
    if args.dry_run:
        logger.info("Mode DRY-RUN : aucune modification ne sera écrite")

    # Session HTTP avec retry
    session = create_http_session(api_key)

    # Étape 1: Parser le XML
    logger.info("Etape 1/3 : Lecture du fichier XML...")
    items = parse_hera_xml(args.xml_file)

    if not items:
        logger.error("Aucun item trouvé dans le XML")
        sys.exit(1)

    vertical_count = sum(1 for item in items if item.get('vertical_path'))
    logger.info("%d fichiers vertical.txt trouvés dans le XML", vertical_count)

    # Étape 2: Construire le mapping avec les hash de l'API
    logger.info("Etape 2/3 : Construction du mapping...")
    page_mapping, fiche_mapping, api_stats = build_page_url_mapping(
        items, session, api_url, nakala_url
    )

    if not page_mapping and not fiche_mapping:
        logger.error("Aucun mapping trouvé. Vérifiez les données.")
        sys.exit(1)

    # Étape 3: Modifier les fichiers vertical
    logger.info("Etape 3/3 : Traitement des fichiers vertical.txt...")
    file_stats = process_vertical_files(
        items, page_mapping, fiche_mapping, args.dry_run
    )

    # Rapport de synthèse
    print_summary(len(items), vertical_count, api_stats, file_stats, args.dry_run)


if __name__ == '__main__':
    main()
