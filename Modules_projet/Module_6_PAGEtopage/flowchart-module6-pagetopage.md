# Module6 Pagetopage

> **Note**: Ce diagramme est également disponible en format image PNG dans le même dossier.

```mermaid
flowchart TD
    %% ========================================
    %% MODULE 6 - ENRICHISSEMENT LINGUISTIQUE (PAGEtopage)
    %% CAS GÉNÉRAL : Manuscrits et Éditions
    %% N'UTILISE PAS pour le Décret de Gratien
    %% ========================================

    START([📦 MODULE 6<br/>PAGEtopage - Enrichissement Linguistique<br/>Pipeline en 4 étapes<br/>Cas général uniquement])

    %% ENTRÉE
    INPUT_MODULE5[📥 XML PAGE finalisés<br/>Sortie du Module 5<br/>Manuscrits/Éditions génériques]
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

        TREETAGGER_PROCESS[🧠 Traitement TreeTagger<br/>Lemmatisation + POS-tagging<br/>Installation automatique]

        VERTICAL_FORMAT[📊 Format Vertical<br/>Mot / POS / Lemme]

        CORPUS_VERTICAL[💾 corpus.vertical.txt<br/>Fichier annoté complet]

        ENRICH_START --> SENTENCE_SPLIT
        SENTENCE_SPLIT --> TOKENIZATION
        TOKENIZATION --> TREETAGGER_PROCESS
        TREETAGGER_PROCESS --> VERTICAL_FORMAT
        VERTICAL_FORMAT --> CORPUS_VERTICAL
    end

    JSON_INTERMEDIATE --> ENRICH_START

    %% ========================================
    %% ÉTAPE 3 : EXPORT
    %% ========================================
    subgraph STEP3 [📤 ÉTAPE 3 : Export]
        EXPORT_START[📖 Lecture corpus vertical]

        FORMAT_CHOICE{Format de sortie ?}

        FORMAT_SCHOLARLY[🎓 Scholarly<br/>Format académique<br/>Recommandé]
        FORMAT_CLEAN[✨ Clean<br/>Texte brut lisible]
        FORMAT_DIPLO[📝 Diplomatic<br/>Avec annotations inline]
        FORMAT_ANNOT[📊 Annotated<br/>Format tabulaire]

        PAGE_SPLIT[📑 Séparation par pages<br/>Un fichier par page]

        COMBINED_FILE[📘 Fichier texte complet<br/>texte_complet.txt]

        INDEX_JSON[🗂️ Index des pages<br/>pages_index.json]

        STATS_JSON[📊 Statistiques corpus<br/>corpus_stats.json]

        IMAGE_MAPPING[🖼️ Correspondance images<br/>images_mapping.txt]

        EXPORT_START --> FORMAT_CHOICE
        FORMAT_CHOICE -->|scholarly| FORMAT_SCHOLARLY
        FORMAT_CHOICE -->|clean| FORMAT_CLEAN
        FORMAT_CHOICE -->|diplomatic| FORMAT_DIPLO
        FORMAT_CHOICE -->|annotated| FORMAT_ANNOT

        FORMAT_SCHOLARLY --> PAGE_SPLIT
        FORMAT_CLEAN --> PAGE_SPLIT
        FORMAT_DIPLO --> PAGE_SPLIT
        FORMAT_ANNOT --> PAGE_SPLIT

        PAGE_SPLIT --> COMBINED_FILE
        PAGE_SPLIT --> INDEX_JSON
        PAGE_SPLIT --> STATS_JSON
        PAGE_SPLIT --> IMAGE_MAPPING
    end

    CORPUS_VERTICAL --> EXPORT_START

    %% ========================================
    %% ÉTAPE 4 : RÉ-ENRICHISSEMENT (OPTIONNEL)
    %% ========================================
    subgraph STEP4 [🔄 ÉTAPE 4 : Ré-enrichissement<br/>Optionnel]
        CORRECTION[✏️ Correction manuelle<br/>Édition des fichiers texte<br/>Coquilles, erreurs OCR]

        REENRICH_START[📖 Lecture fichiers corrigés<br/>Format scholarly]

        PARSE_SCHOLARLY[🔍 Parse format scholarly<br/>Extraction texte + métadonnées]

        RETOKENIZE[🔤 Re-tokenisation<br/>Nouveau découpage]

        RELEMMATIZE[🧠 Re-lemmatisation<br/>TreeTagger sur texte corrigé]

        CORPUS_VERTICAL_CORRECTED[💾 corpus_corrige.vertical.txt<br/>Fichier vertical avec corrections]

        CORRECTION --> REENRICH_START
        REENRICH_START --> PARSE_SCHOLARLY
        PARSE_SCHOLARLY --> RETOKENIZE
        RETOKENIZE --> RELEMMATIZE
        RELEMMATIZE --> CORPUS_VERTICAL_CORRECTED
    end

    PAGE_SPLIT -.->|Optionnel: Si corrections nécessaires| CORRECTION

    %% SORTIE FINALE
    OUTPUT([📤 SORTIE MODULE 6<br/>Corpus enrichi + Fichiers exploitables])

    CORPUS_VERTICAL --> OUTPUT
    CORPUS_VERTICAL_CORRECTED -.-> OUTPUT
    COMBINED_FILE --> OUTPUT
    INDEX_JSON --> OUTPUT
    STATS_JSON --> OUTPUT
    IMAGE_MAPPING --> OUTPUT

    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 Configuration:<br/>config.yaml définit<br/>tous les paramètres<br/>du traitement]
    note2[💡 TreeTagger:<br/>Installation automatique<br/>~20 MB téléchargés<br/>Première fois seulement]
    note3[💡 Formats:<br/>Scholarly = académique recommandé<br/>Clean = lecture humaine<br/>Diplomatic = semi-annoté<br/>Annotated = analyse machine]
    note4[💡 Pipeline:<br/>3 étapes obligatoires<br/>+ 1 étape optionnelle<br/>Exécution complète ou séparée]
    note5[⚠️ IMPORTANT:<br/>Module pour CAS GÉNÉRAL<br/>N'utilise PAS pour Décret<br/>Décret = pipeline spécifique]
    note6[💡 Ré-enrichissement:<br/>Permet de corriger<br/>les coquilles dans le texte<br/>puis regénérer le vertical]

    EXTRACT_START -.-> note1
    TREETAGGER_PROCESS -.-> note2
    FORMAT_CHOICE -.-> note3
    START -.-> note4
    INPUT_MODULE5 -.-> note5
    CORRECTION -.-> note6

    %% ========================================
    %% STATISTIQUES
    %% ========================================
    subgraph STATS [📊 Caractéristiques Techniques]
        S1[Langues supportées: Latin, Français]
        S2[Lemmatiseur: TreeTagger installation automatique]
        S3[Formats sortie: 4 formats configurables]
        S4[Dépendances: Python 3.10+, PyYAML, treetaggerwrapper]
        S5[Étapes: 3 obligatoires + 1 optionnelle correction]
    end

    %% ========================================
    %% OUTILS
    %% ========================================
    subgraph TOOLS [🛠️ Technologies Utilisées]
        T1[Python 3.10+: Langage principal]
        T2[TreeTagger: Lemmatisation et POS-tagging]
        T3[PyYAML: Configuration]
        T4[lxml: Manipulation XML]
        T5[JSON: Formats intermédiaires]
        T6[Argparse: Interface CLI]
    end

    %% ========================================
    %% COMMANDES CLI
    %% ========================================
    subgraph CLI [💻 Commandes Disponibles]
        CMD1[run: Pipeline complet 3 étapes]
        CMD2[extract: Étape 1 seule]
        CMD3[enrich: Étape 2 seule]
        CMD4[export: Étape 3 seule]
        CMD5[re-enrich: Étape 4 ré-enrichissement]
        CMD6[init: Génère config.yaml]
    end

    %% ========================================
    %% FLUX DE DONNÉES
    %% ========================================
    subgraph DATA_FLOW [🔄 Formats de Données]
        DF1[Entrée: XML PAGE<br/>Format eScriptorium/Transkribus]
        DF2[Intermédiaire 1: JSON<br/>Texte extrait + métadonnées]
        DF3[Intermédiaire 2: Vertical<br/>Annotations linguistiques]
        DF4[Sortie: TXT + JSON<br/>Formats exploitables]
    end

    %% ========================================
    %% LIEN AVEC MODULE 5
    %% ========================================
    MODULE5_OUTPUT[📤 MODULE 5<br/>Transcriptions XML finalisées<br/>Cas général: Manuscrits/Éditions<br/>Exclus: Décret de Gratien]
    MODULE5_OUTPUT --> INPUT_MODULE5

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef decision fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    classDef extract fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef enrich fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    classDef export fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef reenrich fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef intermediate fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef output fill:#a5d6a7,stroke:#2e7d32,stroke-width:3px
    classDef note fill:#fff9c4,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5
    classDef module5 fill:#b3e5fc,stroke:#01579b,stroke-width:2px

    class START,OUTPUT startEnd
    class COLUMN_DECISION,FORMAT_CHOICE decision
    class EXTRACT_START,SINGLE_COL,DUAL_COL,HYPHEN_MERGE extract
    class ENRICH_START,SENTENCE_SPLIT,TOKENIZATION,TREETAGGER_PROCESS,VERTICAL_FORMAT enrich
    class EXPORT_START,FORMAT_SCHOLARLY,FORMAT_CLEAN,FORMAT_DIPLO,FORMAT_ANNOT,PAGE_SPLIT export
    class CORRECTION,REENRICH_START,PARSE_SCHOLARLY,RETOKENIZE,RELEMMATIZE reenrich
    class JSON_INTERMEDIATE,CORPUS_VERTICAL,CORPUS_VERTICAL_CORRECTED intermediate
    class COMBINED_FILE,INDEX_JSON,STATS_JSON,IMAGE_MAPPING output
    class note1,note2,note3,note4,note5,note6 note
    class MODULE5_OUTPUT,INPUT_MODULE5 module5

    style STEP1 fill:#e8f5e9,stroke:#1565c0,stroke-width:2px
    style STEP2 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style STEP3 fill:#fff8e1,stroke:#e65100,stroke-width:2px
    style STEP4 fill:#e0f7fa,stroke:#0277bd,stroke-width:2px,stroke-dasharray: 5 5
    style STATS fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 3 3
    style TOOLS fill:#e0f2f1,stroke:#00796b,stroke-width:2px,stroke-dasharray: 3 3
    style CLI fill:#fce4ec,stroke:#c2185b,stroke-width:2px,stroke-dasharray: 3 3
    style DATA_FLOW fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,stroke-dasharray: 3 3

```

---
*Généré automatiquement depuis `flowchart-module6-pagetopage.mmd`*
