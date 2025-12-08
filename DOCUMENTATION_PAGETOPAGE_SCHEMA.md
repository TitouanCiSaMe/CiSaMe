# Documentation PAGEtopage - Liaison avec les Schémas du Pipeline

## 📋 Vue d'ensemble

Ce document établit le lien entre le **dossier PAGEtopage** (nouveau module de traitement) et les **schémas du pipeline** existants dans `Shema_module_projet/`.

**PAGEtopage** représente une **extension majeure du Module 5**, ajoutant des capacités d'enrichissement linguistique et d'export en formats exploitables pour l'analyse textuelle.

---

## 🔗 Position de PAGEtopage dans le Pipeline Global

### Pipeline Complet (Modules 1-5 + PAGEtopage)

```
MODULE 1: Acquisition Manuscrits
    ↓
MODULE 2: Téléchargement Images
    ↓
MODULE 3: Acquisition Éditions
    ↓
MODULE 4: Traitement eScriptorium (HTR/OCR)
    ↓
MODULE 5: Nettoyage Post-eScriptorium ← Schéma existant
    ↓
📦 PAGEtopage: Enrichissement Linguistique ← NOUVEAU
    ↓
FORMAT VERTICAL + CORPUS ANNOTÉ
```

---

## 📊 Correspondance Module 5 ↔ PAGEtopage

### Ce que fait le Module 5 (selon flowchart-module5.mmd)

| Étape Module 5 | Description | Schéma |
|----------------|-------------|---------|
| 🔹 Import XML | Import depuis eScriptorium | `flowchart-module5.mmd:11-13` |
| 🔹 Stockage Seafile | Archivage cloud avec ID | `flowchart-module5.mmd:12` |
| 🔹 Distinction Layout | 1, 2 ou 4 régions Main | `flowchart-module5.mmd:22-24` |
| 🔹 Regex Communes | Normalisation espaces, ponctuation | `flowchart-module5.mmd:105-110` |
| 🔹 Regex Spécifiques | Abbréviations, numérotation | `flowchart-module5.mmd:112-118` |
| 🔹 Vérification | Détection erreurs, cohérence | `flowchart-module5.mmd:81-94` |
| ✅ **Sortie** | **Transcriptions XML PAGE finalisées** | `flowchart-module5.mmd:95` |

### Ce que fait PAGEtopage (au-delà du Module 5)

| Étape PAGEtopage | Description | Fichier Code |
|------------------|-------------|--------------|
| 🔹 **ENTRÉE** | **XML PAGE finalisés (sortie Module 5)** | - |
| 🔹 Extraction (Step 1) | Extraction texte, fusion mots coupés | `PAGEtopage/step1_extract/` |
| 🔹 Enrichissement (Step 2) | Lemmatisation, POS-tagging (CLTK) | `PAGEtopage/step2_enrich/` |
| 🔹 Export (Step 3) | Format vertical, fichiers texte | `PAGEtopage/step3_export/` |
| ✅ **SORTIE** | **Corpus annoté + Fichiers texte exploitables** | - |

---

## 🎯 PAGEtopage = Module 5.5 ou Module 6 ?

### Option 1 : Module 5 Étendu (5.5)
PAGEtopage peut être considéré comme une **extension du Module 5**, ajoutant :
- Post-traitement linguistique
- Enrichissement automatique
- Transformation en formats d'analyse

### Option 2 : Nouveau Module 6
PAGEtopage pourrait être un **Module 6 distinct** :
- **MODULE 5** : Nettoyage et finalisation des XML PAGE
- **MODULE 6** : Transformation linguistique et enrichissement

**➡️ Recommandation** : Considérer PAGEtopage comme **Module 6 - Enrichissement Linguistique**

---

## 📐 Nouveau Schéma Proposé : Module 6 (PAGEtopage)

### Diagramme de Flux Module 6

```mermaid
flowchart TD
    %% ========================================
    %% MODULE 6 - ENRICHISSEMENT LINGUISTIQUE (PAGEtopage)
    %% ========================================

    START([📦 MODULE 6<br/>PAGEtopage - Enrichissement Linguistique])

    %% ENTRÉE
    INPUT_MODULE5[📥 XML PAGE finalisés<br/>Sortie du Module 5]
    START --> INPUT_MODULE5

    %% ========================================
    %% ÉTAPE 1 : EXTRACTION
    %% ========================================
    subgraph STEP1 [📄 ÉTAPE 1 : Extraction]
        EXTRACT_START[🔍 Lecture des XML PAGE<br/>Analyse de la structure]

        COLUMN_DECISION{Mode colonnes ?}
        SINGLE_COL[📄 Single Column<br/>Extraction séquentielle]
        DUAL_COL[📄📄 Dual Columns<br/>Extraction en 2 colonnes]

        HYPHEN_MERGE[🔗 Fusion mots coupés<br/>re-/constituer → reconstituer]

        JSON_INTERMEDIATE[💾 Fichier JSON intermédiaire<br/>extracted.json]

        EXTRACT_START --> COLUMN_DECISION
        COLUMN_DECISION -->|single| SINGLE_COL
        COLUMN_DECISION -->|dual| DUAL_COL
        SINGLE_COL --> HYPHEN_MERGE
        DUAL_COL --> HYPHEN_MERGE
        HYPHEN_MERGE --> JSON_INTERMEDIATE
    end

    INPUT_MODULE5 --> EXTRACT_START

    %% ========================================
    %% ÉTAPE 2 : ENRICHISSEMENT
    %% ========================================
    subgraph STEP2 [🎓 ÉTAPE 2 : Enrichissement]
        ENRICH_START[📖 Lecture JSON<br/>Chargement corpus]

        SENTENCE_SPLIT[✂️ Découpage en phrases<br/>Détection de limites]

        TOKENIZATION[🔤 Tokenisation<br/>Séparation en mots]

        CLTK_PROCESS[🧠 Traitement CLTK<br/>Lemmatisation + POS-tagging]

        VERTICAL_FORMAT[📊 Format Vertical<br/>Mot | POS | Lemme]

        CORPUS_VERTICAL[💾 corpus.vertical.txt<br/>Fichier annoté complet]

        ENRICH_START --> SENTENCE_SPLIT
        SENTENCE_SPLIT --> TOKENIZATION
        TOKENIZATION --> CLTK_PROCESS
        CLTK_PROCESS --> VERTICAL_FORMAT
        VERTICAL_FORMAT --> CORPUS_VERTICAL
    end

    JSON_INTERMEDIATE --> ENRICH_START

    %% ========================================
    %% ÉTAPE 3 : EXPORT
    %% ========================================
    subgraph STEP3 [📤 ÉTAPE 3 : Export]
        EXPORT_START[📖 Lecture corpus vertical]

        FORMAT_CHOICE{Format de sortie ?}

        FORMAT_CLEAN[✨ Clean<br/>Texte brut lisible]
        FORMAT_DIPLO[📝 Diplomatic<br/>Avec annotations inline]
        FORMAT_ANNOT[📊 Annotated<br/>Format tabulaire]

        PAGE_SPLIT[📑 Séparation par pages<br/>Un fichier par page]

        COMBINED_FILE[📘 Fichier texte complet<br/>texte_complet.txt]

        INDEX_JSON[🗂️ Index des pages<br/>pages_index.json]

        STATS_JSON[📊 Statistiques corpus<br/>corpus_stats.json]

        IMAGE_MAPPING[🖼️ Correspondance images<br/>images_mapping.txt]

        EXPORT_START --> FORMAT_CHOICE
        FORMAT_CHOICE -->|clean| FORMAT_CLEAN
        FORMAT_CHOICE -->|diplomatic| FORMAT_DIPLO
        FORMAT_CHOICE -->|annotated| FORMAT_ANNOT

        FORMAT_CLEAN --> PAGE_SPLIT
        FORMAT_DIPLO --> PAGE_SPLIT
        FORMAT_ANNOT --> PAGE_SPLIT

        PAGE_SPLIT --> COMBINED_FILE
        PAGE_SPLIT --> INDEX_JSON
        PAGE_SPLIT --> STATS_JSON
        PAGE_SPLIT --> IMAGE_MAPPING
    end

    CORPUS_VERTICAL --> EXPORT_START

    %% SORTIE FINALE
    OUTPUT([📤 SORTIE MODULE 6<br/>Corpus enrichi + Fichiers exploitables])

    COMBINED_FILE --> OUTPUT
    INDEX_JSON --> OUTPUT
    STATS_JSON --> OUTPUT
    IMAGE_MAPPING --> OUTPUT

    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 Configuration:<br/>config.yaml définit<br/>tous les paramètres<br/>du traitement]
    note2[💡 CLTK:<br/>Première exécution lente<br/>Téléchargement modèles<br/>Puis rapide]
    note3[💡 Formats:<br/>Clean = lecture humaine<br/>Diplomatic = semi-annoté<br/>Annotated = analyse machine]
    note4[💡 Métadonnées:<br/>Préservées à chaque étape<br/>Traçabilité complète]

    EXTRACT_START -.-> note1
    CLTK_PROCESS -.-> note2
    FORMAT_CHOICE -.-> note3
    INDEX_JSON -.-> note4

    %% ========================================
    %% STATISTIQUES
    %% ========================================
    subgraph STATS [📊 Caractéristiques Techniques]
        S1[Langues supportées: Latin, Français]
        S2[Lemmatiseur: CLTK pour langues anciennes]
        S3[Formats sortie: 3 formats configurables]
        S4[Métadonnées: Préservées dans tous formats]
        S5[Performance: 100-1000 pages/minute]
    end

    %% ========================================
    %% OUTILS
    %% ========================================
    subgraph TOOLS [🛠️ Technologies Utilisées]
        T1[Python 3.10+]
        T2[CLTK: Classical Language Toolkit]
        T3[PyYAML: Configuration]
        T4[lxml: Manipulation XML]
        T5[JSON: Formats intermédiaires]
    end

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef decision fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    classDef extract fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef enrich fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    classDef export fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef intermediate fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef output fill:#a5d6a7,stroke:#2e7d32,stroke-width:3px
    classDef note fill:#fff9c4,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5

    class START,OUTPUT startEnd
    class COLUMN_DECISION,FORMAT_CHOICE decision
    class EXTRACT_START,SINGLE_COL,DUAL_COL,HYPHEN_MERGE extract
    class ENRICH_START,SENTENCE_SPLIT,TOKENIZATION,CLTK_PROCESS,VERTICAL_FORMAT enrich
    class EXPORT_START,FORMAT_CLEAN,FORMAT_DIPLO,FORMAT_ANNOT,PAGE_SPLIT export
    class JSON_INTERMEDIATE,CORPUS_VERTICAL intermediate
    class COMBINED_FILE,INDEX_JSON,STATS_JSON,IMAGE_MAPPING output
    class note1,note2,note3,note4 note

    style STEP1 fill:#e8f5e9,stroke:#1565c0,stroke-width:2px
    style STEP2 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style STEP3 fill:#fff8e1,stroke:#e65100,stroke-width:2px
    style STATS fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 3 3
    style TOOLS fill:#e0f2f1,stroke:#00796b,stroke-width:2px,stroke-dasharray: 3 3
```

---

## 📚 Références Croisées : Documentation ↔ Schéma

### Étape 1 : Extraction

| Documentation (README.md) | Schéma Module 6 | Fichier Code |
|---------------------------|-----------------|--------------|
| Section "Étape 1 : Extraction des XML" (ligne 174-184) | Sous-graphe STEP1 | `step1_extract/` |
| Option `column_mode: single/dual` (ligne 106) | `COLUMN_DECISION` | `config.py` |
| Option `merge_hyphenated: true` (ligne 107) | `HYPHEN_MERGE` | `step1_extract/extractor.py` |
| Sortie `extracted.json` (ligne 184) | `JSON_INTERMEDIATE` | - |

### Étape 2 : Enrichissement

| Documentation (README.md) | Schéma Module 6 | Fichier Code |
|---------------------------|-----------------|--------------|
| Section "Étape 2 : Enrichissement" (ligne 186-198) | Sous-graphe STEP2 | `step2_enrich/` |
| Option `lemmatizer: cltk` (ligne 111) | `CLTK_PROCESS` | `config.py` |
| Option `language: lat` (ligne 112) | `CLTK_PROCESS` | `config.py` |
| Section "Format vertical" (ligne 251-289) | `VERTICAL_FORMAT` | - |
| Sortie `corpus.vertical.txt` (ligne 189) | `CORPUS_VERTICAL` | - |

### Étape 3 : Export

| Documentation (README.md) | Schéma Module 6 | Fichier Code |
|---------------------------|-----------------|--------------|
| Section "Étape 3 : Export" (ligne 200-210) | Sous-graphe STEP3 | `step3_export/` |
| Section "Formats de sortie" (ligne 213-248) | `FORMAT_CHOICE` | `config.py` |
| Format "clean" (ligne 215-221) | `FORMAT_CLEAN` | `step3_export/formatter.py` |
| Format "diplomatic" (ligne 223-229) | `FORMAT_DIPLO` | `step3_export/formatter.py` |
| Format "annotated" (ligne 231-241) | `FORMAT_ANNOT` | `step3_export/formatter.py` |
| Fichier `pages/page_*.txt` (ligne 161-163) | `PAGE_SPLIT` | - |
| Fichier `texte_complet.txt` (ligne 165) | `COMBINED_FILE` | - |
| Fichier `pages_index.json` (ligne 164) | `INDEX_JSON` | - |
| Fichier `corpus_stats.json` (ligne 166) | `STATS_JSON` | - |
| Fichier `images_mapping.txt` (ligne 167) | `IMAGE_MAPPING` | - |

---

## 🔄 Flux de Données Complet : Module 5 → PAGEtopage

```
┌─────────────────────────────────────────────────────────────┐
│ MODULE 5 : Nettoyage Post-eScriptorium                      │
│ (flowchart-module5.mmd)                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Import XML] → [Stockage Seafile] → [Export local]        │
│       ↓                                                     │
│  [Distinction Layout: 1/2/4 régions Main]                   │
│       ↓                                                     │
│  [Application Regex Communes]                               │
│       ↓                                                     │
│  [Application Regex Spécifiques]                            │
│       ↓                                                     │
│  [Vérification et Corrections]                              │
│       ↓                                                     │
│  ✅ SORTIE : Transcriptions XML PAGE finalisées            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                         ↓
                         ↓ (Fichiers XML PAGE nettoyés)
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ MODULE 6 : PAGEtopage - Enrichissement Linguistique        │
│ (PAGEtopage/)                                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ÉTAPE 1 : Extraction                                       │
│  ─────────────────────                                      │
│  [Lecture XML PAGE] → [Extraction texte]                   │
│       ↓                                                     │
│  [Gestion colonnes single/dual]                             │
│       ↓                                                     │
│  [Fusion mots coupés]                                       │
│       ↓                                                     │
│  → extracted.json                                           │
│                                                             │
│  ÉTAPE 2 : Enrichissement                                   │
│  ──────────────────────                                     │
│  [Lecture JSON] → [Découpage en phrases]                   │
│       ↓                                                     │
│  [Tokenisation]                                             │
│       ↓                                                     │
│  [Lemmatisation CLTK + POS-tagging]                        │
│       ↓                                                     │
│  → corpus.vertical.txt                                      │
│                                                             │
│  ÉTAPE 3 : Export                                           │
│  ─────────────────                                          │
│  [Lecture corpus vertical]                                  │
│       ↓                                                     │
│  [Choix format: clean/diplomatic/annotated]                │
│       ↓                                                     │
│  [Génération fichiers par page]                            │
│       ↓                                                     │
│  ✅ SORTIES :                                               │
│     • pages/page_*.txt (un par page)                       │
│     • texte_complet.txt (tout le corpus)                   │
│     • pages_index.json (métadonnées)                       │
│     • corpus_stats.json (statistiques)                     │
│     • images_mapping.txt (correspondances)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                         ↓
                         ↓
                   CORPUS EXPLOITABLE
                (Analyse linguistique, recherches, etc.)
```

---

## 🎯 Cas d'Usage : Du Manuscrit au Corpus Annoté

### Exemple Pratique

1. **MODULES 1-3** : Acquisition du manuscrit MS123 (Décret de Gratien, XIIe siècle)
   - Téléchargement IIIF depuis la British Library
   - 300 pages, TIF 600 DPI

2. **MODULE 4** : Traitement eScriptorium
   - Segmentation automatique (modèle réutilisé)
   - Transcription HTR (CER = 5.2%)
   - Validation manuelle

3. **MODULE 5** : Nettoyage (`flowchart-module5.mmd`)
   - Import des 300 XML PAGE
   - Détection : 2 régions Main par page (verso-recto)
   - Application regex communes (normalisation espaces)
   - Application regex spécifiques (abbréviations latines)
   - Vérification : 12 erreurs détectées et corrigées
   - **Sortie** : 300 fichiers XML PAGE finalisés

4. **MODULE 6** : PAGEtopage (`PAGEtopage/`)

   **Commande exécutée** :
   ```bash
   python -m PAGEtopage run \
       --input ./ms123_xml_pages/ \
       --output ./ms123_corpus/ \
       --config ms123_config.yaml
   ```

   **Étape 1 - Extraction** :
   - Lecture des 300 XML PAGE
   - Mode : `dual` (2 colonnes par page)
   - Fusion des mots coupés : 1847 occurrences
   - Création : `extracted.json` (2.3 Mo)

   **Étape 2 - Enrichissement** :
   - Découpage : 8 742 phrases
   - Tokenisation : 156 392 tokens
   - Lemmatisation CLTK (Latin) : 154 203 lemmes identifiés
   - POS-tagging : 97.8% de confiance
   - Création : `corpus.vertical.txt` (8.7 Mo)

   **Étape 3 - Export** :
   - Format choisi : `clean` (texte lisible)
   - Génération de 300 fichiers `page_*.txt`
   - Création `texte_complet.txt` (512 Ko)
   - Création `pages_index.json` avec métadonnées complètes
   - Statistiques : 156k mots, 8.7k phrases, 300 pages

5. **RÉSULTAT FINAL** : Corpus MS123 prêt pour :
   - Recherche plein-texte
   - Analyse linguistique (fréquences, concordances)
   - Études lexicales (lemmes, POS)
   - Comparaison avec autres manuscrits
   - Intégration dans une base de données

---

## 🔧 Fichiers de Configuration : Lien avec le Schéma

Le fichier `config.yaml` contrôle chaque étape du schéma Module 6 :

```yaml
# Contrôle COLUMN_DECISION dans Étape 1
extraction:
  column_mode: single          # → SINGLE_COL
  # ou dual                    # → DUAL_COL
  merge_hyphenated: true       # → HYPHEN_MERGE

# Contrôle CLTK_PROCESS dans Étape 2
enrichment:
  lemmatizer: cltk             # → CLTK_PROCESS
  language: lat                # → CLTK_PROCESS (Latin)

# Contrôle FORMAT_CHOICE dans Étape 3
export:
  format: clean                # → FORMAT_CLEAN
  # ou diplomatic              # → FORMAT_DIPLO
  # ou annotated               # → FORMAT_ANNOT
  generate_index: true         # → INDEX_JSON
  generate_combined: true      # → COMBINED_FILE
```

---

## 📖 Exemples de Données à Chaque Étape

### Entrée Module 6 (Sortie Module 5)

**Fichier** : `0042.xml` (XML PAGE finalisé)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PcGts>
  <Page imageFilename="ms_0042.tif">
    <TextRegion id="region_main_1" type="MainZone">
      <TextLine id="line_1">
        <TextEquiv>
          <Unicode>Dominus enim dicit in evangelio</Unicode>
        </TextEquiv>
      </TextLine>
    </TextRegion>
  </Page>
</PcGts>
```

### Après Étape 1 (Extraction)

**Fichier** : `extracted.json`

```json
{
  "pages": [
    {
      "folio": "0042.xml",
      "page_number": 42,
      "text": "Dominus enim dicit in evangelio. Qui perseveraverit usque in finem, hic salvus erit."
    }
  ]
}
```

### Après Étape 2 (Enrichissement)

**Fichier** : `corpus.vertical.txt`

```
<doc folio="0042.xml" page_number="42" edition_id="MS123" title="Décret de Gratien">
<s>
Dominus	NOM	dominus
enim	ADV	enim
dicit	VER	dico
in	PRP	in
evangelio	NOM	evangelium
.	PUNCT	.
</s>
<s>
Qui	PRO	qui
perseveraverit	VER	persevero
usque	ADV	usque
in	PRP	in
finem	NOM	finis
,	PUNCT	,
hic	ADV	hic
salvus	ADJ	salvus
erit	VER	sum
.	PUNCT	.
</s>
</doc>
```

### Après Étape 3 (Export format "clean")

**Fichier** : `pages/page_0042_0042.txt`

```
Dominus enim dicit in evangelio. Qui perseveraverit usque in finem, hic salvus erit.
```

**Fichier** : `pages_index.json`

```json
{
  "pages": [
    {
      "folio": "0042.xml",
      "page_number": 42,
      "file_path": "pages/page_0042_0042.txt",
      "word_count": 15,
      "sentence_count": 2,
      "line_count": 1
    }
  ]
}
```

---

## 🚀 Utilisation Pratique : Commandes et Schéma

### Pipeline Complet (Méthode Recommandée)

```bash
python -m PAGEtopage run \
    --input ./xml_pages/ \
    --output ./output/ \
    --config config.yaml
```

**Parcours dans le schéma** :
```
START → INPUT_MODULE5 → EXTRACT_START → ... → OUTPUT
```

### Pipeline Étape par Étape

#### Étape 1 : Extraction

```bash
python -m PAGEtopage extract \
    --input ./xml_pages/ \
    --output ./extracted.json
```

**Parcours** : `START → STEP1 → JSON_INTERMEDIATE`

#### Étape 2 : Enrichissement

```bash
python -m PAGEtopage enrich \
    --input ./extracted.json \
    --output ./corpus.vertical.txt
```

**Parcours** : `JSON_INTERMEDIATE → STEP2 → CORPUS_VERTICAL`

#### Étape 3 : Export

```bash
python -m PAGEtopage export \
    --input ./corpus.vertical.txt \
    --output ./pages/ \
    --format clean
```

**Parcours** : `CORPUS_VERTICAL → STEP3 → OUTPUT`

---

## 📊 Mise à Jour de l'Index des Schémas

### Ajout Recommandé à `Shema_module_projet/FLOWCHARTS_INDEX.md`

Ajouter une nouvelle section après le MODULE 5 :

```markdown
#### 📌 [flowchart-module6-pagetopage.mmd](./flowchart-module6-pagetopage.mmd)
**MODULE 6 - Enrichissement Linguistique (PAGEtopage)**
**Niveau de détail:** ⭐⭐⭐⭐ (Très détaillé)

**Contenu:**
- Étape 1 : Extraction du texte depuis XML PAGE
  - Gestion des colonnes (single/dual)
  - Fusion des mots coupés
  - Production JSON intermédiaire
- Étape 2 : Enrichissement linguistique
  - Découpage en phrases et tokenisation
  - Lemmatisation CLTK (langues anciennes)
  - POS-tagging automatique
  - Production format vertical
- Étape 3 : Export multi-formats
  - Format clean (texte brut)
  - Format diplomatic (annotations inline)
  - Format annotated (tabulaire)
  - Génération index et statistiques
- Technologies : Python, CLTK, PyYAML, lxml

**Idéal pour:**
- Comprendre la transformation XML → Corpus annoté
- Planifier l'enrichissement linguistique
- Choisir les formats de sortie appropriés

**Code source:** `../PAGEtopage/`
**Documentation:** `../PAGEtopage/README.md`
```

---

## 🎓 Glossaire Étendu : Termes du Module 6

| Terme | Définition | Référence Schéma |
|-------|------------|------------------|
| **Format Vertical** | Format d'annotation linguistique avec un mot par ligne, incluant lemme et POS | `VERTICAL_FORMAT` |
| **Lemmatisation** | Réduction d'un mot à sa forme canonique (dicit → dico) | `CLTK_PROCESS` |
| **POS-tagging** | Part-of-Speech tagging, étiquetage grammatical (nom, verbe...) | `CLTK_PROCESS` |
| **CLTK** | Classical Language Toolkit, bibliothèque Python pour langues anciennes | `CLTK_PROCESS` |
| **Tokenisation** | Découpage du texte en unités (mots, ponctuation) | `TOKENIZATION` |
| **Format Clean** | Texte brut sans annotations, lisible par humains | `FORMAT_CLEAN` |
| **Format Diplomatic** | Texte avec annotations entre parenthèses | `FORMAT_DIPLO` |
| **Format Annotated** | Format tabulaire avec colonnes (mot/POS/lemme) | `FORMAT_ANNOT` |
| **Mots coupés** | Mots séparés par un tiret en fin de ligne (re-/constituer) | `HYPHEN_MERGE` |
| **JSON intermédiaire** | Format temporaire entre extraction et enrichissement | `JSON_INTERMEDIATE` |
| **Corpus vertical** | Fichier contenant tout le corpus au format vertical | `CORPUS_VERTICAL` |

---

## 🔗 Ressources et Liens

### Documentation

- **PAGEtopage README** : `PAGEtopage/README.md`
- **PAGEtopage QUICKSTART** : `PAGEtopage/QUICKSTART.md`
- **Schéma Module 5** : `Shema_module_projet/flowchart-module5.mmd`
- **Index des Schémas** : `Shema_module_projet/FLOWCHARTS_INDEX.md`

### Code Source

- **Étape 1** : `PAGEtopage/step1_extract/`
- **Étape 2** : `PAGEtopage/step2_enrich/`
- **Étape 3** : `PAGEtopage/step3_export/`
- **Configuration** : `PAGEtopage/config.py`
- **CLI** : `PAGEtopage/cli.py`
- **Modèles** : `PAGEtopage/models.py`

### Outils Externes

- **CLTK** : https://cltk.org/
- **PageXML** : https://github.com/PRImA-Research-Lab/PAGE-XML
- **PyYAML** : https://pyyaml.org/
- **lxml** : https://lxml.de/

---

## 📝 Conclusion

Ce document établit le **lien conceptuel et technique** entre :

1. **Le schéma existant Module 5** (`flowchart-module5.mmd`) qui décrit le nettoyage post-eScriptorium
2. **Le nouveau dossier PAGEtopage** qui étend le pipeline avec l'enrichissement linguistique

**PAGEtopage** doit être considéré comme un **Module 6** à part entière, transformant les transcriptions XML PAGE finalisées en **corpus annotés linguistiquement exploitables**.

Le schéma Mermaid proposé dans ce document peut être sauvegardé comme `flowchart-module6-pagetopage.mmd` dans le dossier `Shema_module_projet/` pour compléter la documentation visuelle du pipeline.

---

**Dernière mise à jour** : Décembre 2024
**Auteur** : Équipe Data_Base
**Version** : 1.0
