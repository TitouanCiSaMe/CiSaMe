# Metadonnees

> **Note**: Ce diagramme est également disponible en format image PNG dans le même dossier.

```mermaid
flowchart TD
    %% ========================================
    %% MODULE MÉTADONNÉES
    %% ========================================

    START([📋 MODULE MÉTADONNÉES<br/>Gestion des Fiches Descriptives])

    %% ========================================
    %% ENTRÉE
    %% ========================================
    INPUT[📥 Entrée:<br/>Fiches de métadonnées<br/>Documents sources<br/>Catalogues historiques]

    START --> INPUT

    %% ========================================
    %% CONTENU FICHES
    %% ========================================
    subgraph CONTENU_FLOW [📄 Contenu des Fiches]
        CONTENU_TITLE[Informations collectées]
        CONTENU_OEUVRE["🔸 Oeuvre:<br/>• Titre<br/>• Auteur(s)<br/>• Date/période rédaction<br/>• Lieu/aire géographique<br/>• Type de texte"]
        CONTENU_EDITION[🔸 Édition:<br/>• Titre édition<br/>• Éditeur scientifique<br/>• Maison d'édition/Collection<br/>• Lieu et date d'édition<br/>• Pagination<br/>• Remarques<br/>• Bibliographie]

        CONTENU_TITLE --> CONTENU_OEUVRE
        CONTENU_TITLE --> CONTENU_EDITION
    end

    INPUT --> CONTENU_TITLE

    %% ========================================
    %% EXTRACTION
    %% ========================================
    EXTRACTION[⚙️ Extraction et<br/>Structuration<br/>des informations]

    CONTENU_OEUVRE --> EXTRACTION
    CONTENU_EDITION --> EXTRACTION

    %% ========================================
    %% TABLES RELATIONNELLES
    %% ========================================
    subgraph TABLES_FLOW [🗃️ Tables Relationnelles]
        TABLES_TITLE[Modèle de données]

        TABLE_AUTEURS[📊 Table AUTEURS<br/>Métadonnées:<br/>• ID auteur unique<br/>• Nom<br/>• Alias]

        TABLE_OEUVRES[📊 Table OEUVRES<br/>Métadonnées:<br/>• ID oeuvre unique<br/>• Titre<br/>• ID auteur ref<br/>• Date/période rédaction<br/>• Lieu/aire géographique<br/>• Auteur de la notice<br/>• Type]

        TABLE_EDITIONS[📊 Table ÉDITIONS<br/>Métadonnées:<br/>• ID édition unique<br/>• Titre édition<br/>• Éditeur scientifique<br/>• Maison/Collection<br/>• Lieu/date édition<br/>• Pagination<br/>• Remarques<br/>• Auteur de la notice<br/>• ID oeuvre ref<br/>• Type]

        TABLES_TITLE --> TABLE_AUTEURS
        TABLES_TITLE --> TABLE_OEUVRES
        TABLES_TITLE --> TABLE_EDITIONS
    end

    EXTRACTION --> TABLES_TITLE

    %% ========================================
    %% LIENS RELATIONNELS
    %% ========================================
    RELATIONS[🔗 Relations entre tables<br/>via clés étrangères]

    TABLE_AUTEURS -.->|ID auteur| TABLE_OEUVRES
    TABLE_OEUVRES -.->|ID oeuvre| TABLE_EDITIONS

    TABLE_AUTEURS --> RELATIONS
    TABLE_OEUVRES --> RELATIONS
    TABLE_EDITIONS --> RELATIONS

    %% ========================================
    %% BASE DE DONNÉES HEURIST
    %% ========================================
    subgraph HEURIST_FLOW [🏛️ Base de Données Heurist]
        HEURIST_TITLE[Système de gestion]
        HEURIST_IMPORT[📥 Import des tables<br/>dans Heurist]
        HEURIST_VALIDATION[✅ Validation<br/>intégrité référentielle]
        HEURIST_INTERFACE[🖥️ Interface web<br/>Consultation et recherche]
        HEURIST_EXPORT[📤 Export formats<br/>multiples: JSON, CSV, XML]

        HEURIST_TITLE --> HEURIST_IMPORT
        HEURIST_IMPORT --> HEURIST_VALIDATION
        HEURIST_VALIDATION --> HEURIST_INTERFACE
        HEURIST_INTERFACE --> HEURIST_EXPORT
    end

    RELATIONS --> HEURIST_TITLE

    %% ========================================
    %% SORTIE
    %% ========================================
    OUTPUT([📤 SORTIE MODULE MÉTADONNÉES<br/>Base structurée et consultable<br/>Traçabilité complète])

    HEURIST_EXPORT --> OUTPUT

    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 Fiches sources:<br/>Documents collectés<br/>durant la recherche<br/>Catalogues bibliothèques]
    note2[💡 Structure 3 tables:<br/>Normalisation données<br/>Évite redondances<br/>Flexibilité recherches]
    note3[💡 Clés étrangères:<br/>AUTEURS → OEUVRES<br/>OEUVRES → ÉDITIONS<br/>Intégrité garantie]
    note4[💡 Heurist:<br/>Base données académique<br/>Spécialisée SHS<br/>Interface paramétrable]
    note5[💡 Utilité:<br/>Traçabilité des sources<br/>Recherche multicritère<br/>Export pour publications]

    INPUT -.-> note1
    TABLES_TITLE -.-> note2
    RELATIONS -.-> note3
    HEURIST_TITLE -.-> note4
    OUTPUT -.-> note5

    %% ========================================
    %% STATISTIQUES
    %% ========================================
    subgraph STATS [📊 Statistiques Indicatives]
        S1[~5768 records référencés]
        S2[~129 éditions documentées]
        S3[~200 auteurs médiévaux]
        S4[Format: Base Heurist + exports]
    end

    %% ========================================
    %% OUTILS
    %% ========================================
    subgraph TOOLS [🛠️ Outils Utilisés]
        T1[Heurist: Base de données SHS]
        T2[Python: Scripts extraction]
        T3[Export: JSON, CSV, XML]
    end

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef contenu fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef extraction fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef tables fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    classDef relations fill:#b2dfdb,stroke:#00796b,stroke-width:2px
    classDef heurist fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef result fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px
    classDef note fill:#fff9c4,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5
    classDef title fill:#e0e0e0,stroke:#757575,stroke-width:2px

    class START,OUTPUT startEnd
    class INPUT input
    class CONTENU_TITLE,CONTENU_OEUVRE,CONTENU_EDITION contenu
    class EXTRACTION extraction
    class TABLES_TITLE,TABLE_AUTEURS,TABLE_OEUVRES,TABLE_EDITIONS tables
    class RELATIONS relations
    class HEURIST_TITLE,HEURIST_IMPORT,HEURIST_VALIDATION,HEURIST_INTERFACE,HEURIST_EXPORT heurist
    class note1,note2,note3,note4,note5 note

    style CONTENU_FLOW fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style TABLES_FLOW fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style HEURIST_FLOW fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style STATS fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 3 3
    style TOOLS fill:#e0f2f1,stroke:#00796b,stroke-width:2px,stroke-dasharray: 3 3

```

---
*Généré automatiquement depuis `flowchart-metadonnees.mmd`*
