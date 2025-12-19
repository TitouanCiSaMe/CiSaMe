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
  - `MODULE1_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Téléchargement des images depuis diverses sources (IIIF, PDF, Hexa, Tuiles) pour 317 manuscrits du corpus

#### [`Module_2/`](./Module_2/)
**Méthodes de téléchargement**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module2.mmd` : Schéma du workflow de téléchargement
  - `MODULE2_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Différentes méthodes d'acquisition d'images (IIIF, PDF, Hexadécimale, Tuiles, Manuel)
- **Script principal** : `download_images.py` (racine du repo)

#### [`Module_3/`](./Module_3/)
**Récupération d'éditions de manuscrits**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module3.mmd` : Schéma du workflow d'acquisition
  - `MODULE3_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Acquisition et catégorisation des éditions selon les droits (libre/restreint/secret)
- **Critères** : Libre = auteur mort +70 ans, Restreint = -70 ans, Secret = jamais publié

#### [`Module_4/`](./Module_4/)
**Traitement eScriptorium (Segmentation et Transcription)**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module4.mmd` : Schéma du workflow de traitement
  - `MODULE4_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Segmentation et transcription HTR/OCR via eScriptorium avec entraînement sur HPC
- **Tutoriels** : [EN](https://escriptorium.readthedocs.io/en/latest/) | [FR](https://lectaurep.hypotheses.org/documentation/prendre-en-main-escriptorium)
- **Scripts HPC** : Disponibles dans `Documentation/`

#### [`Module_5/`](./Module_5/)
**Nettoyage Post-eScriptorium**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module5.mmd` : Schéma du workflow de nettoyage
  - `MODULE5_DOCUMENTATION.md` : Documentation complète du module
- **Description** : Nettoyage des fichiers XML PAGE avec Oxygène (XPath + Regex)
- **Outil** : [Oxygène XML Editor](https://www.oxygenxml.com/) | [Licence d'essai](https://www.oxygenxml.com/xml_editor/register.html?p=editor)

### 🔸 Modules en développement

#### [`Module_6_PAGEtopage/`](./Module_6_PAGEtopage/)
**Enrichissement linguistique avec PAGEtopage**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module6-pagetopage.mmd` : Schéma du pipeline PAGEtopage
  - `MODULE6_PAGETOPAGE_DOCUMENTATION.md` : Documentation détaillée (Extract → Enrich → Export → Re-enrich)
- **Description** : Pipeline d'enrichissement linguistique en 4 étapes (3 + correction optionnelle) utilisant TreeTagger (installation automatique) pour lemmatisation et POS-tagging (Latin/Français)
- **Technologies** : Python 3.10+, TreeTagger, treetaggerwrapper, PyYAML
- **Formats de sortie** : 4 formats (scholarly, clean, diplomatic, annotated)
- **⚠️ Note** : N'utilise **pas** ce module pour le Décret de Gratien (pipeline spécifique)

#### [`Module_7_NoSketch_Engine/`](./Module_7_NoSketch_Engine/)
**Pipeline NoSketch-Engine (Corpus interrogeables)**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `module_nosketch_engine.mermaid` : Schéma du pipeline principal
  - `module_nosketch_installation.mermaid` : Schéma d'installation de l'instance test
  - `MODULE_NOSKETCH_ENGINE_DOCUMENTATION.md` : Documentation complète du pipeline
- **Description** : Création de corpus interrogeables à partir des fichiers verticaux (.vertical.txt) produits par MODULE 6
- **Workflow** : Fusion → Test → Export → Compilation → Mise en service
- **Outils** : Fusion_txt_NoSketch.py, SCP, compilation serveur
- **Fonctionnalités** : Concordances, collocations, recherche par lemme/forme/POS

#### [`Module_8_Diffusion_Donnees/`](./Module_8_Diffusion_Donnees/)
**Diffusion finale des données textuelles**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `module_donnees_textuelles.mermaid` : Schéma de décision de diffusion
  - `MODULE_DONNEES_TEXTUELLES_DOCUMENTATION.md` : Documentation complète
- **Description** : Gestion de la diffusion finale des corpus enrichis (avec/sans images, libre/restreint)
- **Destinations** :
  - **Nakala** : Données libres (Algo Hécate + connecteur Nakala)
  - **Seafile** : Données restreintes (cloud universitaire)

### 🔸 Modules transversaux

#### [`Module_Metadonnees/`](./Module_Metadonnees/)
**Extraction et gestion des métadonnées (Transversal)**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `module_fiches_metadonnees.mermaid` : Schéma d'extraction vers Heurist
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
  - `DECRET_GRATIEN_DOCUMENTATION.md` : Documentation complète du corpus
- **Description** : Pipeline adapté au format spécifique du Décret de Gratien
- **Statistiques** : 4 149 fichiers .txt, ~4 000 canons, ~5 Mo
- **Structure** : Premiere_partie (D.1-D.101), Deuxieme_partie (C.1-C.36/q.X), Troisieme_partie (D.1-D.5)
- **⚠️ Important** : Ce corpus **ne passe pas** par le MODULE 6 (PAGEtopage), il possède son propre format .txt et est déjà sur NoSketch-Engine

### 📊 Vues d'ensemble

#### [`Vue_Ensemble/`](./Vue_Ensemble/)
**Schémas récapitulatifs et analyses**
- **Contenu** :
  - `flowchart-complete-improved.mmd` : Schéma complet amélioré de tous les modules
  - `flowchart-overview.mmd` : Vue d'ensemble du projet
  - `flowchart-simple.mmd` : Vue simplifiée du workflow
  - `FLOWCHARTS_INDEX.md` : Index de tous les schémas du projet
  - `ANALYSE_SCHEMAS_DOCUMENTATION.md` : Analyse détaillée de la base Heurist (1,152 lignes)
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

*Dernière mise à jour : 12 décembre 2025*
