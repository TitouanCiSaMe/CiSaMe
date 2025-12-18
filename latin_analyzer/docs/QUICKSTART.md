# 🚀 Démarrage rapide

## Installation en 1 commande

```bash
bash setup.sh
```

**Ou manuellement :**

```bash
# 1. Installer les bibliothèques
pip install python-docx lxml unidecode

# 2. Cloner PyCollatinus
cd /tmp && git clone https://github.com/PonteIneptique/collatinus-python.git

# 3. Patch Python 3.11
sed -i 's/from collections import OrderedDict, Callable/from collections import OrderedDict\nfrom collections.abc import Callable/' \
    /tmp/collatinus-python/pycollatinus/util.py

# 4. Télécharger Du Cange
cd /home/user/Data_Base && python3 download_ducange.py
```

---

## Utilisation

### 📝 Analyser un fichier texte brut

```bash
cd latin_analyzer/src
python3 latin_analyzer_v2.py -i mon_texte.txt -o resultat.docx
```

---

### 📄 Analyser des fichiers XML Pages (1 colonne)

```bash
cd latin_analyzer/src
python3 latin_analyzer_v2.py -i /path/to/xml_folder/ -o resultat.docx -m xml-single
```

---

### 📄 Analyser des fichiers XML Pages (2 colonnes)

```bash
cd latin_analyzer/src
python3 latin_analyzer_v2.py -i /path/to/xml_folder/ -o resultat.docx -m xml-dual
```

---

### 📊 Générer un rapport d'analyse des mots non reconnus

```bash
cd latin_analyzer/src
python3 latin_analyzer_v2.py -i mon_texte.txt -o resultat.docx --report analyse_orange.txt
```

---

## Tests

```bash
# Test PyCollatinus
python3 test_pycollatinus.py

# Test XML Pages
python3 test_xml_integration.py
```

---

## Structure des fichiers

```
requirements.txt         → Liste des dépendances
setup.sh                 → Installation automatique
INSTALL.md               → Guide complet
QUICKSTART.md            → Ce guide
README_AMELIORATIONS.md  → Documentation Phase 1
GUIDE_XML_PAGES.md       → Documentation XML Pages
```

---

## Aide

**Problème d'import ?**
```bash
pip install -r requirements.txt
```

**PyCollatinus manquant ?**
```bash
cd /tmp && git clone https://github.com/PonteIneptique/collatinus-python.git
```

**Dictionnaire Du Cange manquant ?**
```bash
python3 download_ducange.py
```

---

Pour plus de détails : **INSTALL.md**
