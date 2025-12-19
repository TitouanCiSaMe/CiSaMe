# 📦 MODULE 6 - PAGEtopage : Enrichissement Linguistique

**Documentation de l'outil d'enrichissement linguistique**

---

## 📋 Vue d'ensemble

MODULE 6 est un pipeline Python d'enrichissement linguistique pour les textes latins et français issus de manuscrits et éditions **génériques** (hors Décret de Gratien).

**Nom de l'outil** : PAGEtopage
**Langage** : Python 3.10+
**Entrée** : Fichiers XML PAGE (sortie du Module 5)
**Sortie** : Corpus enrichi avec lemmatisation + formats exploitables

⚠️ **IMPORTANT** : Ce module est utilisé pour le **cas général uniquement**. Le Décret de Gratien suit un pipeline spécifique et n'utilise PAS PAGEtopage.

---

## 🔄 Pipeline en 4 étapes (3 + correction optionnelle)

### **ÉTAPE 1 : EXTRACTION**

**Objectif** : Extraire le texte des fichiers XML PAGE

**Processus** :
1. Lecture des XML PAGE
2. Détection du mode colonnes :
   - **Single column** : Extraction séquentielle (manuscrits simples)
   - **Dual columns** : Extraction en 2 colonnes (éditions en colonnes)
3. **Fusion des mots coupés** : Reconstitution des mots avec trait d'union
   - Exemple : `re-` + `constituer` → `reconstituer`
4. Génération d'un fichier JSON intermédiaire

**Technologies** :
- `lxml` : Manipulation XML
- Algorithme de fusion de césure

**Sortie** : `extracted.json`

---

### **ÉTAPE 2 : ENRICHISSEMENT**

**Objectif** : Ajouter annotations linguistiques (lemmes, POS tags)

**Processus** :
1. Chargement du JSON extrait
2. **Découpage en phrases** : Détection des limites de phrases
3. **Tokenisation** : Séparation en mots individuels
4. **Traitement TreeTagger** : Lemmatisation + POS-tagging
   - TreeTagger = Outil rapide et fiable pour le latin
   - **Installation automatique** lors de la première utilisation (~20 Mo)
   - Supporte Latin et Français
5. Génération du format **vertical** : 1 mot par ligne avec annotations

**Format vertical** :
```
Mot      POS    Lemme
---      ---    -----
In       PRP    in
nomine   NOM    nomen
Patris   NOM    pater
```

**Technologies** :
- TreeTagger : Lemmatisation latin/français (auto-installé)
- Algorithmes de segmentation de phrases
- Tokenisation adaptée au latin médiéval

**Sortie** : `corpus.vertical.txt`

⚠️ **Note** : TreeTagger s'installe automatiquement lors de la première utilisation (~1 minute pour 350 pages ensuite).

---

### **ÉTAPE 3 : EXPORT**

**Objectif** : Générer les fichiers exploitables dans différents formats

**4 formats disponibles** :

1. **Scholarly** (recommandé) : Format académique avec en-tête complet
   - En-tête détaillé avec toutes les métadonnées
   - Texte en lignes continues
   - Pour publications et ré-enrichissement
   - Préserve parfaitement les métadonnées

2. **Clean** : Texte brut lisible
   - Pour lecture humaine
   - Pas d'annotations visibles
   - Texte fluide

3. **Diplomatic** : Avec annotations inline
   - Annotations semi-visibles
   - Conserve structure originale
   - Pour édition critique

4. **Annotated** : Format tabulaire complet
   - Toutes les annotations
   - Format machine-readable
   - Pour analyse linguistique

**Processus** :
1. Lecture du corpus vertical
2. Choix du format de sortie
3. **Séparation par pages** : Un fichier par page
4. Génération des fichiers complémentaires :
   - `texte_complet.txt` : Fichier unique avec tout le texte
   - `pages_index.json` : Index des pages avec métadonnées
   - `corpus_stats.json` : Statistiques du corpus
   - `images_mapping.txt` : Correspondance texte ↔ images

**Métadonnées incluses** :
Les métadonnées proviennent de **Heurist** et sont renseignées dans `config.yaml` :
```yaml
edition_id: "Edi-7"
title: "Magistri Honorii Summa ''De iure canonico tractaturus''"
language: "Latin"
author: "Honorius"
source: "Summa ''De iure canonico tractaturus''"
type: "Droit canonique"
date: "1188"
lieu: "France"
ville: "Paris"
```

**Sortie** : Dossier avec tous les fichiers + métadonnées enrichies

---

### **ÉTAPE 4 : RÉ-ENRICHISSEMENT (Optionnel)**

**Objectif** : Corriger manuellement le texte et regénérer le corpus vertical

⚠️ **Note** : Cette étape est **optionnelle** et ne s'utilise que si vous devez corriger des coquilles ou erreurs OCR dans le texte final.

**Cas d'usage** :
- Corriger des erreurs OCR/HTR
- Fixer des fautes de transcription
- Améliorer la qualité du texte final
- Régénérer le corpus vertical avec les corrections

**Processus** :
1. **Correction manuelle** : Édition des fichiers texte (format scholarly)
   - Ouvrir les fichiers dans un éditeur de texte
   - Corriger les coquilles, erreurs OCR, etc.
   - Sauvegarder les fichiers corrigés
2. **Parse format scholarly** : Extraction du texte et des métadonnées
   - Lecture des en-têtes détaillés
   - Préservation de toutes les métadonnées
3. **Re-tokenisation** : Nouveau découpage en mots
4. **Re-lemmatisation** : TreeTagger sur le texte corrigé
   - Régénération des lemmes et POS tags
5. Génération du nouveau corpus vertical avec corrections

**Technologies** :
- Parser scholarly : Extraction texte + métadonnées
- TreeTagger : Re-lemmatisation automatique
- Préservation intégrale des métadonnées

**Sortie** : `corpus_corrige.vertical.txt`

**Avantages** :
- Permet de corriger facilement dans des fichiers texte lisibles
- Régénère automatiquement les annotations linguistiques
- Préserve toutes les métadonnées du corpus
- Pas besoin de revenir aux XML sources

---

## 💻 Utilisation

### Installation

```bash
# Prérequis
Python 3.10 ou supérieur

# Dépendances
pip install pyyaml treetaggerwrapper

# TreeTagger s'installe automatiquement
# Pas de configuration manuelle nécessaire
```

### Configuration

1. **Créer le fichier config.yaml**
   ```bash
   python -m PAGEtopage init
   ```

2. **Éditer config.yaml**
   - Consulter Heurist pour récupérer les métadonnées
   - Copier les métadonnées dans le fichier config.yaml
   - Configurer les chemins d'entrée/sortie
   - Choisir le mode colonnes (single/dual)
   - Choisir le format de sortie (clean/diplomatic/annotated)

### Commandes CLI

```bash
# Pipeline complet (3 étapes obligatoires)
python -m PAGEtopage run --input ./xml_pages/ --output ./output/ --config config.yaml

# Étape 1 seule (extraction)
python -m PAGEtopage extract --input ./xml_pages/ --output ./extracted.json

# Étape 2 seule (enrichissement)
python -m PAGEtopage enrich --input ./extracted.json --output ./corpus.vertical.txt

# Étape 3 seule (export)
python -m PAGEtopage export --input ./corpus.vertical.txt --output ./pages/ --format scholarly

# Étape 4 (optionnelle) : ré-enrichissement après correction
python -m PAGEtopage re-enrich --input ./pages_corrigees/ --output ./corpus_corrige.vertical.txt --config config.yaml
```

---

## 🔗 Lien avec les autres modules

### En amont : MODULE 5 (Nettoyage)

**Entrée de PAGEtopage** : Fichiers XML PAGE finalisés

Le Module 5 génère les XML PAGE nettoyés qui servent d'entrée à PAGEtopage.

### En parallèle : Base Heurist

**Source des métadonnées** :

1. Les fiches de métadonnées sont extraites et stockées dans Heurist
2. L'utilisateur consulte Heurist pour l'édition/manuscrit à traiter
3. Copie des métadonnées pertinentes dans `config.yaml`
4. PAGEtopage utilise ces métadonnées pour enrichir les exports

**Métadonnées utilisées** :
- `edition_id` : Identifiant Heurist (ex: "Edi-7")
- `title` : Titre complet
- `language` : Latin / Français
- `author` : Auteur(s)
- `source` : Oeuvre source
- `type` : Type de droit (canonique, romain, etc.)
- `date` : Date de rédaction
- `lieu` : Lieu de rédaction
- `ville` : Ville spécifique

### En aval : NoSketch-Engine

**Sortie vers NoSketch** :

Les fichiers verticaux générés par PAGEtopage sont ensuite :
1. Fusionnés avec `Fusion_txt_NoSketch.py`
2. Importés dans NoSketch-Engine pour consultation

---

## 🎯 Cas d'usage

### ✅ Utilisations appropriées

- Manuscrits juridiques généraux
- Éditions imprimées
- Textes latins classiques
- Textes français médiévaux
- Corpus nécessitant lemmatisation

### ❌ Exclusions

- **Décret de Gratien** : Utilise son propre pipeline spécifique
  - Raison : Structure particulière (allégations + canons)
  - Traitement spécifique déjà implémenté
  - Format .txt adapté déjà sur NoSketch

---

## 📊 Performances et statistiques

**Vitesse de traitement** : ~1 minute pour 350 pages (après installation de TreeTagger)

**Taux d'automatisation** : ~100%
- Extraction : 100% automatique
- Enrichissement : 100% automatique (TreeTagger auto-installé)
- Export : 100% automatique
- Ré-enrichissement : 100% automatique (après corrections manuelles)

**Qualité de lemmatisation** :
- Latin : Excellente (TreeTagger optimisé)
- Français : Très bonne
- Installation automatique : Aucune configuration manuelle

---

## 🛠️ Technologies utilisées

**Langage** : Python 3.10+

**Bibliothèques principales** :
- **TreeTagger** : Lemmatisation latin (installation automatique)
- **treetaggerwrapper** : Interface Python pour TreeTagger
- **PyYAML** : Configuration
- **lxml** : Manipulation XML
- **JSON** : Formats intermédiaires
- **Argparse** : Interface CLI

**Outils connexes** :
- Heurist : Source des métadonnées
- Fusion_txt_NoSketch.py : Export vers NoSketch

---

## 📁 Structure du code

```
PAGEtopage/
├── __init__.py
├── __main__.py              # Point d'entrée CLI
├── cli.py                   # Interface ligne de commande
├── config.py                # Gestion configuration
├── config_example.yaml      # Exemple de configuration
├── models.py                # Modèles de données
│
├── step1_extract/           # ÉTAPE 1
│   ├── extractor.py         # Extraction XML → JSON
│   ├── hyphen_merger.py     # Fusion mots coupés
│   └── zone_parser.py       # Analyse zones XML
│
├── step2_enrich/            # ÉTAPE 2
│   ├── processor.py         # Orchestration enrichissement
│   ├── tokenizer.py         # Tokenisation
│   ├── lemmatizer.py        # Lemmatisation TreeTagger
│   └── treetagger_installer.py  # Installation auto TreeTagger
│
├── step3_export/            # ÉTAPE 3
│   ├── exporter.py          # Export principal
│   ├── formatters.py        # 4 formats (scholarly/clean/diplomatic/annotated)
│   ├── scholarly_parser.py  # Parser format scholarly
│   ├── index_generator.py   # Génération index + stats
│   └── vertical_parser.py   # Lecture format vertical
│
├── step4_reenrich/          # ÉTAPE 4 (optionnelle)
│   └── reenricher.py        # Ré-enrichissement après correction
│
└── tests/                   # Tests unitaires
    ├── test_step1_extract.py
    ├── test_step2_enrich.py
    └── test_step3_export.py
```

---

## 📝 Exemples de configuration

### Manuscrit simple (1 colonne)

```yaml
# config.yaml
metadata:
  edition_id: "Edi-12"
  title: "Summa Decretorum"
  language: "Latin"
  author: "Gratianus"
  type: "Droit canonique"
  date: "1140"

input:
  xml_directory: "/path/to/xml_pages/"

processing:
  column_mode: "single"  # 1 colonne
  merge_hyphens: true

output:
  format: "clean"        # Texte lisible
  output_directory: "/path/to/output/"
  split_pages: true
```

### Édition imprimée (2 colonnes)

```yaml
# config.yaml
metadata:
  edition_id: "Edi-7"
  title: "Magistri Honorii Summa"
  language: "Latin"
  author: "Honorius"
  type: "Droit canonique"
  date: "1188"
  lieu: "France"
  ville: "Paris"

input:
  xml_directory: "/path/to/xml_pages/"

processing:
  column_mode: "dual"      # 2 colonnes
  merge_hyphens: true

output:
  format: "diplomatic"     # Avec annotations
  output_directory: "/path/to/output/"
  split_pages: true
```

---

## ⚠️ Points d'attention

### Première exécution

TreeTagger s'installe automatiquement lors de la première utilisation (~20 Mo). Les exécutions suivantes sont rapides (~1 minute pour 350 pages).

### Qualité des données d'entrée

PAGEtopage suppose que les XML PAGE sont déjà :
- Nettoyés (Module 5)
- Bien structurés
- Avec balises correctes

Si données d'entrée corrompues → résultats imprévisibles.

### Métadonnées manuelles

Les métadonnées doivent être **copiées manuellement** depuis Heurist dans config.yaml. Vérifier :
- L'ID d'édition correct (ex: "Edi-7")
- L'orthographe des noms
- Les dates au bon format

---

## 🔄 Workflow complet

```
1. Module 5 → XML PAGE nettoyés
        ↓
2. Consultation Heurist → Récupération métadonnées
        ↓
3. Édition config.yaml → Ajout métadonnées
        ↓
4. PAGEtopage ÉTAPE 1 → Extraction texte
        ↓
5. PAGEtopage ÉTAPE 2 → Enrichissement TreeTagger
        ↓
6. PAGEtopage ÉTAPE 3 → Export multi-formats (scholarly recommandé)
        ↓
7. (Optionnel) Correction manuelle → Édition des fichiers texte
        ↓
8. (Optionnel) PAGEtopage ÉTAPE 4 → Ré-enrichissement
        ↓
9. Fusion_txt_NoSketch.py → Préparation NoSketch
        ↓
10. Import NoSketch-Engine → Consultation finale
```

---

## 📚 Documentation complémentaire

**Fichiers du projet** :
- `PAGEtopage/README.md` : Documentation technique complète
- `PAGEtopage/QUICKSTART.md` : Guide de démarrage rapide
- `DOCUMENTATION_PAGETOPAGE_SCHEMA.md` : Liens avec schémas

**Schémas** :
- `flowchart-module6-pagetopage.mmd` : Pipeline détaillé

---

## ✅ État actuel

**MODULE 6 (PAGEtopage)** : 🔄 **En cours de développement**

- Code source complet : ✅
- Tests unitaires : ✅
- Documentation : ✅
- Configuration YAML : ✅
- Interface CLI : ✅

**Prêt pour utilisation** avec configuration appropriée.

---

## 🚀 Prochaines étapes

1. Finaliser les tests sur corpus réel
2. Optimisation des performances
3. Documentation utilisateur détaillée
4. Intégration complète dans le pipeline global
