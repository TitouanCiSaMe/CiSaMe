"""
Tests unitaires pour add_nakala_links.py

Couvre : parsing XML, extraction page_number, ajout de liens dans les
balises <doc>, traitement des fichiers vertical, et fusion des verticaux
modifiés en un fichier unique.
"""

import os
import sys
import tempfile
import shutil
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ajouter le dossier parent au path pour l'import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from add_nakala_links import (
    parse_hera_xml,
    extract_page_number,
    escape_url_for_attr,
    add_links_to_vertical,
    process_vertical_files,
    create_merged_vertical,
    get_api_urls,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ── Helpers ──────────────────────────────────────────────────────────

def create_sample_xml(tmp_dir, vertical_paths):
    """Crée un fichier cisame.xml de test avec les chemins vertical dynamiques."""
    template = (FIXTURES_DIR / "sample_cisame.xml").read_text(encoding="utf-8")
    content = template.replace("{vertical_path_1}", vertical_paths[0])
    content = content.replace("{vertical_path_2}", vertical_paths[1])
    xml_path = os.path.join(tmp_dir, "cisame.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(content)
    return xml_path


def copy_vertical(fixture_name, dest_path):
    """Copie un fichier vertical fixture vers un chemin de destination."""
    src = FIXTURES_DIR / fixture_name
    shutil.copy2(src, dest_path)
    return dest_path


# ── Tests parse_hera_xml ─────────────────────────────────────────────

class TestParseHeraXml:
    """Tests pour le parsing du fichier XML cisame."""

    def test_parse_valid_xml(self, tmp_path):
        """Test parsing d'un XML valide avec 2 items."""
        v1 = str(tmp_path / "vertical1.txt")
        v2 = str(tmp_path / "vertical2.txt")
        copy_vertical("sample_vertical_1.txt", v1)
        copy_vertical("sample_vertical_2.txt", v2)

        xml_path = create_sample_xml(str(tmp_path), [v1, v2])
        items = parse_hera_xml(xml_path)

        assert len(items) == 2
        assert items[0]["doi"] == "10.34847/nkl.abc123"
        assert items[0]["title"] == "Brachylogus"
        assert items[1]["doi"] == "10.34847/nkl.def456"
        assert items[1]["title"] == "Summa Codicis"

    def test_parse_extracts_vertical_path(self, tmp_path):
        """Test que le chemin vertical.txt est extrait correctement."""
        v1 = str(tmp_path / "vertical.txt")
        v2 = str(tmp_path / "vertical2.txt")
        # Creer un XML ou le fichier se termine par vertical.txt
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<root>
  <item eid="item">
    <metadata pid="identifier" aid="doi">10.34847/nkl.test</metadata>
    <metadata pid="title">Test</metadata>
    <metadata pid="file">{v1}</metadata>
  </item>
</root>"""
        xml_path = str(tmp_path / "test.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        items = parse_hera_xml(xml_path)

        assert len(items) == 1
        assert items[0]["vertical_path"] == os.path.normpath(v1)

    def test_parse_nonexistent_file(self):
        """Test parsing d'un fichier XML inexistant."""
        items = parse_hera_xml("/nonexistent/file.xml")
        assert items == []

    def test_parse_invalid_xml(self, tmp_path):
        """Test parsing d'un fichier XML malformé."""
        bad_xml = tmp_path / "bad.xml"
        bad_xml.write_text("<invalid><<<", encoding="utf-8")

        items = parse_hera_xml(str(bad_xml))
        assert items == []

    def test_parse_item_without_doi(self, tmp_path):
        """Test qu'un item sans DOI est ignoré."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
  <item eid="item">
    <metadata pid="title">Orphan</metadata>
    <metadata pid="file">vertical.txt</metadata>
  </item>
</root>"""
        xml_path = str(tmp_path / "no_doi.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        items = parse_hera_xml(xml_path)
        assert items == []


# ── Tests extract_page_number ────────────────────────────────────────

class TestExtractPageNumber:
    """Tests pour l'extraction du numéro de page."""

    def test_standard_page_filename(self):
        assert extract_page_number("page_0001_brachylogus.txt") == 1

    def test_high_page_number(self):
        assert extract_page_number("page_0158_xxx.txt") == 158

    def test_page_with_path(self):
        assert extract_page_number("/some/path/page_0042_test.txt") == 42

    def test_non_page_filename(self):
        assert extract_page_number("fiche.pdf") is None

    def test_vertical_filename(self):
        assert extract_page_number("vertical.txt") is None


# ── Tests escape_url_for_attr ────────────────────────────────────────

class TestEscapeUrlForAttr:
    """Tests pour l'échappement des URLs dans les attributs XML."""

    def test_simple_url(self):
        result = escape_url_for_attr("https://nakala.fr/10.34847/xxx#sha1")
        assert "https://nakala.fr/10.34847/xxx#sha1" in result

    def test_url_with_ampersand(self):
        result = escape_url_for_attr("https://example.com?a=1&b=2")
        assert "&amp;" in result


# ── Tests add_links_to_vertical ──────────────────────────────────────

class TestAddLinksToVertical:
    """Tests pour l'ajout des liens dans un fichier vertical."""

    def test_add_link_and_fiche(self, tmp_path):
        """Test ajout des attributs link et fiche."""
        vertical = tmp_path / "vertical.txt"
        shutil.copy2(FIXTURES_DIR / "sample_vertical_1.txt", vertical)

        page_mapping = {
            ("Brachylogus", 1): "https://nakala.fr/doi1#sha_page1",
            ("Brachylogus", 2): "https://nakala.fr/doi1#sha_page2",
        }
        fiche_mapping = {
            "Brachylogus": "https://nakala.fr/doi1#sha_fiche",
        }

        modified = add_links_to_vertical(
            str(vertical), "Brachylogus", page_mapping, fiche_mapping
        )

        assert modified == 2

        content = vertical.read_text(encoding="utf-8")
        assert 'link="https://nakala.fr/doi1#sha_page1"' in content
        assert 'link="https://nakala.fr/doi1#sha_page2"' in content
        assert 'fiche="https://nakala.fr/doi1#sha_fiche"' in content

    def test_no_modification_when_no_mapping(self, tmp_path):
        """Test qu'aucune modification n'est faite sans mapping."""
        vertical = tmp_path / "vertical.txt"
        shutil.copy2(FIXTURES_DIR / "sample_vertical_1.txt", vertical)

        original = vertical.read_text(encoding="utf-8")
        modified = add_links_to_vertical(
            str(vertical), "Unknown Title", {}, {}
        )

        assert modified == 0
        assert vertical.read_text(encoding="utf-8") == original

    def test_dry_run_does_not_modify_file(self, tmp_path):
        """Test que dry-run ne modifie pas le fichier."""
        vertical = tmp_path / "vertical.txt"
        shutil.copy2(FIXTURES_DIR / "sample_vertical_1.txt", vertical)

        original = vertical.read_text(encoding="utf-8")
        page_mapping = {
            ("Brachylogus", 1): "https://nakala.fr/doi1#sha_page1",
        }
        fiche_mapping = {"Brachylogus": "https://nakala.fr/doi1#sha_fiche"}

        modified = add_links_to_vertical(
            str(vertical), "Brachylogus", page_mapping, fiche_mapping,
            dry_run=True
        )

        assert modified == 2
        # Le fichier ne doit PAS avoir changé
        assert vertical.read_text(encoding="utf-8") == original

    def test_no_duplicate_links(self, tmp_path):
        """Test que les liens ne sont pas ajoutés en double."""
        vertical = tmp_path / "vertical.txt"
        vertical.write_text(
            '<doc link="https://existing.url" edition_id="Edi-101" '
            'source="Brachylogus" page_number="1">\n</doc>\n',
            encoding="utf-8"
        )

        page_mapping = {
            ("Brachylogus", 1): "https://nakala.fr/new#sha",
        }

        modified = add_links_to_vertical(
            str(vertical), "Brachylogus", page_mapping, {}
        )

        # link= déjà présent, ne doit pas être remplacé
        assert modified == 0

    def test_nonexistent_file(self):
        """Test avec un fichier inexistant."""
        modified = add_links_to_vertical(
            "/nonexistent/vertical.txt", "Title", {}, {}
        )
        assert modified == 0


# ── Tests process_vertical_files ─────────────────────────────────────

class TestProcessVerticalFiles:
    """Tests pour le traitement batch des fichiers vertical."""

    def test_process_returns_modified_files(self, tmp_path):
        """Test que la liste des fichiers modifiés est retournée."""
        v1 = str(tmp_path / "vertical1.txt")
        v2 = str(tmp_path / "vertical2.txt")
        copy_vertical("sample_vertical_1.txt", v1)
        copy_vertical("sample_vertical_2.txt", v2)

        items = [
            {"doi": "doi1", "title": "Brachylogus", "vertical_path": v1},
            {"doi": "doi2", "title": "Summa Codicis", "vertical_path": v2},
        ]
        page_mapping = {
            ("Brachylogus", 1): "https://nakala.fr/doi1#p1",
            ("Brachylogus", 2): "https://nakala.fr/doi1#p2",
            ("Summa Codicis", 1): "https://nakala.fr/doi2#p1",
        }
        fiche_mapping = {}

        stats = process_vertical_files(items, page_mapping, fiche_mapping)

        assert stats["files_processed"] == 2
        assert stats["files_skipped"] == 0
        assert stats["total_modified"] == 3
        assert len(stats["modified_files"]) == 2
        assert v1 in stats["modified_files"]
        assert v2 in stats["modified_files"]

    def test_process_skips_missing_path(self):
        """Test qu'un item sans vertical_path est ignoré."""
        items = [
            {"doi": "doi1", "title": "NoPath"},
        ]
        stats = process_vertical_files(items, {}, {})

        assert stats["files_processed"] == 0
        assert stats["files_skipped"] == 1
        assert stats["modified_files"] == []

    def test_process_skips_nonexistent_file(self, tmp_path):
        """Test qu'un fichier vertical inexistant est ignoré."""
        items = [
            {"doi": "doi1", "title": "Ghost",
             "vertical_path": str(tmp_path / "ghost.txt")},
        ]
        stats = process_vertical_files(items, {}, {})

        assert stats["files_processed"] == 0
        assert stats["files_skipped"] == 1
        assert stats["modified_files"] == []

    def test_modified_files_excludes_unmodified(self, tmp_path):
        """Test que seuls les fichiers effectivement modifiés sont listés."""
        v1 = str(tmp_path / "vertical1.txt")
        copy_vertical("sample_vertical_1.txt", v1)

        items = [
            {"doi": "doi1", "title": "Brachylogus", "vertical_path": v1},
        ]
        # Mapping vide : aucune modification
        stats = process_vertical_files(items, {}, {})

        assert stats["files_processed"] == 1
        assert stats["total_modified"] == 0
        assert stats["modified_files"] == []


# ── Tests create_merged_vertical ─────────────────────────────────────

class TestCreateMergedVertical:
    """Tests pour la fusion des fichiers verticaux modifiés."""

    def test_merge_two_files(self, tmp_path):
        """Test fusion de 2 fichiers verticaux."""
        v1 = str(tmp_path / "a_vertical.txt")
        v2 = str(tmp_path / "b_vertical.txt")
        copy_vertical("sample_vertical_1.txt", v1)
        copy_vertical("sample_vertical_2.txt", v2)

        output = str(tmp_path / "corpus.txt")
        stats = create_merged_vertical([v1, v2], output)

        assert stats is not None
        assert stats["files_merged"] == 2
        assert stats["total_size"] > 0

        content = Path(output).read_text(encoding="utf-8")
        # Les deux fichiers doivent être présents
        assert "Brachylogus" in content
        assert "Summa Codicis" in content

    def test_merge_sorted_by_filename(self, tmp_path):
        """Test que la fusion trie par nom de fichier."""
        v_z = str(tmp_path / "z_vertical.txt")
        v_a = str(tmp_path / "a_vertical.txt")

        Path(v_z).write_text("<doc>Z content</doc>\n", encoding="utf-8")
        Path(v_a).write_text("<doc>A content</doc>\n", encoding="utf-8")

        output = str(tmp_path / "merged.txt")
        # Passer les fichiers dans le désordre
        create_merged_vertical([v_z, v_a], output)

        content = Path(output).read_text(encoding="utf-8")
        pos_a = content.index("A content")
        pos_z = content.index("Z content")
        # A doit apparaître avant Z (tri alphabétique)
        assert pos_a < pos_z

    def test_merge_empty_list(self):
        """Test fusion avec une liste vide."""
        result = create_merged_vertical([], "/tmp/empty.txt")
        assert result is None

    def test_merge_dry_run(self, tmp_path):
        """Test que dry-run ne crée pas le fichier."""
        v1 = str(tmp_path / "vertical.txt")
        copy_vertical("sample_vertical_1.txt", v1)

        output = str(tmp_path / "output.txt")
        stats = create_merged_vertical([v1], output, dry_run=True)

        assert stats is not None
        assert stats["files_merged"] == 1
        assert stats["total_size"] == 0
        assert not Path(output).exists()

    def test_merge_single_file(self, tmp_path):
        """Test fusion avec un seul fichier."""
        v1 = str(tmp_path / "vertical.txt")
        copy_vertical("sample_vertical_1.txt", v1)

        output = str(tmp_path / "output.txt")
        stats = create_merged_vertical([v1], output)

        assert stats["files_merged"] == 1
        original = Path(v1).read_text(encoding="utf-8")
        merged = Path(output).read_text(encoding="utf-8")
        assert original in merged

    def test_merge_adds_trailing_newline(self, tmp_path):
        """Test qu'un saut de ligne est ajouté si absent en fin de fichier."""
        v1 = str(tmp_path / "a.txt")
        v2 = str(tmp_path / "b.txt")
        # Fichier sans newline finale
        Path(v1).write_text("<doc>content A</doc>", encoding="utf-8")
        Path(v2).write_text("<doc>content B</doc>\n", encoding="utf-8")

        output = str(tmp_path / "merged.txt")
        create_merged_vertical([v1, v2], output)

        content = Path(output).read_text(encoding="utf-8")
        # Le contenu de B ne doit pas être collé à celui de A
        assert "<doc>content A</doc>\n<doc>content B</doc>" in content

    def test_merge_invalid_output_path(self, tmp_path):
        """Test fusion vers un chemin d'écriture invalide."""
        v1 = str(tmp_path / "vertical.txt")
        copy_vertical("sample_vertical_1.txt", v1)

        result = create_merged_vertical(
            [v1], "/nonexistent/dir/output.txt"
        )
        assert result is None


# ── Tests get_api_urls ───────────────────────────────────────────────

class TestGetApiUrls:
    """Tests pour la sélection des URLs API."""

    def test_production_urls(self):
        api, front = get_api_urls(test=False)
        assert api == "https://api.nakala.fr"
        assert front == "https://nakala.fr"

    def test_test_urls(self):
        api, front = get_api_urls(test=True)
        assert api == "https://apitest.nakala.fr"
        assert front == "https://test.nakala.fr"


# ── Test d'intégration ───────────────────────────────────────────────

class TestIntegration:
    """Test d'intégration : enrichissement + fusion."""

    def test_full_pipeline_with_merge(self, tmp_path):
        """Test du pipeline complet : enrichissement puis fusion."""
        # Préparer les fichiers
        v1 = str(tmp_path / "vertical1.txt")
        v2 = str(tmp_path / "vertical2.txt")
        copy_vertical("sample_vertical_1.txt", v1)
        copy_vertical("sample_vertical_2.txt", v2)

        items = [
            {"doi": "doi1", "title": "Brachylogus", "vertical_path": v1},
            {"doi": "doi2", "title": "Summa Codicis", "vertical_path": v2},
        ]
        page_mapping = {
            ("Brachylogus", 1): "https://nakala.fr/doi1#sha_p1",
            ("Brachylogus", 2): "https://nakala.fr/doi1#sha_p2",
            ("Summa Codicis", 1): "https://nakala.fr/doi2#sha_p1",
        }
        fiche_mapping = {
            "Brachylogus": "https://nakala.fr/doi1#sha_fiche",
        }

        # Etape 3 : enrichissement
        file_stats = process_vertical_files(items, page_mapping, fiche_mapping)

        assert file_stats["total_modified"] == 3
        assert len(file_stats["modified_files"]) == 2

        # Etape 4 : fusion
        output = str(tmp_path / "corpus.txt")
        merge_stats = create_merged_vertical(
            file_stats["modified_files"], output
        )

        assert merge_stats is not None
        assert merge_stats["files_merged"] == 2

        # Vérifier le contenu du fichier fusionné
        content = Path(output).read_text(encoding="utf-8")
        assert 'link="https://nakala.fr/doi1#sha_p1"' in content
        assert 'link="https://nakala.fr/doi2#sha_p1"' in content
        assert 'fiche="https://nakala.fr/doi1#sha_fiche"' in content
        assert "Brachylogus" in content
        assert "Summa Codicis" in content
