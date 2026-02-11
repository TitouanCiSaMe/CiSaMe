# Analyseur de Textes Latins Medievaux - Version 2.4.0

Outil pour verifier automatiquement la qualite de textes latins medievaux (issus d'OCR/HTR).
Il colore chaque mot selon sa fiabilite : **noir** (bon), **orange** (douteux), **rouge** (erreur probable).

---

## A quoi ca sert ?

Quand on transcrit un manuscrit medieval avec un logiciel d'OCR ou HTR (ex: eScriptorium, Transkribus),
le resultat contient des erreurs. Cet outil analyse chaque mot du texte et le compare a deux dictionnaires :

1. **PyCollatinus** : dictionnaire de latin classique (~500 000 formes)
2. **Du Cange** : dictionnaire de latin medieval (~100 000 mots)

Chaque mot recoit un **score de 0 a 100** et une couleur :

| Couleur | Score | Signification |
|---------|-------|---------------|
| **Noir** | 75-100 | Mot reconnu, probablement correct |
| **Orange** | 40-74 | Mot douteux, a verifier manuellement |
| **Rouge** | 0-39 | Mot probablement faux (erreur OCR) |

Le resultat est un fichier Word (.docx) avec le texte colore.

---

## Installation

### Methode rapide (recommandee)

```bash
cd latin_analyzer
bash setup.sh
```

Cela installe tout automatiquement en ~3 minutes.

### Methode manuelle

Si `setup.sh` ne fonctionne pas, voir le guide detaille : [docs/INSTALL.md](docs/INSTALL.md)

---

## Utilisation

### 1. Analyser un fichier texte (.txt)

```bash
cd latin_analyzer/src
python3 latin_analyzer_v2.py -i mon_texte.txt -o resultat.docx
```

- `-i` : le fichier d'entree (votre texte latin)
- `-o` : le fichier de sortie (le Word colore)

### 2. Analyser des fichiers XML Pages

Si votre texte vient d'eScriptorium ou d'un autre outil HTR, vous avez des fichiers XML PAGE.
Mettez-les tous dans un dossier et lancez :

```bash
# Si le manuscrit a 1 colonne de texte par page :
python3 latin_analyzer_v2.py -i mon_dossier_xml/ -o resultat.docx -m xml-single

# Si le manuscrit a 2 colonnes de texte par page :
python3 latin_analyzer_v2.py -i mon_dossier_xml/ -o resultat.docx -m xml-dual
```

Le `-m` (mode) indique le format :
- `txt` : fichier texte brut (par defaut)
- `xml-single` : XML PAGE, 1 colonne
- `xml-dual` : XML PAGE, 2 colonnes

### 3. Generer un rapport detaille

Pour avoir un rapport sur les mots non reconnus (utile pour ameliorer la transcription) :

```bash
python3 latin_analyzer_v2.py -i mon_texte.txt -o resultat.docx --report rapport.txt
```

Le rapport contient :
- Les 50 mots non reconnus les plus frequents
- Des categories (abreviations, erreurs OCR, variantes medievales)
- Des recommandations pour ameliorer le taux de reconnaissance

### 4. Specifier un dictionnaire Du Cange personnalise

Par defaut, le dictionnaire est cherche dans `latin_analyzer/data/ducange_data/`.
Si vous l'avez place ailleurs :

```bash
python3 latin_analyzer_v2.py -i texte.txt -o resultat.docx -d /chemin/vers/dictionnaire_ducange.txt
```

---

## Comprendre le resultat

### Le fichier Word

Ouvrez le fichier `.docx` genere. Vous verrez votre texte avec 3 couleurs :

- Les mots en **noir** sont reconnus par au moins un dictionnaire
- Les mots en **orange** sont partiellement reconnus (suffixe latin, contexte ecclesiastique...)
- Les mots en **rouge** ne sont reconnus nulle part (probablement des erreurs OCR)

### Les statistiques dans le terminal

A la fin de l'analyse, le programme affiche un resume :

```
Distribution des scores :
  Noir (bons mots)      : 5717 (86%)
  Orange (douteux)       : 524 (8%)
  Rouge (erreurs prob.)  : 388 (6%)
```

### Les pages dans le Word

Si vous analysez un dossier XML, chaque fichier XML correspond a une page/folio.
Le Word genere contient des separateurs visuels entre les pages :

```
──────────────────── Folio: 0042_r | Page: 1 ────────────────────
Dominus enim dicit in evangelio quod est ueritas...

──────────────────── Folio: 0042_v | Page: 2 ────────────────────
Et ideo beatus augustinus ait in libro...
```

---

## Fonctionnalites avancees

### PyCollatinus est optionnel

Si PyCollatinus n'est pas installe (ou plante a l'import), le programme fonctionne
quand meme en utilisant uniquement le dictionnaire Du Cange. Vous verrez un message :

```
PyCollatinus non disponible - analyse avec Du Cange uniquement
```

L'analyse sera moins precise mais reste utilisable.

### Comment le scoring fonctionne

Chaque mot demarre avec un score de base de **25 points**. Ensuite :

| Critere | Points ajoutes | Explication |
|---------|----------------|-------------|
| Reconnu par PyCollatinus | +50 | Le mot existe en latin classique |
| Reconnu par Du Cange | +50 | Le mot existe en latin medieval |
| Suffixe latin productif | +10 | Terminaison comme -arius, -atio, -torium... |
| Contexte ecclesiastique | +5 | Mots religieux autour (ecclesia, deus...) |
| Variante orthographique | +10 | Forme alternative detectee (ae/e, ti/ci...) |

Le score est plafonne a 100. Exemples :
- `dominus` : reconnu par les deux → 25 + 50 + 50 = 100 → **noir**
- `sanctitatis` : reconnu par Du Cange seul, suffixe latin → 25 + 50 + 10 = 85 → **noir**
- `abbrevatio` : suffixe latin + contexte → 25 + 10 + 5 = 40 → **orange**
- `xqzfgh` : rien reconnu → 25 → **rouge**

### Normalisations automatiques

Le programme normalise automatiquement certaines variations :

- **u/v** : `uel` est traite comme `vel`, `uidetur` comme `videtur`
- **i/j** : `iam` est traite comme `jam`
- **Cesures** : si un mot est coupe en fin de ligne (`sancti-` + `tatis`), il est recolle en `sanctitatis`
- **Chiffres romains** : `xuiii.`, `uii.`, `ui.` ne sont pas comptes comme des erreurs

---

## Utiliser dans un script Python

Si vous voulez integrer l'analyseur dans votre propre code Python :

```python
# Importer la classe
from latin_analyzer.src.latin_analyzer_v2 import LatinAnalyzer

# Creer l'analyseur
# (le dictionnaire Du Cange est trouve automatiquement)
analyzer = LatinAnalyzer()

# Analyser un fichier texte
resultats = analyzer.analyze_text_file("mon_texte.txt")

# Analyser des XML Pages
resultats = analyzer.analyze_page_xml("dossier_xml/", column_mode="single")

# Generer le Word colore
analyzer.generate_docx("resultat.docx", resultats)
```

Pour specifier un dictionnaire Du Cange personnalise :

```python
analyzer = LatinAnalyzer(ducange_dict_file="/chemin/vers/dictionnaire_ducange.txt")
```

---

## Structure du projet

```
latin_analyzer/
├── src/                              # Code source
│   ├── latin_analyzer_v2.py          # Programme principal
│   ├── page_xml_parser.py            # Lecture des fichiers XML PAGE
│   ├── export_xml_to_txt.py          # Export XML vers texte brut
│   └── __init__.py
│
├── data/                             # Donnees
│   └── ducange_data/                 # Dictionnaire Du Cange
│       └── dictionnaire_ducange.txt  # 99 917 mots de latin medieval
│
├── tests/                            # Tests
│   ├── test_pycollatinus.py
│   └── test_xml_integration.py
│
├── docs/                             # Documentation
│   ├── INSTALL.md                    # Guide d'installation detaille
│   ├── QUICKSTART.md                 # Demarrage rapide
│   ├── GUIDE_XML_PAGES.md            # Guide XML Pages
│   └── README_AMELIORATIONS.md       # Details techniques
│
├── scripts/                          # Utilitaires
│   └── download_ducange.py           # Telecharger le dictionnaire
│
├── requirements.txt                  # Dependances Python
└── setup.sh                          # Installation automatique
```

---

## Dependances

| Package | Role | Obligatoire ? |
|---------|------|---------------|
| python-docx | Generer les fichiers Word | Oui |
| lxml | Lire les fichiers XML | Oui |
| unidecode | Normaliser les caracteres | Oui |
| PyCollatinus | Dictionnaire latin classique | Non (optionnel depuis v2.4.0) |
| Du Cange | Dictionnaire latin medieval | Recommande |

Installation des dependances obligatoires :
```bash
pip install -r requirements.txt
```

---

## Resolution de problemes

### "No module named 'docx'"

```bash
pip install python-docx
```

### "cannot import name 'Callable' from 'collections'"

Ce probleme arrive avec Python 3.10+. Depuis la version 2.4.0, PyCollatinus est optionnel :
le programme fonctionne sans lui. Si vous voulez quand meme l'utiliser, appliquez le patch :

```bash
sed -i 's/from collections import OrderedDict, Callable/from collections import OrderedDict\nfrom collections.abc import Callable/' \
    /tmp/collatinus-python/pycollatinus/util.py
```

### Le programme ne trouve pas le dictionnaire Du Cange

Verifiez que le fichier existe :
```bash
ls latin_analyzer/data/ducange_data/dictionnaire_ducange.txt
```

Si le fichier n'existe pas, lancez :
```bash
cd latin_analyzer/scripts
python3 download_ducange.py
```

### PyCollatinus est tres lent au premier lancement

C'est normal. Le premier chargement prend 10-15 secondes. Les suivants sont plus rapides.

---

## Changelog

**Version 2.4.0 :**
- PyCollatinus rendu optionnel (fonctionne sans, avec Du Cange seul)
- Correction du scoring : rouge et orange desormais atteignables
- Preservation des pages/folios dans le DOCX (en-tetes visuels)
- Correction bug generator PyCollatinus
- Reset des compteurs entre analyses successives
- Version harmonisee dans tout le projet

**Version 2.3.0 :**
- Rapport d'analyse des mots orange (`--report`)
- Categorisation automatique et recommandations

**Version 2.2.0 :**
- Correction critique : PyCollatinus ne detectait aucun mot (bug generator)
- Passage de 62% a 86% de mots valides

**Version 2.1.0 :**
- Interface CLI avec argparse
- Support XML Pages integre
- Fusion des cesures, normalisation u/v et i/j

**Version 2.0.0 :**
- Integration PyCollatinus + Du Cange
- Scoring multi-criteres 0-100
- Structure projet organisee

---

## Liens utiles

- [Du Cange en ligne](http://ducange.enc.sorbonne.fr/)
- [PyCollatinus (GitHub)](https://github.com/PonteIneptique/collatinus-python)
- [Collatinus](https://github.com/biblissima/collatinus)

---

**Pour demarrer rapidement : [docs/QUICKSTART.md](docs/QUICKSTART.md)**

**Auteur** : CiSaMe
**Version** : 2.4.0
