# Modules CiSaMe - Organisation du projet

Ce dossier contient l'ensemble des modules du projet **CiSaMe** (Corpus informatisé des Sources de l'Ancien droit Médiéval et moderne), ainsi que leurs schémas de workflow et documentations détaillées.

## 📋 Vue d'ensemble du projet

Le projet CiSaMe vise à constituer un corpus numérique de manuscrits juridiques médiévaux pour l'Université de Strasbourg, en assurant leur numérisation, enrichissement linguistique, et diffusion scientifique.

## 📂 Structure du dossier

### 🔹 Modules opérationnels

#### [`Module_1/`](./Module_1/)
**Téléchargement des images de manuscrits**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module1.mmd` : Schéma du workflow de téléchargement
  - `flowchart-module1.png` : Image du schéma
  - `MODULE1_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Téléchargement des images depuis diverses sources (IIIF, PDF, Hexa, Tuiles) pour 317 manuscrits du corpus

#### [`Module_2/`](./Module_2/)
**Méthodes de téléchargement**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module2.mmd` : Schéma du workflow de téléchargement
  - `flowchart-module2.png` : Image du schéma
  - `MODULE2_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Différentes méthodes d'acquisition d'images (IIIF, PDF, Hexadécimale, Tuiles, Manuel)
- **Script principal** : `Modules_projet/Module_1/download_images.py`

#### [`Module_3/`](./Module_3/)
**Récupération d'éditions de manuscrits**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module3.mmd` : Schéma du workflow d'acquisition
  - `flowchart-module3.png` : Image du schéma
  - `MODULE3_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Acquisition et catégorisation des éditions selon les droits (libre/restreint/secret)
- **Critères** : Libre = auteur mort +70 ans, Restreint = -70 ans, Secret = jamais publié

#### [`Module_4/`](./Module_4/)
**Traitement eScriptorium (Segmentation et Transcription)**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module4.mmd` : Schéma du workflow de traitement
  - `flowchart-module4.png` : Image du schéma
  - `MODULE4_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Segmentation et transcription HTR/OCR via eScriptorium avec entraînement sur HPC
- **Tutoriels** : [EN](https://escriptorium.readthedocs.io/en/latest/) | [FR](https://lectaurep.hypotheses.org/documentation/prendre-en-main-escriptorium)
- **Scripts HPC** : Disponibles dans `Documentation/`

#### [`Module_5/`](./Module_5/)
**Nettoyage Post-eScriptorium**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module5.mmd` : Schéma du workflow de nettoyage
  - `flowchart-module5.png` : Image du schéma
  - `MODULE5_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Nettoyage des fichiers XML PAGE avec Oxygène (XPath + Regex)
- **Outil** : [Oxygène XML Editor](https://www.oxygenxml.com/) | [Licence d'essai](https://www.oxygenxml.com/xml_editor/register.html?p=editor)

### 🔸 Modules en développement

#### [`Module_6_PAGEtopage/`](./Module_6_PAGEtopage/)
**Enrichissement linguistique avec PAGEtopage**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module6-pagetopage.mmd` : Schéma du pipeline PAGEtopage
  - `flowchart-module6-pagetopage.png` : Image du schéma
  - `MODULE6_PAGETOPAGE_DOCUMENTATION.md` : Documentation détaillée (Extract → Enrich → Export → Re-enrich)
- **Description** : Pipeline d'enrichissement linguistique en 4 étapes (3 + correction optionnelle) utilisant TreeTagger (installation automatique) pour lemmatisation et POS-tagging (Latin/Français)
- **Technologies** : Python 3.10+, TreeTagger, treetaggerwrapper, PyYAML
- **Formats de sortie** : 4 formats (scholarly, clean, diplomatic, annotated)
- **⚠️ Note** : N'utilise **pas** ce module pour le Décret de Gratien (pipeline spécifique)

#### [`Module_7_NoSketch_Engine/`](./Module_7_NoSketch_Engine/)
**Pipeline NoSketch-Engine (Corpus interrogeables)**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module7-nosketch.mmd` : Schéma du pipeline principal
  - `flowchart-module7-nosketch.png` : Image du schéma
  - `MODULE_NOSKETCH_ENGINE_DOCUMENTATION.md` : Documentation complète du pipeline
- **Description** : Création de corpus interrogeables à partir des fichiers verticaux (.vertical.txt) produits par MODULE 6
- **Workflow** : Fusion → Test → Export → Compilation → Mise en service
- **Outils** : `pagetopage fusion` (PAGEtopage/fusion_vertical.py), SCP, compilation serveur
- **Fonctionnalités** : Concordances, collocations, recherche par lemme/forme/POS

#### [`Module_8_Diffusion_Donnees/`](./Module_8_Diffusion_Donnees/)
**Diffusion finale des données textuelles**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module8-diffusion.mmd` : Schéma de décision de diffusion
  - `flowchart-module8-diffusion.png` : Image du schéma
  - `MODULE_DONNEES_TEXTUELLES_DOCUMENTATION.md` : Documentation complète
- **Description** : Gestion de la diffusion finale des corpus enrichis (avec/sans images, libre/restreint)
- **Destinations** :
  - **Nakala** : Données libres (Algo Hécate + connecteur Nakala)
  - **Seafile** : Données restreintes (cloud universitaire)

#### [`Module_9_Visualisation_Requetes/`](./Module_9_Visualisation_Requetes/)
**Visualisation et Générateur de Requêtes**
- **Statut** : ✅ Production
- **Contenu** :
  - `flowchart-module9-visualisation.mmd` : Schéma du pipeline de visualisation
  - `flowchart-module9-visualisation.png` : Image du schéma
  - `MODULE9_VISUALISATION_DOCUMENTATION.md` : Documentation complète
- **Description** : Plateforme web d'analyse pour NoSketch-Engine (canon-law-toolkit)
- **Fonctionnalités** :
  - **Query Generator** : Générateur de requêtes CQL (4 types de recherche, 96 variantes orthographiques)
  - **Concordance Analyzer** : 9 vues d'analyse, comparaison de 2 corpus
- **Technologies** : React 18.2, Vite 5.0, Recharts, D3.js, react-i18next
- **Repository** : [canon-law-toolkit](https://github.com/TitouanCiSaMe/canon-law-toolkit)

### 🔸 Modules transversaux

#### [`Module_Metadonnees/`](./Module_Metadonnees/)
**Extraction et gestion des métadonnées (Transversal)**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-metadonnees.mmd` : Schéma d'extraction vers Heurist
  - `flowchart-metadonnees.png` : Image du schéma
  - `MODULE_METADONNEES_DOCUMENTATION.md` : Documentation de la structure Heurist
- **Description** : Extraction des métadonnées des fiches manuscrits vers la base Heurist (3 tables : Auteurs, Oeuvres, Éditions). Alimente le config.yaml du MODULE 6.
- **Base de données** : Heurist (hdb_cisame_misha) - 5,768 records, 129 éditions
- **Rôle** : Fournit les métadonnées bibliographiques pour l'enrichissement (MODULE 6)

### 🔹 Pipelines spécifiques

#### [`Decret_Gratien/`](./Decret_Gratien/)
**Pipeline spécifique au Décret de Gratien**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-decret-gratien.mmd` : Schéma du workflow dédié
  - `flowchart-decret-gratien.png` : Image du schéma
  - `DECRET_GRATIEN_DOCUMENTATION.md` : Documentation complète du corpus
- **Description** : Pipeline adapté au format spécifique du Décret de Gratien
- **Statistiques** : 4 149 fichiers .txt, ~4 000 canons, ~5 Mo
- **Structure** : Premiere_partie (D.1-D.101), Deuxieme_partie (C.1-C.36/q.X), Troisieme_partie (D.1-D.5)
- **⚠️ Important** : Ce corpus **ne passe pas** par le MODULE 6 (PAGEtopage), il possède son propre format .txt et est déjà sur NoSketch-Engine

### 📊 Vues d'ensemble

#### [`Vue_Ensemble/`](./Vue_Ensemble/)
**Schémas récapitulatifs et analyses**
- **Contenu** :
  - `flowchart-pipeline-complet-integre.mmd` : Schéma complet amélioré de tous les modules
  - `flowchart-pipeline-complet-integre.png` : Image du schéma principal
  - `FLOWCHARTS_INDEX.md` : Index de tous les schémas du projet
  - `README_VUE_ENSEMBLE.md` : Documentation de la vue d'ensemble
- **Description** : Documentation globale, schémas récapitulatifs et analyses approfondies du projet

## 🔗 Pipeline complet intégré

```
MODULE 1 : Téléchargement images
         ↓
MODULE 2 : OCR (extraction texte)
         ↓
MODULE 3 : Segmentation
         ↓
MODULE 4 : Corrections
         ↓
MODULE 5 : Export
         ↓
MODULE 6 : PAGEtopage (Enrichissement linguistique)
         │  ← [Module Métadonnées : Heurist → config.yaml]
         ↓
    (3 formats produits : clean, diplomatic, annotated.vertical.txt)
         ↓
    ┌────┴──────┐
    ↓           ↓
MODULE 7     MODULE 8
NoSketch     Diffusion
Engine       Données
(.vertical)  (Nakala/Seafile)
    ↓           ↓
Corpus       Archives
interrogeable publiques/privées
    ↓
MODULE 9
Visualisation
& Requêtes
(canon-law-toolkit)
```

**Pipeline parallèle** : Décret de Gratien (workflow spécifique, déjà sur NoSketch-Engine)

## 🛠️ Technologies principales

- **Langages** : Python 3.10+, Shell
- **OCR** : Tesseract, Kraken
- **Enrichissement** : TreeTagger (lemmatisation, POS-tagging)
- **Base de données** : Heurist
- **Stockage** : Seafile (privé), Nakala (public)
- **Corpus query** : NoSketch-Engine
- **Formats** : XML, JSON, YAML, Vertical (NoSketch)
- **Diagrammes** : Mermaid

## 📊 Corpus

- **Manuscrits** : 317 manuscrits juridiques médiévaux
- **Records Heurist** : 5,768 records
- **Éditions documentées** : 129 éditions
- **Langues** : Latin, Français
- **Période** : Moyen Âge (droit canonique et civil)

## 📖 Comment utiliser cette documentation

### Pour comprendre un module spécifique
1. Accédez au dossier du module (ex: `Module_6_PAGEtopage/`)
2. Consultez le schéma `.mmd` ou `.mermaid` (visualisable avec un viewer Mermaid)
3. Lisez la documentation `.md` pour les détails d'implémentation

### Pour une vue globale du projet
1. Consultez le dossier [`Vue_Ensemble/`](./Vue_Ensemble/)
2. Commencez par `flowchart-overview.mmd` pour la vue générale
3. Lisez `ANALYSE_SCHEMAS_DOCUMENTATION.md` pour l'analyse approfondie

### Pour comprendre les interconnexions
1. Consultez `flowchart-complete-improved.mmd` dans `Vue_Ensemble/`
2. Lisez les sections "Relation avec les autres modules" dans chaque documentation

## 🔍 Cas particuliers à noter

### Décret de Gratien
- **Pipeline séparé** : Ne suit pas le workflow général
- **Pas de MODULE 6** : Format .txt adapté déjà créé
- **Déjà sur NoSketch** : Corpus opérationnel

### Métadonnées PAGEtopage
- **Processus manuel** : Consultation Heurist → Copie dans config.yaml
- **Pas d'automatisation** : Transfert manuel des métadonnées

### Données libres vs restreintes
- **Libres avec images** → Nakala (via Algo Hécate)
- **Libres sans images** → Nakala (texte seul)
- **Restreintes** → Seafile (privé université)

## 🚀 Statut global du projet

| Module | Statut | Priorité |
|--------|--------|----------|
| **MODULE 1** : Téléchargement images | ✅ Opérationnel | Complété |
| **MODULE 2** : OCR | ✅ Opérationnel | Complété |
| **MODULE 3** : Segmentation | ✅ Opérationnel | Complété |
| **MODULE 4** : Corrections | ✅ Opérationnel | Complété |
| **MODULE 5** : Export | ✅ Opérationnel | Complété |
| **MODULE 6** : PAGEtopage (Enrichissement) | ✅ Opérationnel | Complété |
| **MODULE 7** : NoSketch-Engine | ✅ Opérationnel | Complété |
| **MODULE 8** : Diffusion Données | ✅ Opérationnel | Complété |
| **MODULE 9** : Visualisation & Requêtes | ✅ Production | Complété |
| **Transversal** : Métadonnées (Heurist) | ✅ Opérationnel | Complété |
| **Parallèle** : Décret de Gratien | ✅ Opérationnel | Complété |

## 📝 Maintenance

Pour mettre à jour cette documentation :
1. Placez les nouveaux schémas `.mmd` ou `.mermaid` dans le dossier du module concerné
2. Créez ou mettez à jour la documentation `.md` associée
3. Mettez à jour ce README si nécessaire
4. Committez avec un message descriptif

## 📧 Contact

**Projet** : CiSaMe - Université de Strasbourg
**Portée** : Corpus juridiques médiévaux

---

*Dernière mise à jour : 26 décembre 2025*
