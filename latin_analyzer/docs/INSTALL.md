# Guide d'installation detaille

Ce guide explique comment installer l'analyseur pas a pas.
Si vous etes presse, lancez simplement `bash setup.sh` (voir [QUICKSTART.md](QUICKSTART.md)).

---

## Ce qu'il vous faut avant de commencer

- **Python 3.8 ou plus recent** (teste sur Python 3.11)
- **pip** (le gestionnaire de paquets Python, normalement inclus avec Python)
- **git** (pour telecharger PyCollatinus - optionnel)

Pour verifier :
```bash
python3 --version    # Doit afficher 3.8 ou plus
pip --version        # Doit afficher quelque chose
git --version        # Necessaire seulement pour PyCollatinus
```

---

## Etape 1 : Installer les bibliotheques Python

Depuis le dossier du projet :

```bash
cd latin_analyzer
pip install -r requirements.txt
```

Cela installe 3 bibliotheques :
- **python-docx** : pour generer les fichiers Word
- **lxml** : pour lire les fichiers XML
- **unidecode** : pour normaliser les caracteres speciaux

Si `pip install -r requirements.txt` ne fonctionne pas, installez-les une par une :
```bash
pip install python-docx
pip install lxml
pip install unidecode
```

---

## Etape 2 : Installer PyCollatinus (optionnel)

PyCollatinus est un dictionnaire de latin classique. **Depuis la version 2.4.0, il est optionnel** :
le programme fonctionne sans lui (avec le dictionnaire Du Cange uniquement).

Si vous voulez l'installer pour une meilleure precision :

```bash
# Telecharger depuis GitHub
cd /tmp
git clone https://github.com/PonteIneptique/collatinus-python.git

# Corriger un bug de compatibilite Python 3.10+
sed -i 's/from collections import OrderedDict, Callable/from collections import OrderedDict\nfrom collections.abc import Callable/' \
    /tmp/collatinus-python/pycollatinus/util.py
```

**Pourquoi `/tmp` ?** Le programme cherche PyCollatinus dans `/tmp/collatinus-python` par defaut.
Ce n'est pas installe via `pip` car le paquet pip est casse.

**Premier lancement lent ?** C'est normal, PyCollatinus met 10-15 secondes a charger la premiere fois.

---

## Etape 3 : Telecharger le dictionnaire Du Cange

Le dictionnaire Du Cange contient ~100 000 mots de latin medieval. C'est le dictionnaire principal.

```bash
cd latin_analyzer/scripts
python3 download_ducange.py
```

Cela va :
1. Telecharger 24 fichiers XML depuis SourceForge (~78 Mo)
2. Extraire les mots latins
3. Creer le fichier `latin_analyzer/data/ducange_data/dictionnaire_ducange.txt`

---

## Verifier que tout fonctionne

### Test 1 : Les bibliotheques Python

```bash
python3 -c "import docx; import lxml; import unidecode; print('Toutes les libs sont OK')"
```

Vous devez voir : `Toutes les libs sont OK`

### Test 2 : PyCollatinus (si installe)

```bash
cd latin_analyzer/tests
python3 test_pycollatinus.py
```

Si PyCollatinus n'est pas installe, ce test echouera. Ce n'est pas grave.

### Test 3 : Integration XML Pages

```bash
cd latin_analyzer/tests
python3 test_xml_integration.py
```

---

## Resolution de problemes

### "No module named 'docx'"

Le paquet s'appelle `python-docx` (pas `docx`) :
```bash
pip install python-docx
```

### "No module named 'unidecode'"

```bash
pip install unidecode
```

### "cannot import name 'Callable' from 'collections'"

Ce probleme arrive avec Python 3.10 et plus recent. Deux solutions :

**Solution 1** (recommandee) : Ne rien faire. Depuis la version 2.4.0, le programme fonctionne sans PyCollatinus.

**Solution 2** : Corriger le fichier source de PyCollatinus :
```bash
sed -i 's/from collections import OrderedDict, Callable/from collections import OrderedDict\nfrom collections.abc import Callable/' \
    /tmp/collatinus-python/pycollatinus/util.py
```

### Le dictionnaire Du Cange n'est pas trouve

Verifiez que le fichier existe :
```bash
ls latin_analyzer/data/ducange_data/dictionnaire_ducange.txt
```

Si non, retelecharger :
```bash
cd latin_analyzer/scripts
python3 download_ducange.py
```

### "prefix 'xml' not found in prefix map"

Erreur lors du telechargement Du Cange. Le script `download_ducange.py` gere ce cas.
Verifiez que vous avez la derniere version du script.

### PyCollatinus est tres lent

Le premier chargement prend 10-15 secondes. C'est normal.
Les analyses suivantes dans la meme session sont rapides.

---

## Environnement virtuel (optionnel, pour utilisateurs avances)

Si vous voulez isoler les dependances :

```bash
# Creer l'environnement
python3 -m venv venv_latin

# L'activer
source venv_latin/bin/activate

# Installer les dependances
pip install -r requirements.txt
```

A chaque session, pensez a activer l'environnement :
```bash
source venv_latin/bin/activate
```

---

## Arborescence apres installation

```
latin_analyzer/
├── src/
│   ├── latin_analyzer_v2.py          # Le programme principal
│   ├── page_xml_parser.py            # Lecture XML Pages
│   └── __init__.py
│
├── data/
│   └── ducange_data/
│       └── dictionnaire_ducange.txt  # 99 917 mots (cree a l'etape 3)
│
├── tests/
│   ├── test_pycollatinus.py
│   └── test_xml_integration.py
│
├── scripts/
│   └── download_ducange.py
│
├── docs/
│   ├── INSTALL.md                    # Ce guide
│   ├── QUICKSTART.md
│   └── GUIDE_XML_PAGES.md
│
├── requirements.txt
└── setup.sh

/tmp/collatinus-python/               # PyCollatinus (optionnel, etape 2)
```

---

**Auteur** : CiSaMe
**Version** : 2.4.0
