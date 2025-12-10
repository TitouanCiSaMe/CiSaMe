# Vue d'Ensemble - Schéma récapitulatif CiSaMe

Ce dossier contient le schéma global et la documentation du projet CiSaMe.

## 📊 Schéma principal

### 🆕 **flowchart-pipeline-complet-integre.mmd**
**Schéma complet intégré de tout le projet**

Le schéma le plus à jour et complet, montrant :
- ✅ **Modules 1 à 9** : Pipeline principal complet et intégré
- 🟣 **Module Métadonnées** : Transversal (Heurist → config.yaml → MODULE 6)
- 🔴 **Décret de Gratien** : Pipeline parallèle spécifique
- 🔵 **Décisions** : Arbres de décision (avec/sans images, libre/restreint)
- 📦 **Stockages** : Nakala, Seafile, NoSketch-Engine

**Structure du pipeline :**
```
MODULE 1 (Images) → MODULE 2 (OCR) → MODULE 3 (Segmentation)
→ MODULE 4 (Corrections) → MODULE 5 (Nettoyage Oxygène)
→ MODULE 6 (PAGEtopage + Métadonnées)
→ MODULE 7 (NoSketch-Engine) + MODULE 8 (Diffusion Données)
→ MODULE 9 (Visualisation & Analyse)
```

**À utiliser pour :**
- Comprendre le flux complet du projet
- Présenter le projet à des nouveaux collaborateurs
- Documenter l'architecture globale

---

## 📚 Documentation complémentaire

### **FLOWCHARTS_INDEX.md**
**Index de tous les schémas du projet**

Catalogue complet listant :
- Tous les schémas Mermaid disponibles dans le projet
- Description de chaque module
- Emplacement des fichiers
- Usage recommandé

**À utiliser pour :**
- Navigation rapide entre modules
- Retrouver un schéma spécifique
- Vue d'ensemble de la documentation visuelle

---

## 🔍 Détails du pipeline intégré

### MODULE 1 - Téléchargement Images
Acquisition des manuscrits depuis diverses sources :
- IIIF (International Image Interoperability Framework)
- PDF avec extraction
- Méthodes avancées (hexadécimal, tuiles)

### MODULE 2 - OCR & Reconnaissance
Extraction du texte des images :
- Outils : Escriptorium, Kraken
- Sortie : XML PAGE avec segmentation

### MODULE 3 - Segmentation & Structuration
Analyse et découpage sémantique :
- HTR (Handwritten Text Recognition)
- Modèles spécialisés
- Répartition : 30% libre, 68% restreint, 2% secret

### MODULE 4 - Corrections & Validation
Corrections manuelles et validation :
- Post-traitement
- Vérification qualité
- Validation métadonnées

### MODULE 5 - Nettoyage Post-eScriptorium
**Oxygène XML Editor** : Nettoyage avancé des fichiers XML
- XPath pour ciblage précis des régions
- Regex spécifiques au texte médiéval
- Support layouts : 1, 2 ou 4 régions Main par page
- Temps : ~20 min par œuvre
- Format : NOMÉDITION_ID.xml

### MODULE 6 (🚧 Développement)
**PAGEtopage** : Enrichissement linguistique
- Extract : XML → JSON
- Enrich : **TreeTagger** (lemmatisation, POS-tagging)
- Export : **2 formats**
  - texte_clean.txt (normalisé, lemmatisé)
  - corpus_vertical.txt (format vertical : Mot | POS | Lemme)
- Alimenté par : Module Métadonnées (Heurist)
- Technologies : Python 3.10+, TreeTagger, PyYAML

### MODULE 7 - NoSketch-Engine
**Concordancier** : Corpus interrogeable
- Fusion des fichiers corpus_vertical.txt
- Test sur instance locale
- Export vers serveur production (SCP)
- Compilation et mise en service
- Sortie : Corpus CiSaMe interrogeable en ligne

### MODULE 8 - Diffusion Données Textuelles
**Archives publiques/privées**
- Décision : Avec/Sans images × Libre/Restreint
- Destinations :
  - **Nakala** : Données libres (via Connecteur Nakala)
  - **Seafile** : Données restreintes (cloud universitaire)
- Sortie : Archives scientifiques accessibles

### MODULE 9 - Visualisation et Générateur de Requêtes
**Canon-Law-Toolkit** : Plateforme web d'analyse
- **Query Generator** : Générateur de requêtes CQL
  - 4 types de recherche (Proximité, Variations, Sémantique, Combiné)
  - 96 variantes orthographiques médiévales (ae/e, v/u, j/i, ti/ci)
  - Export direct vers NoSketch-Engine
- **Concordance Analyzer** : Analyse de concordances
  - 9 vues d'analyse spécialisées
  - Enrichissement métadonnées Edi-XX
  - Comparaison de 2 corpus (5 dimensions)
  - Export : CSV, JSON, PNG
- Technologies : React 18.2, Vite 5.0, Recharts, D3.js
- Repository : [canon-law-toolkit](https://gitlab.com/cisame/canon-law-toolkit)

### Module Métadonnées (Transversal)
**Heurist** : Base de données bibliographiques
- 3 tables : Auteurs, Oeuvres, Éditions
- 5,768 records, ~150 éditions
- Alimente : config.yaml du MODULE 6
- Processus manuel : consultation → copie

### Pipeline Parallèle : Décret de Gratien
**Workflow spécifique**
- ⚠️ NE PASSE PAS par MODULE 6
- Traitement spécialisé déjà effectué
- Déjà sur NoSketch-Engine
- Corpus opérationnel : 4149 fichiers, 5 Mo
- Format ID : Grat_XXXX

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
| Éditions de manuscrits | ~150 |
| Records Heurist | 5,768 |
| Modules principaux | 9 |
| Modules transversaux | 1 (Métadonnées) |
| Pipelines parallèles | 1 (Décret de Gratien) |
| Modules opérationnels | 8 (1-5, 7-9) |
| Modules en développement | 1 (MODULE 6) |

---

## 🔄 Dernière mise à jour

**Date** : 10 décembre 2024

**Modifications récentes :**
- ✅ Module 9 : Ajout Visualisation et Générateur de Requêtes (canon-law-toolkit)
- ✅ Module 5 : Refonte complète avec Oxygène XML Editor
- ✅ Module 6 : Migration CLTK → TreeTagger, 2 formats au lieu de 3
- ✅ Module 7 : Reformatage complet NoSketch Engine
- ✅ Module 8 : Remplacement Algo Hécate → Connecteur Nakala uniquement
- ✅ Module Métadonnées : Reformatage complet (~150 éditions)
- ✅ Décret de Gratien : Restructuration complète
- ✅ Vue Ensemble : Mise à jour avec toutes les corrections
- ✅ Suppression des schémas obsolètes
- ✅ Corrections parsing Mermaid pour affichage GitHub

---

## 📧 Contact

**Projet** : CiSaMe - Université de Strasbourg
**Portée** : Corpus juridiques médiévaux (droit canonique et civil)
**Période** : Moyen Âge

---

*Pour la documentation technique complète, voir le dossier [`/Documentation/`](../../Documentation/)*
