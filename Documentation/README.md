# Documentation Projet CiSaMe

Ce dossier contient la documentation technique et les fichiers de référence du projet CiSaMe.

## 📚 Fichiers de Documentation

### Analyses et Schémas

#### **ANALYSE_SCHEMAS_DOCUMENTATION.md**
Analyse détaillée de la base de données Heurist (hdb_cisame_misha)
- Structure complète de la base
- 9 entités prévues vs 6 créées
- Relations entre entités
- 5,768 records, ~150 éditions
- Identification des entités manquantes
- Recommandations d'amélioration

#### **ANALYSE_SCHEMAS_MODULES.md**
Documentation des schémas de modules (ancienne version de la Vue_Ensemble)
- Archive de l'analyse des schémas modules
- Référence historique

#### **DOCUMENTATION_PAGETOPAGE_SCHEMA.md**
Documentation du MODULE 6 - PAGEtopage
- Enrichissement linguistique détaillé
- TreeTagger pour lemmatisation et POS-tagging
- Export formats (texte_clean.txt, corpus_vertical.txt)
- Architecture technique

### Guides et Procédures

#### **README_MANUSCRIPT_DOWNLOADER.md**
Guide d'utilisation du script de téléchargement de manuscrits
- Module 1 : Téléchargement d'images
- Méthodes IIIF
- Configuration et usage

#### **NoSKetch_Unistra.txt**
Informations de connexion et commandes NoSketch-Engine
- Connexion SSH serveur Unistra
- Commandes SCP pour export
- Module 7 : Déploiement NoSketch

### Données de Référence

#### **liste_manuscrits.csv**
Liste complète des manuscrits du corpus CiSaMe
- 317 manuscrits juridiques médiévaux
- Métadonnées : cote, bibliothèque, date, etc.
- Référence pour MODULE 1

#### **Liste MSS juridiques.docx**
Document Word original de la liste des manuscrits
- Version source avant extraction CSV
- Contient annotations et notes supplémentaires

---

## 🔗 Liens vers la Documentation Principale

- **Modules Projet** : [`/Modules_projet/`](../Modules_projet/)
- **Vue d'Ensemble** : [`/Modules_projet/Vue_Ensemble/`](../Modules_projet/Vue_Ensemble/)
- **Schéma Principal** : [`flowchart-pipeline-complet-integre.mmd`](../Modules_projet/Vue_Ensemble/flowchart-pipeline-complet-integre.mmd)

---

## 📊 Structure du Projet

```
CiSaMe/
├── Documentation/           # ← Vous êtes ici
│   ├── Analyses techniques
│   ├── Guides utilisateur
│   └── Données de référence
├── Modules_projet/         # Schémas et doc des 8 modules
│   ├── Module_1/           # Téléchargement Images
│   ├── Module_2/           # OCR & Reconnaissance
│   ├── Module_3/           # Segmentation
│   ├── Module_4/           # Corrections
│   ├── Module_5/           # Nettoyage Oxygène
│   ├── Module_6_PAGEtopage/    # Enrichissement TreeTagger
│   ├── Module_7_NoSketch_Engine/   # Concordancier
│   ├── Module_8_Diffusion_Donnees/ # Diffusion Nakala/Seafile
│   ├── Module_Metadonnees/     # Base Heurist
│   ├── Decret_Gratien/         # Pipeline parallèle
│   └── Vue_Ensemble/           # Schéma global
├── PAGEtopage/             # Code MODULE 6
├── latin_analyzer/         # Code MODULE 5B (futur)
├── canon-law-toolkit/      # Outils droit canonique
└── download_images.py      # Script MODULE 1
```

---

## 🔄 Historique

**Création** : 10 décembre 2024

Ce dossier a été créé pour centraliser toute la documentation technique du projet, séparant ainsi les fichiers de référence des schémas de modules opérationnels.

---

## 📧 Contact

**Projet** : CiSaMe - Université de Strasbourg
**Corpus** : Manuscrits juridiques médiévaux (droit canonique et civil)
**Période** : Moyen Âge
