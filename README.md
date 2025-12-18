# CiSaMe - Corpus informatisé des Sources de l'Ancien droit Médiéval et moderne

Pipeline de numérisation, transcription et enrichissement linguistique de manuscrits juridiques médiévaux.

**Université de Strasbourg** | Droit canonique et civil | Moyen Âge

## Vue d'ensemble

Pipeline de traitement en 9 modules :

```
Images → OCR → Segmentation → Corrections → Nettoyage
  → Enrichissement linguistique → Corpus interrogeable + Diffusion
```

**Corpus** : 317 manuscrits, ~150 éditions, 5768 records (Heurist)

## Structure du projet

```
CiSaMe/
├── Modules_projet/              # Documentation des 9 modules
│   ├── Module_1/                # Téléchargement images (IIIF, PDF, etc.)
│   ├── Module_2/                # OCR & Reconnaissance
│   ├── Module_3/                # Segmentation & Structuration
│   ├── Module_4/                # eScriptorium (HTR/OCR)
│   ├── Module_5/                # Nettoyage Oxygène XML
│   ├── Module_6_PAGEtopage/     # Enrichissement TreeTagger
│   ├── Module_7_NoSketch_Engine/# Concordancier
│   ├── Module_8_Diffusion_Donnees/ # Nakala/Seafile
│   ├── Module_9_Visualisation_Requetes/ # Query Generator + Analyzer
│   ├── Module_Metadonnees/      # Base Heurist (transversal)
│   ├── Decret_Gratien/          # Pipeline parallèle
│   └── Vue_Ensemble/            # Schéma global du projet
├── PAGEtopage/                  # Code MODULE 6 (enrichissement)
├── latin_analyzer/              # Analyseur morphologique latin
├── Modeles/                     # Modèles Kraken (.mlmodel)
├── Documentation/               # Guides techniques et scripts
└── download_images.py           # Script MODULE 1
```

## Documentation principale

| Document | Description |
|----------|-------------|
| [`Modules_projet/README.md`](Modules_projet/README.md) | Organisation complète des modules |
| [`Modules_projet/Vue_Ensemble/`](Modules_projet/Vue_Ensemble/) | Schéma global intégré |
| [`Documentation/README.md`](Documentation/README.md) | Guides techniques et scripts |
| [`PAGEtopage/README.md`](PAGEtopage/README.md) | Enrichissement linguistique (MODULE 6) |
| [`Modeles/README.md`](Modeles/README.md) | Modèles de segmentation/transcription |

## Démarrage rapide

### MODULE 1 : Télécharger des images de manuscrits

```bash
python download_images.py --iiif <url_manifest>
```

### MODULE 6 : Enrichissement linguistique

```bash
cd PAGEtopage
python pagetopage.py extract input.xml
python pagetopage.py enrich extracted.json config.yaml
python pagetopage.py export enriched.json --format scholarly
```

### MODULE 7 : Fusion pour NoSketch-Engine

```bash
cd PAGEtopage
python fusion_vertical.py dossier_corpus/ corpus_fusionne.vertical.txt
```

## Technologies

**Langages** : Python 3.10+, Shell
**OCR/HTR** : eScriptorium, Kraken
**Enrichissement** : TreeTagger (lemmatisation, POS-tagging)
**Base de données** : Heurist
**Stockage** : Seafile (privé), Nakala (public)
**Concordancier** : NoSketch-Engine
**Visualisation** : React, D3.js

## Statut des modules

| Module | Statut |
|--------|--------|
| MODULE 1-5, 7-9 | ✅ Opérationnel |
| MODULE 6 (PAGEtopage) | 🚧 En développement |
| Décret de Gratien | ✅ Opérationnel (pipeline parallèle) |

## Schéma global

Voir [`Modules_projet/Vue_Ensemble/flowchart-pipeline-complet-integre.mmd`](Modules_projet/Vue_Ensemble/flowchart-pipeline-complet-integre.mmd)

Visualisation : [Mermaid Live Editor](https://mermaid.live/)

## Ressources

- **eScriptorium** : https://escriptorium.readthedocs.io/
- **Kraken HTR** : https://kraken.re/
- **TreeTagger** : https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/
- **NoSketch-Engine** : https://nlp.fi.muni.cz/trac/noske
- **Heurist** : https://heuristnetwork.org/

---

*Dernière mise à jour : Décembre 2025*
