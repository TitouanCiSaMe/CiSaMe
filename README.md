# CiSaMe - Circulation des Savoirs Médiévaux

**Suite d'outils numériques pour l'analyse de manuscrits juridiques médiévaux**

**Université de Strasbourg** | Droit canonique et civil | Moyen Âge

---

## 📖 Présentation du projet

**CiSaMe** (Circulation des Savoirs Médiévaux) est un projet de recherche visant à constituer, enrichir et analyser un corpus de **manuscrits juridique (droit canonique et romain) et théologiques médiévaux** pour les chercheurs en histoire du droit.

### Objectifs

1. **Numériser** : Acquisition d'images haute résolution depuis sources IIIF, PDF et archives
2. **Transcrire** : Reconnaissance automatique HTR/OCR via eScriptorium et modèles Kraken
3. **Enrichir** : Annotation linguistique (lemmatisation, POS-tagging) avec TreeTagger
4. **Analyser** : Outils d'analyse lexicométrique et structurelle (Query Generator, Concordance Analyzer)
5. **Diffuser** : Archives scientifiques (Nakala/Seafile) et corpus interrogeables (NoSketch-Engine)

### Résultats

- **~150 éditions** transcrites et enrichies
- **5,768 records** de métadonnées bibliographiques (Heurist)
- **Corpus annotés** avec lemmes et parties du discours
- **Plateforme web d'analyse** (https://cisame.vercel.app)
- **Concordancier en ligne** pour requêtes CQL avancées

---

## 📋 Pipeline de traitement

Pipeline automatisé en 9 modules pour transformer des images de manuscrits en corpus exploitables :

```
Images → OCR/HTR → Segmentation → Corrections → Nettoyage XML
  → Enrichissement linguistique → Concordancier + Diffusion + Analyse
```

**Technologies** : Python, eScriptorium, Kraken, TreeTagger, NoSketch-Engine, React

---

## 🚀 Installation

### Prérequis
- **Python 3.10+** (requis)
- **Git** (pour PyCollatinus)

### Installation des dépendances

```bash
# Cloner le projet
git clone <URL_DU_DEPOT>
cd CiSaMe

# Installer les dépendances principales
pip install -r requirements.txt

# (Optionnel) Installer les dépendances de développement
pip install -r requirements-dev.txt
```

**📚 Guide complet :** Voir [Documentation/DEPENDENCIES.md](Documentation/DEPENDENCIES.md) pour l'installation détaillée incluant PyCollatinus.

---

## 🚀 Démarrage rapide

### MODULE 1 : Télécharger des images

```bash
python Modules_projet/Module_1/download_images.py --iiif <url_manifest>
```

### MODULE 6 : Enrichir linguistiquement

```bash
cd PAGEtopage
python -m PAGEtopage run --input ./xml_pages/ --output ./output/ --config config.yaml
```

### MODULE 7 : Fusionner pour NoSketch-Engine

```bash
python PAGEtopage/fusion_vertical.py -i ./corpus/ -o corpus_complet.vertical.txt
```

---

## 📂 Structure du projet

```
CiSaMe/
├── PAGEtopage/                  # MODULE 6 : Enrichissement TreeTagger
│   ├── step1_extract/           #   - Extraction XML → JSON
│   ├── step2_enrich/            #   - Lemmatisation + POS-tagging
│   ├── step3_export/            #   - Export 4 formats (scholarly/clean/etc.)
│   ├── step4_reenrich/          #   - Ré-enrichissement après corrections
│   └── fusion_vertical.py       # MODULE 7 : Fusion corpus NoSketch
├── latin_analyzer/              # Analyseur latin (PyCollatinus + Du Cange)
│   ├── src/latin_analyzer_v2.py # Validation automatique textes latins
│   └── data/ducange_data/       # Dictionnaire 100k mots médiévaux
├── Modeles/                     # Modèles Kraken (.mlmodel)
│   ├── MODELES_SEGMENTATION/    # Détection lignes/régions (éditions/manuscrits)
│   └── MODELES_TRANSCRIPTION/   # HTR/OCR (classique/médiéval)
├── Modules_projet/              # Documentation des 9 modules
│   ├── Module_1/                # Téléchargement images
│   │   └── download_images.py   #   - Script téléchargement IIIF
│   ├── Module_2/                # Méthodes acquisition (IIIF/PDF/Hexa/Tuiles)
│   ├── Module_3/                # Récupération éditions (libre/restreint)
│   ├── Module_4/                # eScriptorium (segmentation/transcription HTR)
│   ├── Module_5/                # Nettoyage Oxygène XML (XPath + Regex)
│   ├── Module_6_PAGEtopage/     # Enrichissement linguistique
│   ├── Module_7_NoSketch_Engine/# Concordancier web
│   ├── Module_8_Diffusion_Donnees/ # Documentation workflow Nakala/Seafile
│   ├── Module_9_Visualisation_Requetes/ # Query Generator + Analyzer
│   ├── Module_Metadonnees/      # Base Heurist (5768 records, transversal)
│   ├── Decret_Gratien/          # Pipeline parallèle (4149 fichiers)
│   └── Vue_Ensemble/            # Schéma global intégré
├── Nakala/                      # MODULE 8 : Scripts export Nakala
│   ├── validate_export.py       #   - Validation cohérence données
│   ├── prepare_nakala_export.py #   - Préparation structure Libre/Non_libre
│   ├── upload_nakala.py         #   - Upload via Heimdall
│   └── add_nakala_links.py      #   - Enrichissement URLs verticaux
└── Documentation/               # Guides techniques et scripts
    ├── Fine_tuning_*.sh         # Scripts HPC entraînement Kraken
    ├── liste_manuscrits.csv     # Corpus 317 manuscrits
    └── Guide_Kraken_HTR_Mac.txt # Installation Kraken
```

---

## 📖 Documentation

| Document | Contenu |
|----------|---------|
| **[Documentation/DEPENDENCIES.md](Documentation/DEPENDENCIES.md)** | 📦 Guide installation dépendances (Python, PyCollatinus, TreeTagger) |
| **[Documentation/DEPENDENCY_AUDIT_REPORT.md](Documentation/DEPENDENCY_AUDIT_REPORT.md)** | 🔒 Audit sécurité et recommandations dépendances |
| **[Modules_projet/README.md](Modules_projet/README.md)** | Vue d'ensemble des 9 modules |
| **[Modules_projet/Vue_Ensemble/](Modules_projet/Vue_Ensemble/)** | Schéma global intégré du projet |
| **[PAGEtopage/README.md](PAGEtopage/README.md)** | Guide enrichissement linguistique (MODULE 6) |
| **[Nakala/README.md](Nakala/README.md)** | Guide export Nakala/Seafile (MODULE 8) |
| **[latin_analyzer/README.md](latin_analyzer/README.md)** | Validation automatique textes latins |
| **[Modeles/README.md](Modeles/README.md)** | Modèles Kraken segmentation/transcription |
| **[Documentation/README.md](Documentation/README.md)** | Guides techniques et scripts HPC |

---

## 🛠️ Technologies

| Composant | Technologie |
|-----------|-------------|
| **Langages** | Python 3.10+, JavaScript, Shell, YAML |
| **OCR/HTR** | eScriptorium, Kraken (HPC Unistra) |
| **Enrichissement** | TreeTagger (lemmatisation auto-installée) |
| **Validation latin** | PyCollatinus + Du Cange (100k mots médiévaux) |
| **Base de données** | Heurist (métadonnées bibliographiques) |
| **Stockage** | Seafile (privé), Nakala (public) |
| **Concordancier** | NoSketch-Engine (requêtes CQL) |
| **Frontend** | React 18.2, Vite 5.0 (MODULE 9) |
| **Visualisation** | Recharts, D3.js (MODULE 9) |
| **Tests** | Vitest, React Testing Library (MODULE 9) |
| **Déploiement** | Vercel (MODULE 9) |
| **Formats** | XML PAGE, JSON, YAML, Vertical (NoSketch) |

---

## 📊 Statut des modules

| Module | Statut | Description |
|--------|--------|-------------|
| **MODULE 1** | ✅ Opérationnel | Téléchargement images (IIIF/PDF/Hexa/Tuiles) |
| **MODULE 2** | ✅ Opérationnel | Méthodes d'acquisition d'images |
| **MODULE 3** | ✅ Opérationnel | Récupération éditions (droits libre/restreint/secret) |
| **MODULE 4** | ✅ Opérationnel | eScriptorium (segmentation + transcription HTR) |
| **MODULE 5** | ✅ Opérationnel | Nettoyage Oxygène XML (XPath + Regex) |
| **MODULE 6** | ✅ Opérationnel | PAGEtopage (enrichissement TreeTagger) |
| **MODULE 7** | ✅ Opérationnel | NoSketch-Engine (concordancier) |
| **MODULE 8** | ✅ Opérationnel | Diffusion Nakala/Seafile (scripts `/Nakala/`) |
| **MODULE 9** | ✅ Opérationnel | Canon-Law-Toolkit (plateforme web d'analyse) |
| **Transversal** | ✅ Opérationnel | Module Métadonnées (Heurist) |
| **Parallèle** | ✅ Opérationnel | Décret de Gratien (pipeline spécifique) |

---

## 📊 Corpus

| Métrique | Valeur |
|----------|--------|
| Manuscrits juridiques | 317 |
| Éditions documentées | ~150 |
| Records Heurist | 5,768 |
| Fichiers Décret de Gratien | 4,149 |
| Langues | Latin, Français |
| Période | Moyen Âge |
| Type | Droit canonique et civil |

---

## 🔗 Pipeline complet

```
MODULE 1 : Téléchargement images (IIIF, PDF, etc.)
    ↓
MODULE 2 : Acquisition diverses méthodes
    ↓
MODULE 3 : Récupération éditions (libre/restreint)
    ↓
MODULE 4 : eScriptorium (segmentation + transcription HTR/OCR)
    ↓
MODULE 5 : Nettoyage Oxygène XML (XPath + Regex)
    ↓
MODULE 6 : PAGEtopage (enrichissement TreeTagger)
    │  ← [Module Métadonnées : Heurist → config.yaml]
    ↓
(4 formats : scholarly, clean, diplomatic, annotated + corpus.vertical.txt)
    ↓
    ┌────┴──────┐
    ↓           ↓
MODULE 7     MODULE 8
NoSketch     Diffusion
Engine       (Nakala/Seafile)
(.vertical)
    ↓           ↓
Corpus       Archives
interrogeable scientifiques
    ↓
MODULE 9
Visualisation
(Query Generator
+ Analyzer)
```

**Pipeline parallèle** : Décret de Gratien (format .txt spécifique, déjà sur NoSketch)

---

## 🎯 Cas d'usage

### Workflow typique

1. **Télécharger images** (MODULE 1) : `python Modules_projet/Module_1/download_images.py --iiif <url>`
2. **Transcrire** (MODULE 4) : Importer dans eScriptorium, appliquer modèles Kraken
3. **Nettoyer** (MODULE 5) : Oxygène XML avec XPath + Regex
4. **Enrichir** (MODULE 6) : `python -m PAGEtopage run --input ./xml/ --output ./output/ --config config.yaml`
5. **Diffuser** :
   - NoSketch-Engine (MODULE 7) : Fusion + compilation corpus
   - Nakala/Seafile (MODULE 8) : `python Nakala/prepare_nakala_export.py` puis `upload_nakala.py`
6. **Analyser** (MODULE 9) : Query Generator + visualisations

---

## 🔬 MODULE 9 : Canon-Law-Toolkit

**Plateforme web d'analyse lexicométrique et structurelle**

🌐 **URL** : https://cisame.vercel.app
📦 **Repository** : https://github.com/TitouanCiSaMe/canon-law-toolkit
📌 **Version** : 1.5.0 (Novembre 2025)

### Outils disponibles

#### 1. Query Generator (Générateur de requêtes CQL)

Création de requêtes CQL pour NoSketch-Engine avec :

- **Recherches de proximité** : Localisation de mots à distance configurable (1-20 tokens)
- **Variations orthographiques médiévales** : 96 variantes automatiques (ae/e, v/u, j/i, ti/ci)
- **Recherches sémantiques** : Découverte conceptuelle par lemmes
- **Combinaisons avancées** : Fusion proximité + variations

**Exemple** : Rechercher "dominus" et ses variantes dans un rayon de 5 mots autour de "ecclesia"

#### 2. Concordance Analyzer (Analyseur de concordances)

Analyse de concordances avec **9 vues spécialisées** :

- **Enrichissement automatique** : Métadonnées Edi-XX injectées
- **Visualisations interactives** : Graphiques, chronologies, nuages de mots
- **Comparaison de corpus** : Analyse sur 5 dimensions
- **Filtrage avancé** : Recherche multicritères
- **Export** : CSV, JSON, PNG

**Fonctionnalités** :
- Calcul de taux de correspondance métadonnées
- Analyse par domaine juridique, auteur, lieu
- Chronologies avec granularités variables
- Représentations type Gantt
- Word clouds basés sur fréquences

### Technologies

| Composant | Stack |
|-----------|-------|
| **Frontend** | React 18.2, Vite 5.0 |
| **Routing** | React Router DOM v6 |
| **Visualisation** | Recharts, D3.js |
| **i18n** | react-i18next (FR/EN) |
| **Tests** | Vitest + React Testing Library |
| **Styling** | CSS Modules |
| **Déploiement** | Vercel (CI/CD automatique) |

### Statut qualité

- ✅ **100% tests UI** : 93/93 composants testés
- ✅ **70% tests vues** : 64/91 composants testés
- ✅ **Production** : Déployé sur Vercel avec CDN global
- ✅ **Bilingue** : Interface FR/EN complète

### Installation locale

```bash
git clone https://github.com/TitouanCiSaMe/canon-law-toolkit.git
cd canon-law-toolkit
npm install
npm run dev
```

**Accès** : http://localhost:5173

---

## 📚 Ressources

### Plateformes CiSaMe

- **Canon-Law-Toolkit** (MODULE 9) : https://cisame.vercel.app
- **Repository GitHub** : https://github.com/TitouanCiSaMe/canon-law-toolkit

### Outils externes

- **eScriptorium** : https://escriptorium.readthedocs.io/
- **Kraken HTR** : https://kraken.re/
- **TreeTagger** : https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/
- **NoSketch-Engine** : https://nlp.fi.muni.cz/trac/noske
- **Heurist** : https://heuristnetwork.org/
- **PyCollatinus** : https://github.com/PonteIneptique/collatinus-python
- **Du Cange** : http://ducange.enc.sorbonne.fr/

---

## 📧 Contact

**Projet** : CiSaMe - Université de Strasbourg
**Portée** : Manuscrits juridiques médiévaux (droit canonique et civil)
**Période** : Moyen Âge

---

*Dernière mise à jour : Janvier 2026*
