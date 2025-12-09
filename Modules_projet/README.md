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
**Numérisation et OCR**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module2.mmd` : Schéma du workflow OCR
- **Description** : Reconnaissance optique de caractères (Tesseract, Kraken) pour extraction du texte des images

#### [`Module_3/`](./Module_3/)
**Segmentation et structuration**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module3.mmd` : Schéma du workflow de segmentation
- **Description** : Découpage et structuration du texte brut en unités sémantiques

#### [`Module_4/`](./Module_4/)
**Corrections et consolidation**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module4.mmd` : Schéma du workflow de correction
- **Description** : Validation et correction manuelle/semi-automatique des textes extraits

#### [`Module_5/`](./Module_5/)
**Export et archivage**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `flowchart-module5.mmd` : Schéma du workflow d'export
- **Description** : Préparation des données pour archivage et diffusion

### 🔸 Modules en développement

#### [`Module_6_PAGEtopage/`](./Module_6_PAGEtopage/)
**Enrichissement linguistique avec PAGEtopage**
- **Statut** : 🚧 En développement
- **Contenu** :
  - `flowchart-module6-pagetopage.mmd` : Schéma du pipeline PAGEtopage
  - `MODULE6_PAGETOPAGE_DOCUMENTATION.md` : Documentation détaillée (Extract → Enrich → Export)
- **Description** : Pipeline d'enrichissement linguistique en 3 étapes utilisant CLTK pour lemmatisation et POS-tagging (Latin/Français)
- **Technologies** : Python 3.10+, CLTK, PyYAML, lxml
- **⚠️ Note** : N'utilise **pas** ce module pour le Décret de Gratien (pipeline spécifique)

### 🔸 Modules transversaux

#### [`Module_Donnees_Textuelles/`](./Module_Donnees_Textuelles/)
**Gestion de la diffusion des données**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `module_donnees_textuelles.mermaid` : Schéma de décision de diffusion
  - `MODULE_DONNEES_TEXTUELLES_DOCUMENTATION.md` : Documentation complète
- **Description** : Gestion de la diffusion finale des corpus (avec/sans images, libre/restreint)
- **Destinations** :
  - **Nakala** : Données libres (Algo Hécate + connecteur Nakala)
  - **Seafile** : Données restreintes (cloud universitaire)

#### [`Module_Metadonnees/`](./Module_Metadonnees/)
**Extraction et gestion des métadonnées**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `module_fiches_metadonnees.mermaid` : Schéma d'extraction vers Heurist
  - `MODULE_METADONNEES_DOCUMENTATION.md` : Documentation de la structure Heurist
- **Description** : Extraction des métadonnées des fiches manuscrits vers la base Heurist (3 tables : Auteurs, Oeuvres, Éditions)
- **Base de données** : Heurist (hdb_cisame_misha) - 5,768 records, 129 éditions

#### [`Module_NoSketch_Engine/`](./Module_NoSketch_Engine/)
**Pipeline NoSketch-Engine**
- **Statut** : ✅ Opérationnel
- **Contenu** :
  - `module_nosketch_engine.mermaid` : Schéma du pipeline principal
  - `module_nosketch_installation.mermaid` : Schéma d'installation de l'instance test
  - `MODULE_NOSKETCH_ENGINE_DOCUMENTATION.md` : Documentation complète du pipeline
- **Description** : Création de corpus interrogeables (Fusion → Test → Export → Compilation)
- **Outils** : Fusion_txt_NoSketch.py, SCP, compilation serveur
- **Fonctionnalités** : Concordances, collocations, recherche par lemme/forme/POS

### 🔹 Pipelines spécifiques

#### [`Decret_Gratien/`](./Decret_Gratien/)
**Pipeline spécifique au Décret de Gratien**
- **Contenu** :
  - `flowchart-decret-gratien.mmd` : Schéma du workflow dédié
- **Description** : Pipeline adapté au format spécifique du Décret de Gratien
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

## 🔗 Flux de données principal

```
MODULE 1 (Images)
    ↓
MODULE 2 (OCR)
    ↓
MODULE 3 (Segmentation)
    ↓
MODULE 4 (Corrections)
    ↓
MODULE 5 (Export)
    ↓
MODULE 6 (PAGEtopage - Enrichissement)
    ↓
┌───────────────┴──────────────────┐
│                                   │
Module Données Textuelles    Module NoSketch-Engine
(Nakala/Seafile)            (Corpus interrogeable)
```

**En parallèle** : Module Métadonnées (Heurist) fournit les métadonnées bibliographiques

## 🛠️ Technologies principales

- **Langages** : Python 3.10+, Shell
- **OCR** : Tesseract, Kraken
- **Enrichissement** : CLTK (Classical Language Toolkit)
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
| Module 1 (Images) | ✅ Opérationnel | Complété |
| Module 2 (OCR) | ✅ Opérationnel | Complété |
| Module 3 (Segmentation) | ✅ Opérationnel | Complété |
| Module 4 (Corrections) | ✅ Opérationnel | Complété |
| Module 5 (Export) | ✅ Opérationnel | Complété |
| Module 6 (PAGEtopage) | 🚧 Développement | Haute |
| Module Données Textuelles | ✅ Opérationnel | Complété |
| Module Métadonnées | ✅ Opérationnel | Complété |
| Module NoSketch-Engine | ✅ Opérationnel | Complété |
| Pipeline Décret Gratien | ✅ Opérationnel | Complété |

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

*Dernière mise à jour : 9 décembre 2025*
