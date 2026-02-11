# Demarrage rapide

## Installation

```bash
cd latin_analyzer
bash setup.sh
```

C'est tout. Le script installe les dependances, PyCollatinus et le dictionnaire Du Cange.

Si ca ne marche pas, voir [INSTALL.md](INSTALL.md) pour l'installation manuelle.

---

## Analyser un texte

### Fichier texte (.txt)

```bash
cd latin_analyzer/src
python3 latin_analyzer_v2.py -i mon_texte.txt -o resultat.docx
```

Ouvrez `resultat.docx` : les mots sont colores en noir (OK), orange (douteux) ou rouge (erreur).

---

### Fichiers XML Pages (1 colonne)

```bash
python3 latin_analyzer_v2.py -i /chemin/vers/dossier_xml/ -o resultat.docx -m xml-single
```

---

### Fichiers XML Pages (2 colonnes)

```bash
python3 latin_analyzer_v2.py -i /chemin/vers/dossier_xml/ -o resultat.docx -m xml-dual
```

---

### Avec rapport des mots non reconnus

```bash
python3 latin_analyzer_v2.py -i mon_texte.txt -o resultat.docx --report rapport.txt
```

Le rapport liste les mots non reconnus les plus frequents et propose des pistes d'amelioration.

---

## Verifier que tout fonctionne

```bash
# Tester les dependances Python
python3 -c "import docx; import lxml; print('OK')"

# Tester PyCollatinus (optionnel)
cd latin_analyzer/tests
python3 test_pycollatinus.py

# Tester XML Pages
python3 test_xml_integration.py
```

---

## Aide rapide

| Probleme | Solution |
|----------|----------|
| `No module named 'docx'` | `pip install python-docx` |
| `No module named 'lxml'` | `pip install lxml` |
| PyCollatinus plante | Ce n'est pas grave, il est optionnel depuis v2.4.0 |
| Dictionnaire Du Cange manquant | `cd latin_analyzer/scripts && python3 download_ducange.py` |

Pour plus de details : [INSTALL.md](INSTALL.md) ou le [README principal](../README.md).

---

**Version** : 2.4.0
