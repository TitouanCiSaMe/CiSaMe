# Module Latin Analyzer - Validation de textes latins médiévaux

## 📖 Description

Le module **Latin Analyzer** est un outil automatisé d'analyse et de validation de textes latins médiévaux avec détection intelligente des erreurs. Il combine deux sources complémentaires (PyCollatinus pour le latin classique et le dictionnaire Du Cange pour le latin médiéval) avec un système de scoring multi-critères pour produire des documents Word colorisés indiquant la fiabilité de chaque mot.

## 🎯 Objectif

Valider la qualité des transcriptions HTR/OCR de textes latins médiévaux en :
- Détectant automatiquement les erreurs de transcription
- Identifiant les mots latins valides (classiques et médiévaux)
- Produisant un document colorisé pour correction manuelle
- Générant des rapports d'analyse détaillés

## 🔄 Position dans le workflow

**Entrée** :
- **Module 4** (eScriptorium) : XML Pages avec transcriptions HTR/OCR brutes
- **Module 5** (Post-traitement) : XML Pages nettoyées
- Ou fichiers TXT bruts

**Sortie** :
- Document DOCX colorisé (3 niveaux : Noir/Orange/Rouge)
- Rapport d'analyse optionnel (statistiques, patterns, recommandations)

**Utilisation recommandée** : Validation qualité après Module 4 ou Module 5

## ⚙️ Fonctionnalités principales

### 1. Extraction et pré-traitement
- Support XML Pages (single/dual colonnes) via PageXMLParser
- Extraction automatique MainZone
- Fusion des mots coupés avec tirets (sancti- + tatis → sanctitatis)
- Lecture fichiers TXT bruts

### 2. Normalisation
- **u/v** : Variantes médiévales (uel = vel, uidetur = videtur)
- **i/j** : Variantes médiévales (iam = jam, iudicium = judicium)
- **Chiffres romains** : Filtrage automatique (xuiii., uii., ui.)

### 3. Analyse multi-sources
- **PyCollatinus** : ~500 000 formes de latin classique
  - Lemmatisation automatique
  - Analyse morphologique
  - +30 points si reconnu

- **Dictionnaire Du Cange** : 99 917 mots de latin médiéval
  - Latin ecclésiastique, féodal, administratif
  - +40 points si présent

### 4. Scoring multi-critères (0-100)
- Critère 1 : Latin classique (Collatinus) → +30 points
- Critère 2 : Latin médiéval (Du Cange) → +40 points
- Critère 3 : Suffixe productif (-arius, -atio, -torium...) → +10 points
- Critère 4 : Contexte ecclésiastique (abbas, ecclesia...) → +5 points
- Critère 5 : Variante orthographique (ae↔e, ti↔ci) → +10 points

### 5. Colorisation (3 niveaux)
- **⚫ Noir** (score ≥75) : Mot validé, pas d'erreur
- **🟠 Orange** (score 40-74) : À vérifier manuellement
- **🔴 Rouge** (score <40) : Erreur probable

### 6. Rapport d'analyse (optionnel)
- Statistiques détaillées (total, uniques, longueur moyenne)
- Distribution par longueur
- Patterns détectés (géminées, ae/oe, ph, terminaisons)
- TOP 50 mots les plus fréquents non reconnus
- Catégorisation (abréviations, erreurs OCR, variantes médiévales)
- Recommandations personnalisées
- Estimation d'amélioration potentielle

## 📊 Résultats typiques

**Exemple sur corpus réel** :
- ✅ **86%** de mots validés (noir)
- ⚠️ **13%** à vérifier (orange)
- ❌ **0%** erreurs probables (rouge)

**Sources de reconnaissance** :
- 🏛️ PyCollatinus (classique) : 5 272 mots
- 📖 Du Cange (médiéval) : 3 766 mots
- 🔗 Reconnus par les deux : 3 709 mots

## 💻 Utilisation

### Installation

```bash
cd /home/user/CiSaMe/latin_analyzer
bash setup.sh
```

**Temps d'installation** : ~3 minutes (téléchargement PyCollatinus + Du Cange)

### Commandes CLI

**Analyser un fichier texte** :
```bash
python3 latin_analyzer_v2.py -i texte.txt -o resultat.docx
```

**Analyser des XML Pages (1 colonne)** :
```bash
python3 latin_analyzer_v2.py -i corpus_xml/ -o resultat.docx -m xml-single
```

**Analyser des XML Pages (2 colonnes)** :
```bash
python3 latin_analyzer_v2.py -i corpus_xml/ -o resultat.docx -m xml-dual
```

**Avec rapport d'analyse détaillé** :
```bash
python3 latin_analyzer_v2.py -i texte.txt -o resultat.docx --report analyse_orange.txt
```

**Avec dictionnaire Du Cange personnalisé** :
```bash
python3 latin_analyzer_v2.py -i texte.txt -o resultat.docx -d /chemin/ducange.txt
```

### Arguments

- `-i, --input` : Fichier TXT ou dossier XML Pages (obligatoire)
- `-o, --output` : Fichier DOCX de sortie (obligatoire)
- `-m, --mode` : Mode d'extraction (txt / xml-single / xml-dual)
- `-d, --ducange` : Chemin vers dictionnaire Du Cange (optionnel)
- `--report` : Générer rapport d'analyse des mots orange (optionnel)

## 🛠️ Technologies utilisées

- **Python 3.10+** : Langage principal
- **PyCollatinus** : Lemmatisation latin classique
- **Du Cange** : Dictionnaire latin médiéval (99 917 mots)
- **python-docx** : Génération documents Word
- **lxml** : Parsing XML Pages
- **PageXMLParser** : Extraction MainZone

## 📁 Structure du module

```
Module_Latin_Analyzer/
├── flowchart-latin-analyzer.mmd    # Schéma du workflow
└── README.md                        # Cette documentation
```

**Code source** : `/home/user/CiSaMe/latin_analyzer/`

## ✅ Avantages vs. workflow manuel

| Aspect | Version manuelle (v1.x) | Latin Analyzer (v2.3) |
|--------|-------------------------|------------------------|
| **Workflow** | Interface GUI Collatinus | CLI automatique |
| **Configuration** | Chemins en dur | Arguments flexibles |
| **Dictionnaire** | Latin classique uniquement | Classique + 100k médiéval |
| **Détection** | Binaire (erreur/OK) | Score 0-100 + 3 couleurs |
| **Taux reconnaissance** | ~60% (faux positifs) | **86%** (multi-sources) |
| **XML Pages** | Non supporté | Extraction intégrée |
| **Césures** | Ignorées (erreurs) | Fusionnées automatiquement |
| **Variantes u/v, i/j** | Différentes | Normalisées |
| **Chiffres romains** | Erreurs | Filtrés automatiquement |

## 🔗 Liens utiles

- **Documentation complète** : `/home/user/CiSaMe/latin_analyzer/README.md`
- **Schéma workflow** : `flowchart-latin-analyzer.mmd`
- [Du Cange en ligne](http://ducange.enc.sorbonne.fr/)
- [PyCollatinus GitHub](https://github.com/PonteIneptique/collatinus-python)

## 📝 Changelog

**Version 2.3.0** (Nov 2025) :
- Rapport d'analyse des mots orange avec recommandations

**Version 2.2.0** (Nov 2025) :
- Correction bug critique PyCollatinus (0% → 86% reconnaissance)

**Version 2.1.0** (Nov 2025) :
- Interface CLI avec argparse
- Extraction XML intégrée
- Fusion automatique mots coupés
- Normalisation u/v et i/j

**Version 2.0.0** (Nov 2025) :
- Intégration PyCollatinus + Du Cange
- Scoring multi-critères
- Support XML Pages

## 📄 Licence

À définir selon le projet CiSaMe
