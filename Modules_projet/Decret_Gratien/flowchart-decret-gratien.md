# Decret Gratien

> **Note**: Ce diagramme est également disponible en format image PNG dans le même dossier.

```mermaid
flowchart TD
    %% ========================================
    %% MODULE SPÉCIAL - DÉCRET DE GRATIEN
    %% ========================================

    START([⚖️ MODULE SPÉCIAL<br/>Décret de Gratien])

    %% ========================================
    %% ENTRÉES PARALLÈLES
    %% ========================================
    INPUT1[📥 Entrée 1:<br/>XML Pages depuis MODULE 4<br/>Transcriptions brutes]
    INPUT2[📥 Entrée 2:<br/>Version finale MODULE 5<br/>Transcriptions nettoyées]

    START --> INPUT1
    START --> INPUT2

    %% ========================================
    %% BRANCHE 1 - ALLÉGATIONS
    %% ========================================
    subgraph ALLEGATIONS_FLOW [📊 Workflow Allégations]
        AL_SOURCE[📚 Source:<br/>Ochoa et Diez<br/>Recueil d'Allégations<br/>historique]
        AL_ALGO[⚙️ Algorithme<br/>d'extraction]
        AL_CSV_BRUT[📄 CSV Brut:<br/>Numéro allégation<br/>+ suffixe]
        AL_AJOUT_ID[🔢 Ajout d'ID unique<br/>pour chaque allégation]
        AL_AJOUT_MANUEL[✍️ Ajout manuel<br/>d'allégations manquantes<br/>non détectées automatiquement]
        AL_CORRECTION[✍️ Correction et<br/>Enrichissement<br/>des allégations]
        AL_VALIDATION[✅ Validation<br/>des données]
        AL_FINAL[📊 Allégations.csv<br/>Version finale]

        AL_SOURCE --> AL_ALGO
        AL_ALGO --> AL_CSV_BRUT
        AL_CSV_BRUT --> AL_AJOUT_ID
        AL_AJOUT_ID --> AL_AJOUT_MANUEL
        AL_AJOUT_MANUEL --> AL_CORRECTION
        AL_CORRECTION --> AL_VALIDATION
        AL_VALIDATION --> AL_FINAL
    end

    INPUT1 --> AL_SOURCE

    %% ========================================
    %% BRANCHE 2 - FRIEDBERG & MÜNCHENER
    %% ========================================
    subgraph FRIEDBERG_FLOW [📖 Workflow Friedberg & Münchener]
        FR_SOURCE1[📄 XML Page + Images<br/>Décret de Gratien<br/>Édition Friedberg]
        FR_SOURCE2[🌐 Site Web:<br/>Münchener Digitale<br/>Bibliothek]

        FR_MERGE[🔗 Fusion des sources<br/>Texte intégral<br/>de la version]

        FR_EXTRACTION[📤 Extraction<br/>de tous les canons<br/>au format .txt]

        FR_REPARTITION[📁 Répartition des canons<br/>dans dossiers/sous-dossiers<br/>selon logique du Décret]

        FR_STRUCTURE[🗂️ Structure hiérarchique:<br/>Parties → Distinctions →<br/>Causae → Quaestiones]

        FR_AJOUT_ID[🔢 Ajout ID correspondant<br/>pour chaque canon<br/>selon Allégations.csv]

        FR_ENRICHISSEMENT[✨ Enrichissement<br/>métadonnées]

        FR_VALIDATION[✅ Validation<br/>structure + contenu]

        FR_FINAL[⚖️ Décret de Gratien<br/>enrichi et structuré]

        FR_SOURCE1 --> FR_MERGE
        FR_SOURCE2 --> FR_MERGE
        FR_MERGE --> FR_EXTRACTION
        FR_EXTRACTION --> FR_REPARTITION
        FR_REPARTITION --> FR_STRUCTURE
        FR_STRUCTURE --> FR_AJOUT_ID
        FR_AJOUT_ID --> FR_ENRICHISSEMENT
        FR_ENRICHISSEMENT --> FR_VALIDATION
        FR_VALIDATION --> FR_FINAL
    end

    INPUT2 --> FR_SOURCE1

    %% ========================================
    %% CONNEXION ENTRE LES BRANCHES
    %% ========================================
    AL_FINAL -->|Mapping ID| FR_AJOUT_ID

    %% ========================================
    %% SORTIE FINALE
    %% ========================================
    CONVERGENCE[📦 Données enrichies<br/>Décret de Gratien complet]

    FR_FINAL --> CONVERGENCE
    AL_FINAL -.->|Données référence| CONVERGENCE

    OUTPUT([🎯 SORTIE FINALE<br/>Corpus Décret de Gratien])

    CONVERGENCE --> OUTPUT



    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 Ochoa et Diez:<br/>Référence académique<br/>Catalogue des sources<br/>du Décret]
    note2[💡 Friedberg:<br/>Édition critique standard<br/>1879-1881<br/>Corpus Iuris Canonici]
    note3[💡 Münchener:<br/>Version numérisée<br/>Accès web gratuit<br/>Texte extractible]
    note4[💡 Algorithme extraction:<br/>Parsing intelligent<br/>Reconnaissance structure<br/>Python + Regex]
    note5[💡 ID unique:<br/>Traçabilité complète<br/>Lien allégation ↔ canon<br/>Format: Grat_XXXX]
    note6[💡 Structure dossiers:<br/>Parties → Distinctions →<br/>Causae → Quaestiones<br/>Hiérarchie logique du Décret]

    AL_SOURCE -.-> note1
    FR_SOURCE1 -.-> note2
    FR_SOURCE2 -.-> note3
    AL_ALGO -.-> note4
    AL_AJOUT_ID -.-> note5
    FR_STRUCTURE -.-> note6

    %% ========================================
    %% STATISTIQUES
    %% ========================================
    subgraph STATS [📊 Statistiques Indicatives]
        S1[~4000 canons dans le Décret]
        S2[~3800 allégations recensées]
        S3[~150 distinctions au total]
        S4[~36 causae avec ~150 quaestiones]
        S5[+ Cause 33 Quaestio 3:<br/>7 distinctions spéciales]
        S6[4149 fichiers .txt générés]
        S7[Taille texte: 5 Mo]
    end

    %% ========================================
    %% OUTILS
    %% ========================================
    subgraph TOOLS [🛠️ Outils Utilisés]
        T1[Python: Scripts extraction]
        T2[BeautifulSoup: Scraping web]
        T3[Pandas: Manipulation CSV]
        T4[lxml: Traitement XML]
        T5[Regex: Parsing texte]
    end

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef allegations fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef friedberg fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px
    classDef source fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    classDef algorithme fill:#ffccbc,stroke:#d84315,stroke-width:2px
    classDef validation fill:#b2dfdb,stroke:#00796b,stroke-width:2px
    classDef final fill:#a5d6a7,stroke:#2e7d32,stroke-width:3px
    classDef convergence fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    classDef note fill:#fff9c4,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5
    classDef title fill:#e0e0e0,stroke:#757575,stroke-width:2px

    class START,OUTPUT startEnd
    class INPUT1,INPUT2 input
    class AL_SOURCE,AL_CSV_BRUT,AL_AJOUT_ID,AL_AJOUT_MANUEL,AL_CORRECTION,AL_FINAL allegations
    class FR_SOURCE1,FR_SOURCE2,FR_MERGE,FR_EXTRACTION,FR_REPARTITION,FR_STRUCTURE,FR_AJOUT_ID,FR_ENRICHISSEMENT,FR_FINAL friedberg
    class AL_ALGO,FR_MERGE algorithme
    class AL_VALIDATION,FR_VALIDATION validation
    class AL_FINAL,FR_FINAL final
    class CONVERGENCE convergence
    class note1,note2,note3,note4,note5,note6 note

    style ALLEGATIONS_FLOW fill:#fff8e1,stroke:#f57f17,stroke-width:2px
    style FRIEDBERG_FLOW fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style STATS fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 3 3
    style TOOLS fill:#e0f2f1,stroke:#00796b,stroke-width:2px,stroke-dasharray: 3 3

```

---
*Généré automatiquement depuis `flowchart-decret-gratien.mmd`*
