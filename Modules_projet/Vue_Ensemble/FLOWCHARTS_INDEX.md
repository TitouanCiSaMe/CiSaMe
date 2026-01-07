# Index des Schémas - Projet CiSaMe

## 📋 Vue d'ensemble

Ce document référence tous les schémas Mermaid du projet CiSaMe, organisés par module et par fonction.

---

## 🌐 Vue d'Ensemble Complète

### 📌 [flowchart-pipeline-complet-integre.mmd](./flowchart-pipeline-complet-integre.mmd)
**SCHÉMA PRINCIPAL - Pipeline Complet Intégré**
**Niveau de détail:** ⭐⭐⭐ (Complet et synthétique)
**Usage recommandé:** Comprendre l'ensemble du projet

**Description:** Schéma complet et à jour montrant :
- Pipeline principal : Modules 1 à 8
- Module transversal : Métadonnées (Heurist)
- Pipeline parallèle : Décret de Gratien
- Décisions de diffusion : Avec/Sans images × Libre/Restreint
- Destinations : Nakala, Seafile, NoSketch-Engine

**Technologies clés mentionnées:**
- MODULE 5 : Oxygène XML Editor
- MODULE 6 : TreeTagger (lemmatisation, POS-tagging)
- MODULE 7 : NoSketch-Engine (concordancier)
- MODULE 8 : Connecteur Nakala, Seafile

**Idéal pour:**
- Présenter le projet dans son ensemble
- Comprendre les flux de données
- Former de nouveaux collaborateurs
- Documentation architecture globale

---

## 📦 Schémas par Module

### MODULE 1 - Téléchargement Images
**Fichier:** `Modules_projet/Module_1/flowchart-module1.mmd`
**Détail:** ⭐⭐⭐⭐

**Contenu:**
- Sources d'acquisition (IIIF, PDF, méthodes complexes)
- Formats supportés (JPG, PNG, TIF)
- Stockage sur Seafile

### MODULE 2 - OCR & Reconnaissance
**Fichier:** `Modules_projet/Module_2/flowchart-module2.mmd`
**Détail:** ⭐⭐⭐⭐⭐

**Contenu:**
- Méthodes de téléchargement détaillées
- IIIF (algorithme Manuscrit_Downloader)
- PDF direct avec extraction
- Méthodes complexes (manuelle, hexadécimale, tuiles)
- Comparaison qualité

### MODULE 3 - Segmentation & Structuration
**Fichier:** `Modules_projet/Module_3/flowchart-module3.mmd`
**Détail:** ⭐⭐⭐⭐

**Contenu:**
- Sources d'acquisition des éditions
- Processus de numérisation BNU
- Catégorisation temporelle et juridique
- Statistiques : 30% libre, 68% restreint, 2% secret
- Stockage HPC

### MODULE 4 - Corrections & Validation
**Fichier:** `Modules_projet/Module_4/flowchart-module4.mmd`
**Détail:** ⭐⭐⭐⭐

**Contenu:**
- Traitement eScriptorium (transcription, HTR)
- Modèles spécialisés
- Workflow de validation
- Export XML PAGE

### MODULE 5 - Nettoyage Post-eScriptorium
**Fichier:** `Modules_projet/Module_5/flowchart-module5.mmd`
**Détail:** ⭐⭐⭐⭐⭐

**Contenu:**
- **Oxygène XML Editor** : Outil principal
- Support layouts : 1, 2 ou 4 régions Main
- XPath pour ciblage précis
- Regex spécifiques au texte médiéval
- Procédure détaillée pas à pas
- Format : NOMÉDITION_ID.xml
- Temps : ~20 min par œuvre

### MODULE 6 - PAGEtopage (Enrichissement Linguistique)
**Fichier:** `Modules_projet/Module_6_PAGEtopage/flowchart-module6-pagetopage.mmd`
**Détail:** ⭐⭐⭐⭐⭐
**Statut:** 🚧 En développement

**Contenu:**
- Étape 1 - Extract : XML PAGE → JSON
- Étape 2 - Enrich : **TreeTagger** (lemmatisation, POS-tagging, installation automatique)
- Étape 3 - Export : 4 formats
  - scholarly (format académique recommandé avec en-tête complet)
  - clean (texte brut lisible)
  - diplomatic (annotations inline)
  - annotated (format tabulaire)
  - corpus_vertical.txt (Mot | POS | Lemme)
- Étape 4 - Re-enrich (optionnel) : Correction manuelle + régénération vertical
- Alimenté par config.yaml (métadonnées Heurist)
- Technologies : Python 3.10+, TreeTagger, treetaggerwrapper, PyYAML

### MODULE 7 - NoSketch-Engine
**Fichier:** `Modules_projet/Module_7_NoSketch_Engine/flowchart-module7-nosketch.mmd`
**Détail:** ⭐⭐⭐⭐

**Contenu:**
- Installation instance test locale
- Fusion des fichiers corpus_vertical.txt
- Vérification viabilité
- Déploiement serveur HPC via SCP
- Compilation et mise en service
- Sortie : Concordancier web accessible

### MODULE 8 - Diffusion Données Textuelles
**Fichier:** `Modules_projet/Module_8_Diffusion_Donnees/flowchart-module8-diffusion.md`
**Scripts:** `/Nakala/` (validate, prepare, upload, add_links)
**Détail:** ⭐⭐⭐⭐⭐

**Contenu:**
- Workflow en 4 étapes avec scripts Python
- Étape 1 : `validate_export.py` - Validation cohérence
- Étape 2 : `prepare_nakala_export.py` - Structure Libre/Non_libre
- Étape 3 : `upload_nakala.py` - Upload via Heimdall
- Étape 4 : `add_nakala_links.py` - Enrichissement URLs
- **Nakala** : Données libres (DOI, archivage pérenne)
- **Seafile** : Données restreintes (accès contrôlé)

### MODULE 9 - Visualisation et Générateur de Requêtes
**Fichier:** `Modules_projet/Module_9_Visualisation_Requetes/flowchart-module9-visualisation.mmd`
**Détail:** ⭐⭐⭐⭐⭐
**Statut:** ✅ Production

**Contenu:**
- **Query Generator** : Générateur de requêtes CQL pour NoSketch Engine
  - 4 types de recherche : Proximité, Variations orthographiques médiévales, Sémantique, Proximité+Variations
  - 96 variantes orthographiques possibles (ae/e, v/u, j/i, ti/ci)
  - Configuration interactive et prévisualisation temps réel
  - Export : copier-coller ou lancement direct sur NoSketch
- **Concordance Analyzer** : Analyse approfondie de concordances
  - 9 vues d'analyse spécialisées
  - Enrichissement automatique métadonnées Edi-XX
  - Comparaison de 2 corpus (5 dimensions)
  - Persistance automatique sessionStorage
- **Technologies** : React 18.2, Vite 5.0, Recharts, D3.js, react-i18next
- **Export** : CSV, JSON, PNG
- **Tests** : 157/184 ✅ (85%)
- **Repository** : [canon-law-toolkit](https://github.com/TitouanCiSaMe/canon-law-toolkit)

### MODULE MÉTADONNÉES (Transversal)
**Fichier:** `Modules_projet/Module_Metadonnees/flowchart-metadonnees.mmd`
**Détail:** ⭐⭐⭐⭐

**Contenu:**
- Base de données **Heurist**
- 3 tables relationnelles :
  - Auteurs (ID, nom, alias)
  - Oeuvres (ID, titre, auteur, date, lieu, type)
  - Éditions (ID, titre, éditeur, collection, pagination)
- Liens via clés étrangères
- 5,768 records, ~150 éditions
- Interface web pour consultation
- Export : JSON, CSV, XML

### MODULE DÉCRET DE GRATIEN (Pipeline Parallèle)
**Fichier:** `Modules_projet/Decret_Gratien/flowchart-decret-gratien.mmd`
**Détail:** ⭐⭐⭐⭐

**Contenu:**
- Workflow spécifique **NE PASSANT PAS par MODULE 6**
- Sources : Ochoa et Diez (allégations) + Friedberg (édition)
- Extraction algorithmique
- Enrichissement manuel
- Statistiques : 4149 fichiers, 5 Mo, ~4000 canons
- Format ID : Grat_XXXX
- Corpus déjà opérationnel sur NoSketch-Engine

---

## 📊 Navigation Rapide

### Par Niveau de Détail
- **Vue Ensemble** : `flowchart-pipeline-complet-integre.mmd`
- **Modules Détaillés** : Voir chaque module individuellement

### Par Fonctionnalité
- **Acquisition** : Modules 1, 2, 3
- **Traitement** : Modules 4, 5
- **Enrichissement** : Module 6, Métadonnées
- **Diffusion** : Modules 7, 8
- **Visualisation/Analyse** : Module 9
- **Spécifique** : Décret de Gratien

### Par Technologie
- **Oxygène XML** : Module 5
- **TreeTagger** : Module 6
- **NoSketch-Engine** : Module 7
- **Nakala/Seafile** : Module 8
- **React/Vite/Recharts/D3.js** : Module 9
- **Heurist** : Métadonnées

---

## 🔄 Dernière Mise à Jour

**Date:** Janvier 2026

**Changements récents:**
- ✅ Refonte Module 8 : Scripts dans `/Nakala/` avec workflow complet
- ✅ Ajout Module 9 : Visualisation et Générateur de Requêtes (canon-law-toolkit)
- ✅ Refonte Module 5 : Oxygène XML Editor
- ✅ Migration Module 6 : CLTK → TreeTagger
- ✅ Reformatage Modules 7, Métadonnées
- ✅ Restructuration Décret de Gratien
- ✅ Mise à jour Vue Ensemble

---

## 📧 Support

**Projet:** CiSaMe - Université de Strasbourg
**Documentation complète:** [`/Documentation/`](../../Documentation/)
**Schéma principal:** `flowchart-pipeline-complet-integre.mmd`

---

*Pour comprendre l'architecture globale, consultez le [README Vue d'Ensemble](./README_VUE_ENSEMBLE.md)*
