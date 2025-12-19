# CiSaMe - Corpus informatisé des Sources de l'Ancien droit Médiéval et moderne

Pipeline de numérisation, transcription et enrichissement linguistique de manuscrits juridiques médiévaux (droit canonique et civil).

**Université de Strasbourg** | 317 manuscrits | ~150 éditions

---

## 📋 Vue d'ensemble

Pipeline automatisé de traitement en 9 modules pour transformer des images de manuscrits en corpus interrogeables :

```
Images → OCR/HTR → Segmentation → Corrections → Nettoyage XML
  → Enrichissement linguistique → Corpus interrogeable + Diffusion
```

**Résultat** : Corpus annotés (lemmes, POS tags) accessibles via concordancier web + archives scientifiques (Nakala/Seafile)

---

## 🚀 Démarrage rapide

### MODULE 1 : Télécharger des images

```bash
python download_images.py --iiif <url_manifest>
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
├── download_images.py           # MODULE 1 : Téléchargement images (IIIF, PDF)
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
│   ├── Module_2/                # Méthodes acquisition (IIIF/PDF/Hexa/Tuiles)
│   ├── Module_3/                # Récupération éditions (libre/restreint)
│   ├── Module_4/                # eScriptorium (segmentation/transcription HTR)
│   ├── Module_5/                # Nettoyage Oxygène XML (XPath + Regex)
│   ├── Module_6_PAGEtopage/     # Enrichissement linguistique
│   ├── Module_7_NoSketch_Engine/# Concordancier web
│   ├── Module_8_Diffusion_Donnees/ # Nakala (libre) / Seafile (restreint)
│   ├── Module_9_Visualisation_Requetes/ # Query Generator + Analyzer
│   ├── Module_Metadonnees/      # Base Heurist (5768 records, transversal)
│   ├── Decret_Gratien/          # Pipeline parallèle (4149 fichiers)
│   └── Vue_Ensemble/            # Schéma global intégré
├── Documentation/               # Guides techniques et scripts
│   ├── Fine_tuning_*.sh         # Scripts HPC entraînement Kraken
│   ├── liste_manuscrits.csv     # Corpus 317 manuscrits
│   └── Guide_Kraken_HTR_Mac.txt # Installation Kraken
└── canon-law-toolkit/           # MODULE 9 (en développement)
```

---

## 📖 Documentation

| Document | Contenu |
|----------|---------|
| **[Modules_projet/README.md](Modules_projet/README.md)** | Vue d'ensemble des 9 modules |
| **[Modules_projet/Vue_Ensemble/](Modules_projet/Vue_Ensemble/)** | Schéma global intégré du projet |
| **[PAGEtopage/README.md](PAGEtopage/README.md)** | Guide enrichissement linguistique (MODULE 6) |
| **[latin_analyzer/README.md](latin_analyzer/README.md)** | Validation automatique textes latins |
| **[Modeles/README.md](Modeles/README.md)** | Modèles Kraken segmentation/transcription |
| **[Documentation/README.md](Documentation/README.md)** | Guides techniques et scripts HPC |

---

## 🛠️ Technologies

| Composant | Technologie |
|-----------|-------------|
| **Langages** | Python 3.10+, Shell, YAML |
| **OCR/HTR** | eScriptorium, Kraken (HPC Unistra) |
| **Enrichissement** | TreeTagger (lemmatisation auto-installée) |
| **Validation latin** | PyCollatinus + Du Cange (100k mots médiévaux) |
| **Base de données** | Heurist (métadonnées bibliographiques) |
| **Stockage** | Seafile (privé), Nakala (public) |
| **Concordancier** | NoSketch-Engine (requêtes CQL) |
| **Visualisation** | React 18, D3.js, Recharts (MODULE 9) |
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
| **MODULE 8** | ✅ Opérationnel | Diffusion Nakala/Seafile |
| **MODULE 9** | 🚧 En développement | Canon-Law-Toolkit (Query Generator + Analyzer) |
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

1. **Télécharger images** (MODULE 1) : `python download_images.py --iiif <url>`
2. **Transcrire** (MODULE 4) : Importer dans eScriptorium, appliquer modèles Kraken
3. **Nettoyer** (MODULE 5) : Oxygène XML avec XPath + Regex
4. **Enrichir** (MODULE 6) : `python -m PAGEtopage run --input ./xml/ --output ./output/ --config config.yaml`
5. **Diffuser** :
   - NoSketch-Engine (MODULE 7) : Fusion + compilation corpus
   - Nakala/Seafile (MODULE 8) : Archives scientifiques
6. **Analyser** (MODULE 9) : Query Generator + visualisations

---

## 📚 Ressources externes

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

*Dernière mise à jour : Décembre 2025*
