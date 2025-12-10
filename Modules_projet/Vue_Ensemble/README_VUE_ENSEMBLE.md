# Vue d'Ensemble - Schémas récapitulatifs CiSaMe

Ce dossier contient les schémas globaux et les analyses transversales du projet CiSaMe.

## 📊 Schémas disponibles

### 🆕 **flowchart-pipeline-complet-integre.mmd** (RECOMMANDÉ)
**Schéma complet intégré de tout le projet**

Le schéma le plus à jour et complet, montrant :
- ✅ **Modules 1 à 8** : Pipeline principal complet et intégré
- 🟣 **Module Métadonnées** : Transversal (Heurist → config.yaml → MODULE 6)
- 🔴 **Décret de Gratien** : Pipeline parallèle spécifique
- 🔵 **Décisions** : Arbres de décision (avec/sans images, libre/restreint)
- 📦 **Stockages** : Nakala, Seafile, NoSketch-Engine

**Structure du pipeline :**
```
MODULE 1 (Images) → MODULE 2 (OCR) → MODULE 3 (Segmentation)
→ MODULE 4 (Corrections) → MODULE 5 (Export)
→ MODULE 6 (PAGEtopage + Métadonnées)
→ MODULE 7 (NoSketch-Engine) + MODULE 8 (Diffusion Données)
```

**À utiliser pour :**
- Comprendre le flux complet du projet
- Présenter le projet à des nouveaux collaborateurs
- Documenter l'architecture globale

---

### **flowchart-complete-improved.mmd**
**Version antérieure du schéma complet**

Schéma global antérieur à l'intégration des modules dans une numérotation unique.

**Particularités :**
- Vue d'ensemble des modules mais avec ancienne organisation
- Moins détaillé que `flowchart-pipeline-complet-integre.mmd`

⚠️ **Recommandation** : Utiliser plutôt `flowchart-pipeline-complet-integre.mmd` pour une vision à jour.

---

### **flowchart-overview.mmd**
**Vue d'ensemble générale du projet**

Schéma de haut niveau montrant :
- Les grandes étapes du workflow
- Les interactions entre composants majeurs
- Architecture générale

**À utiliser pour :**
- Introduction rapide au projet
- Présentation exécutive
- Vue macro sans détails techniques

---

### **flowchart-simple.mmd**
**Vue simplifiée du workflow**

Version minimaliste du pipeline pour :
- Présentation grand public
- Documentation utilisateur final
- Communication externe

**Contenu :**
- Flux linéaire simplifié
- Étapes principales sans détails techniques
- Entrées et sorties claires

---

## 📚 Analyses et documentation

### **ANALYSE_SCHEMAS_DOCUMENTATION.md**
**Analyse détaillée de la base de données Heurist**

Document de 1,152 lignes contenant :
- 🗄️ Structure complète de la base Heurist (hdb_cisame_misha)
- 📊 Analyse des 9 entités prévues vs 6 créées
- 🔗 Relations entre entités (Auteurs, Oeuvres, Éditions, Manuscrits, etc.)
- 📈 Statistiques : 5,768 records, 129 éditions documentées
- ⚠️ Identification des entités manquantes (notamment : Chapitre)
- 💡 Recommandations d'amélioration
- 🔍 Analyse des champs de chaque type d'enregistrement

**À utiliser pour :**
- Comprendre la structure de données Heurist
- Développer des scripts d'extraction de métadonnées
- Planifier l'évolution de la base de données
- Référence technique complète

---

### **FLOWCHARTS_INDEX.md**
**Index de tous les schémas du projet**

Catalogue complet listant :
- Tous les schémas Mermaid disponibles dans le projet
- Description de chaque schéma
- Emplacement des fichiers
- Usage recommandé

**À utiliser pour :**
- Navigation rapide entre schémas
- Retrouver un schéma spécifique
- Vue d'ensemble de la documentation visuelle

---

## 🎯 Quel schéma utiliser ?

### Pour comprendre le projet complet
→ **`flowchart-pipeline-complet-integre.mmd`** (le plus complet et à jour)

### Pour une introduction rapide
→ **`flowchart-overview.mmd`** (vue macro)

### Pour une présentation simplifiée
→ **`flowchart-simple.mmd`** (grand public)

### Pour comprendre Heurist
→ **`ANALYSE_SCHEMAS_DOCUMENTATION.md`** (documentation technique)

### Pour naviguer tous les schémas
→ **`FLOWCHARTS_INDEX.md`** (index complet)

---

## 🔍 Détails du pipeline intégré

### MODULE 1 → MODULE 5
Pipeline de numérisation et préparation :
- Téléchargement images
- OCR et extraction texte
- Segmentation et structuration
- Corrections et validation
- Export et préparation

### MODULE 6 (🚧 Développement)
**PAGEtopage** : Enrichissement linguistique
- Extract : XML → JSON
- Enrich : CLTK (lemmatisation, POS-tagging)
- Export : 3 formats (clean, diplomatic, vertical)
- Alimenté par : Module Métadonnées (Heurist)

### MODULE 7
**NoSketch-Engine** : Corpus interrogeable
- Fusion des fichiers verticaux (.vertical.txt)
- Test sur instance locale
- Export vers serveur production (SCP)
- Compilation et mise en service
- Sortie : Corpus CiSaMe interrogeable en ligne

### MODULE 8
**Diffusion Données** : Archives publiques/privées
- Décision : Avec/Sans images × Libre/Restreint
- Destinations :
  - **Nakala** : Données libres (via Algo Hécate)
  - **Seafile** : Données restreintes (cloud universitaire)
- Sortie : Archives scientifiques accessibles

### Module Métadonnées (Transversal)
**Heurist** : Base de données bibliographiques
- 3 tables : Auteurs, Oeuvres, Éditions
- 5,768 records, 129 éditions
- Alimente : config.yaml du MODULE 6
- Processus manuel : consultation → copie

### Pipeline Parallèle : Décret de Gratien
**Workflow spécifique**
- ⚠️ NE PASSE PAS par MODULE 6
- Format .txt adapté déjà créé
- Déjà sur NoSketch-Engine
- Corpus opérationnel

---

## 🛠️ Visualiser les schémas Mermaid

### En ligne
- [Mermaid Live Editor](https://mermaid.live/) : Copier-coller le contenu du fichier .mmd
- [GitHub](https://github.com) : Affichage natif des schémas Mermaid dans les README

### Localement
- **VS Code** : Extension "Markdown Preview Mermaid Support"
- **IntelliJ/PyCharm** : Plugin "Mermaid"
- **CLI** : `mmdc` (Mermaid CLI) pour export PNG/SVG

### Exemple commande CLI
```bash
# Installation
npm install -g @mermaid-js/mermaid-cli

# Export PNG
mmdc -i flowchart-pipeline-complet-integre.mmd -o pipeline.png

# Export SVG
mmdc -i flowchart-pipeline-complet-integre.mmd -o pipeline.svg
```

---

## 📊 Statistiques du projet

| Métrique | Valeur |
|----------|--------|
| Manuscrits dans le corpus | 317 |
| Records Heurist | 5,768 |
| Éditions documentées | 129 |
| Modules principaux | 8 |
| Modules transversaux | 1 |
| Pipelines parallèles | 1 |
| Modules opérationnels | 7 (1-5, 7-8) |
| Modules en développement | 1 (MODULE 6) |

---

## 🔄 Dernière mise à jour

**Date** : 9 décembre 2025

**Modifications récentes :**
- ✅ Intégration complète des modules 7 et 8 dans le pipeline principal
- ✅ Création du schéma `flowchart-pipeline-complet-integre.mmd`
- ✅ Renommage : Module_NoSketch_Engine → Module_7_NoSketch_Engine
- ✅ Renommage : Module_Donnees_Textuelles → Module_8_Diffusion_Donnees
- ✅ Module Métadonnées clairement identifié comme transversal
- ✅ Décret de Gratien clairement identifié comme pipeline parallèle

---

## 📧 Contact

**Projet** : CiSaMe - Université de Strasbourg
**Portée** : Corpus juridiques médiévaux (droit canonique et civil)
**Période** : Moyen Âge

---

*Pour revenir à la documentation principale, voir [`../README.md`](../README.md)*
