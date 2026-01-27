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
"""

import os
import re
import argparse
import requests
import xml.etree.ElementTree as ET
from os.path import join, dirname, realpath, basename
from tqdm import tqdm


# === CONFIGURATION ===
API_KEY = 'aae99aba-476e-4ff2-2886-0aaf1bfa6fd2'
BASE_URL_PROD = 'https://api.nakala.fr'
BASE_URL_TEST = 'https://apitest.nakala.fr'
NAKALA_URL_PROD = 'https://nakala.fr'
NAKALA_URL_TEST = 'https://test.nakala.fr'


def get_api_urls(test=False):
    """Retourne les URLs API et front selon l'environnement"""
    if test:
        return BASE_URL_TEST, NAKALA_URL_TEST
    return BASE_URL_PROD, NAKALA_URL_PROD


def parse_hera_xml(xml_path):
    """Parse le fichier XML heimdall pour extraire les DOI, titres et chemins des verticaux"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    items = []
    
    for item in root.findall('.//item[@eid="item"]'):
        doi = None
        title = None
        files = []
        vertical_path = None
        
        for metadata in item.findall('metadata'):
            pid = metadata.get('pid')
            value = metadata.text
            
            if pid == 'identifier' and metadata.get('aid') == 'doi':
                doi = value
            elif pid == 'title':
                title = value
            elif pid == 'file':
                files.append(value)
                # Récupérer le chemin du fichier vertical
                if value and value.endswith('vertical.txt'):
                    vertical_path = value
        
        if doi and title:
            items.append({
                'doi': doi,
                'title': title,
                'files': files,
                'vertical_path': vertical_path
            })
    
    print(f"📚 {len(items)} items trouvés dans le XML")
    return items


def get_doi_files_hashes(doi, api_key, api_url):
    """Récupère les hash SHA1 des fichiers pour un DOI donné"""
    headers = {'X-API-KEY': api_key}
    response = requests.get(f'{api_url}/datas/{doi}', headers=headers)
    response.raise_for_status()
    data = response.json()
    
    files = {}
    for f in data.get('files', []):
        name = f.get('name', '')
        sha1 = f.get('sha1', '')
        if name and sha1:
            files[name] = sha1
    
    return files


def extract_page_number(filename):
    """Extrait le numéro de page d'un nom de fichier (ex: page_0158_xxx.txt → 158)"""
    match = re.match(r'page_(\d+)', basename(filename))
    if match:
        return int(match.group(1))
    return None


def build_page_url_mapping(items, api_key, api_url, nakala_url):
    """Construit un mapping (source, page_number) → URL Nakala pour les pages et les fiches"""
    page_mapping = {}
    fiche_mapping = {}
    
    print("\n📦 Récupération des hash depuis l'API Nakala...")
    
    for item in tqdm(items, desc="DOI traités"):
        doi = item['doi']
        title = item['title']
        
        try:
            file_hashes = get_doi_files_hashes(doi, api_key, api_url)
        except Exception as e:
            print(f"\n  ⚠️  Erreur pour {doi}: {e}")
            continue
        
        for filename, sha1 in file_hashes.items():
            # Mapping des pages
            page_num = extract_page_number(filename)
            if page_num is not None:
                url = f"{nakala_url}/{doi}#{sha1}"
                key = (title, page_num)
                page_mapping[key] = url
            
            # Mapping des fiches
            if filename == 'fiche.pdf':
                url = f"{nakala_url}/{doi}#{sha1}"
                fiche_mapping[title] = url
    
    print(f"\n🔗 {len(page_mapping)} liens page → URL construits")
    print(f"📋 {len(fiche_mapping)} liens fiche → URL construits")
    return page_mapping, fiche_mapping


def add_links_to_vertical(vertical_path, page_mapping, fiche_mapping, dry_run=False):
    """Ajoute les attributs link et fiche dans un fichier vertical"""
    
    with open(vertical_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    lines_modified = 0
    
    def replace_doc(match):
        nonlocal modified, lines_modified
        
        full_tag = match.group(0)
        new_tag = full_tag
        tag_modified = False
        
        # Extraire title et page_number
        title_match = re.search(r'title="([^"]*)"', full_tag)
        page_match = re.search(r'page_number="(\d+)"', full_tag)

        if not title_match:
            return full_tag

        title = title_match.group(1)

        # Ajouter link (page) si absent
        if 'link=' not in new_tag and page_match:
            page_num = int(page_match.group(1))
            key = (title, page_num)
            if key in page_mapping:
                url = page_mapping[key]
                new_tag = new_tag.replace('<doc ', f'<doc link="{url}" ', 1)
                tag_modified = True

        # Ajouter fiche si absent
        if 'fiche=' not in new_tag and title in fiche_mapping:
            url = fiche_mapping[title]
            new_tag = new_tag.replace('<doc ', f'<doc fiche="{url}" ', 1)
            tag_modified = True
        
        if tag_modified:
            modified = True
            lines_modified += 1
        
        return new_tag
    
    # Remplacer toutes les balises <doc ...>
    new_content = re.sub(r'<doc [^>]+>', replace_doc, content)
    
    if modified:
        if dry_run:
            print(f"  [DRY-RUN] {vertical_path}: {lines_modified} <doc> modifiés")
        else:
            with open(vertical_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ {vertical_path}: {lines_modified} <doc> modifiés")
    else:
        print(f"  ⏭️  {vertical_path}: aucune modification")
    
    return lines_modified


def process_vertical_files(items, page_mapping, fiche_mapping, dry_run=False):
    """Traite les fichiers vertical.txt dont les chemins sont extraits du XML"""
    total_modified = 0
    
    for item in items:
        vertical_path = item.get('vertical_path')
        
        if not vertical_path or not os.path.isfile(vertical_path):
            continue
        
        total_modified += add_links_to_vertical(vertical_path, page_mapping, fiche_mapping, dry_run)
    
    return total_modified


def main():
    parser = argparse.ArgumentParser(description='Enrichir les fichiers vertical avec les URLs Nakala')
    parser.add_argument('xml_file', type=str, help='Fichier XML généré par heimdall (cisame.xml)')
    parser.add_argument('--test', action='store_true', help='Utiliser l\'API de test')
    parser.add_argument('--dry-run', action='store_true', help='Afficher sans modifier')
    args = parser.parse_args()
    
    # Configuration
    api_url, nakala_url = get_api_urls(args.test)
    
    print(f"\n{'='*60}")
    print(f"🔧 Enrichissement des fichiers vertical avec liens Nakala")
    print(f"{'='*60}")
    print(f"📄 Fichier XML: {args.xml_file}")
    print(f"🌐 API: {api_url}")
    print(f"🔗 URLs Nakala: {nakala_url}")
    if args.dry_run:
        print(f"⚠️  Mode DRY-RUN: aucune modification ne sera écrite")
    print()
    
    # Étape 1: Parser le XML
    print("📖 Étape 1/3: Lecture du fichier XML...")
    items = parse_hera_xml(args.xml_file)
    
    if not items:
        print("❌ Aucun item trouvé dans le XML")
        return
    
    # Afficher les chemins des verticaux trouvés
    vertical_count = sum(1 for item in items if item.get('vertical_path'))
    print(f"📁 {vertical_count} fichiers vertical.txt trouvés dans le XML")
    
    # Étape 2: Construire le mapping avec les hash de l'API
    print("\n🔗 Étape 2/3: Construction du mapping...")
    page_mapping, fiche_mapping = build_page_url_mapping(items, API_KEY, api_url, nakala_url)
    
    if not page_mapping and not fiche_mapping:
        print("❌ Aucun mapping trouvé. Vérifiez les données.")
        return
    
    # Étape 3: Modifier les fichiers vertical
    print(f"\n📝 Étape 3/3: Traitement des fichiers vertical.txt...")
    total = process_vertical_files(items, page_mapping, fiche_mapping, args.dry_run)
    
    print(f"\n{'='*60}")
    print(f"✅ Terminé: {total} balises <doc> enrichies avec des liens Nakala")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
