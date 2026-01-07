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

#### **TUTORIEL_FUSION_EXPORT_NOSKETCH.txt**
Tutoriel complet pour débutants en ligne de commande
- Fusion des fichiers verticaux en un corpus unique
- Export vers le serveur NoSketch-Engine via SCP
- Compilation et mise en ligne du corpus
- Compatible Mac/Linux avec explications pas à pas
- Module 7 : Pipeline complet d'export NoSketch

#### **Guide_Kraken_HTR_Mac.txt**
Guide d'installation et d'utilisation de Kraken HTR sur Mac
- Procédures d'installation
- Configuration pour la transcription automatique
- Module 2 : OCR & Reconnaissance

#### **Fine_tuning_transcription.sh**
Script shell pour le fine-tuning des modèles de transcription
- Entraînement des modèles Kraken
- Module 2 : OCR & Reconnaissance

#### **Fine_tuning_segmentation.sh**
Script shell pour le fine-tuning des modèles de segmentation
- Entraînement des modèles de segmentation de lignes
- Module 3 : Segmentation

#### **NoSKetch_Unistra.txt**
Informations de connexion et commandes NoSketch-Engine
- Connexion SSH serveur Unistra
- Commandes SCP pour export
- Module 7 : Déploiement NoSketch

#### **Scripts Nakala** → [`/Nakala/`](../Nakala/)
Scripts Python pour l'export vers Nakala (MODULE 8)
- `validate_export.py` : Validation cohérence des données
- `prepare_nakala_export.py` : Préparation structure Libre/Non_libre
- `upload_nakala.py` : Upload via Heimdall
- `add_nakala_links.py` : Enrichissement URLs verticaux
- Documentation complète : [`Nakala/README.md`](../Nakala/README.md)

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

#### **Apport.docx**
Document détaillant les apports et contributions au projet
- Notes de développement
- Évolutions et améliorations

### Scripts et Utilitaires

> **📦 Script de fusion déplacé** : Le script de fusion des fichiers verticaux est maintenant dans [`PAGEtopage/fusion_vertical.py`](../PAGEtopage/fusion_vertical.py) pour une meilleure organisation du workflow PAGEtopage → NoSketch-Engine.

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
├── Modules_projet/         # Schémas et doc des 9 modules
│   ├── Module_1/           # Téléchargement Images
│   ├── Module_2/           # OCR & Reconnaissance
│   ├── Module_3/           # Segmentation
│   ├── Module_4/           # Corrections
│   ├── Module_5/           # Nettoyage Oxygène
│   ├── Module_6_PAGEtopage/    # Enrichissement TreeTagger
│   ├── Module_7_NoSketch_Engine/   # Concordancier
│   ├── Module_8_Diffusion_Donnees/ # Diffusion Nakala/Seafile
│   ├── Module_9_Visualisation_Requetes/ # Visualisation & Générateur CQL
│   ├── Module_Metadonnees/     # Base Heurist
│   ├── Decret_Gratien/         # Pipeline parallèle
│   └── Vue_Ensemble/           # Schéma global
├── PAGEtopage/             # Code MODULE 6
├── Nakala/                 # Scripts MODULE 8 (export Nakala/Seafile)
├── latin_analyzer/         # Code MODULE 5B (futur)
├── canon-law-toolkit/      # ⚠️ MODULE 9 (En développement - dossier vide)
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
