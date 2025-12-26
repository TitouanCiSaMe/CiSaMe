# Module8 Diffusion

> **Note**: Ce diagramme est également disponible en format image PNG dans le même dossier.

```mermaid
flowchart TD
    %% ========================================
    %% MODULE 8 - DIFFUSION DES DONNÉES
    %% ========================================

    START([📤 MODULE 8<br/>Diffusion des Données Textuelles])

    %% ========================================
    %% ENTRÉE
    %% ========================================
    INPUT[📥 Entrée:<br/>Données textuelles<br/>depuis MODULE 6<br/>Format structuré]

    START --> INPUT

    %% ========================================
    %% DÉCISION TYPE DE PACKAGE
    %% ========================================
    DECISION_TYPE{Type de<br/>package ?}

    INPUT --> DECISION_TYPE

    %% ========================================
    %% BRANCHE AVEC IMAGES
    %% ========================================
    subgraph AVEC_IMAGES_FLOW [📷 Package Avec Images]
        AVEC_TITLE[Package complet<br/>Texte + Images]
        AVEC_CONTENU[📋 Contenu:<br/>• Conversion.log<br/>• images_mapping.txt<br/>• pages_index.json<br/>• Pages individuelles<br/>• texte_complet.txt<br/>• Images de chaque page]
        AVEC_DECISION{Droits de<br/>diffusion ?}

        AVEC_TITLE --> AVEC_CONTENU
        AVEC_CONTENU --> AVEC_DECISION
    end

    DECISION_TYPE -->|Avec images| AVEC_TITLE

    %% ========================================
    %% BRANCHE SANS IMAGES
    %% ========================================
    subgraph SANS_IMAGES_FLOW [📄 Package Sans Images]
        SANS_TITLE[Package texte seul]
        SANS_CONTENU[📋 Contenu:<br/>• Conversion.log<br/>• images_mapping.txt<br/>• pages_index.json<br/>• Pages individuelles<br/>• texte_complet.txt]
        SANS_DECISION{Droits de<br/>diffusion ?}

        SANS_TITLE --> SANS_CONTENU
        SANS_CONTENU --> SANS_DECISION
    end

    DECISION_TYPE -->|Sans images| SANS_TITLE

    %% ========================================
    %% DIFFUSION AVEC IMAGES - LIBRE
    %% ========================================
    subgraph AVEC_LIBRE_FLOW [✅ Avec Images - Libre de Droit]
        AVEC_LIBRE[Édition<br/>Libre de droit]
        AVEC_NAKALA_PREP[🔧 Préparation<br/>métadonnées Nakala]
        AVEC_NAKALA_CONNECT[🔗 Connecteur Nakala<br/>Upload automatisé]
        AVEC_NAKALA_RESULT[☁️ Publication sur Nakala<br/>DOI attribué<br/>Accès public]

        AVEC_LIBRE --> AVEC_NAKALA_PREP
        AVEC_NAKALA_PREP --> AVEC_NAKALA_CONNECT
        AVEC_NAKALA_CONNECT --> AVEC_NAKALA_RESULT
    end

    AVEC_DECISION -->|Libre| AVEC_LIBRE

    %% ========================================
    %% DIFFUSION AVEC IMAGES - RESTREINT
    %% ========================================
    subgraph AVEC_RESTREINT_FLOW [🔒 Avec Images - Droits Restreints]
        AVEC_RESTREINT[Édition<br/>Pas libre de droit]
        AVEC_SEAFILE[☁️ Stockage Seafile<br/>Accès restreint<br/>Usage recherche uniquement]

        AVEC_RESTREINT --> AVEC_SEAFILE
    end

    AVEC_DECISION -->|Restreint| AVEC_RESTREINT

    %% ========================================
    %% DIFFUSION SANS IMAGES - LIBRE
    %% ========================================
    subgraph SANS_LIBRE_FLOW [✅ Sans Images - Libre de Droit]
        SANS_LIBRE[Édition<br/>Libre de droit]
        SANS_NAKALA_PREP[🔧 Préparation<br/>métadonnées Nakala]
        SANS_NAKALA_CONNECT[🔗 Connecteur Nakala<br/>Upload automatisé]
        SANS_NAKALA_RESULT[☁️ Publication sur Nakala<br/>DOI attribué<br/>Accès public]

        SANS_LIBRE --> SANS_NAKALA_PREP
        SANS_NAKALA_PREP --> SANS_NAKALA_CONNECT
        SANS_NAKALA_CONNECT --> SANS_NAKALA_RESULT
    end

    SANS_DECISION -->|Libre| SANS_LIBRE

    %% ========================================
    %% DIFFUSION SANS IMAGES - RESTREINT
    %% ========================================
    subgraph SANS_RESTREINT_FLOW [🔒 Sans Images - Droits Restreints]
        SANS_RESTREINT[Édition<br/>Pas libre de droit]
        SANS_SEAFILE[☁️ Stockage Seafile<br/>Accès restreint<br/>Usage recherche uniquement]

        SANS_RESTREINT --> SANS_SEAFILE
    end

    SANS_DECISION -->|Restreint| SANS_RESTREINT

    %% ========================================
    %% CONVERGENCE
    %% ========================================
    CONVERGENCE[📦 Données diffusées<br/>selon droits applicables]

    AVEC_NAKALA_RESULT --> CONVERGENCE
    AVEC_SEAFILE --> CONVERGENCE
    SANS_NAKALA_RESULT --> CONVERGENCE
    SANS_SEAFILE --> CONVERGENCE

    OUTPUT([📤 SORTIE MODULE 8<br/>Corpus accessible<br/>Valorisation recherche])

    CONVERGENCE --> OUTPUT

    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 Avec/Sans Images:<br/>Choix selon droits<br/>et objectif de diffusion<br/>Images augmentent valeur]
    note2[💡 Nakala:<br/>Plateforme Huma-Num<br/>Archivage pérenne<br/>DOI et métadonnées]
    note3[💡 Connecteur Nakala:<br/>Upload automatisé via API<br/>Gestion métadonnées<br/>Attribution DOI]
    note4[💡 Seafile:<br/>Stockage cloud sécurisé<br/>Accès contrôlé<br/>Usage recherche interne]
    note5[💡 Droits:<br/>Libre: Domaine public<br/>Restreint: Droits d'auteur<br/>Décision selon MODULE 3]

    DECISION_TYPE -.-> note1
    AVEC_NAKALA_RESULT -.-> note2
    AVEC_NAKALA_CONNECT -.-> note3
    AVEC_SEAFILE -.-> note4
    AVEC_DECISION -.-> note5

    %% ========================================
    %% STATISTIQUES
    %% ========================================
    subgraph STATS [📊 Statistiques Indicatives]
        S1[~30% éditions libres → Nakala]
        S2[~68% éditions restreintes → Seafile]
        S3[~2% éditions secrètes → Seafile]
        S4[Format: JSON + TXT structuré]
    end

    %% ========================================
    %% OUTILS
    %% ========================================
    subgraph TOOLS [🛠️ Outils Utilisés]
        T1[Connecteur Nakala: API Huma-Num]
        T2[Seafile: Cloud universitaire]
        T3[Python: Scripts automatisation]
    end

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef decision fill:#ffeb3b,stroke:#f57f17,stroke-width:3px
    classDef avec fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef sans fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef libre fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef restreint fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    classDef nakala fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px
    classDef seafile fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef convergence fill:#bbdefb,stroke:#1976d2,stroke-width:3px
    classDef note fill:#fff9c4,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5
    classDef title fill:#e0e0e0,stroke:#757575,stroke-width:2px

    class START,OUTPUT startEnd
    class INPUT input
    class DECISION_TYPE,AVEC_DECISION,SANS_DECISION decision
    class AVEC_TITLE,AVEC_CONTENU avec
    class SANS_TITLE,SANS_CONTENU sans
    class AVEC_LIBRE,AVEC_NAKALA_PREP,AVEC_NAKALA_CONNECT,AVEC_NAKALA_RESULT,SANS_LIBRE,SANS_NAKALA_PREP,SANS_NAKALA_CONNECT,SANS_NAKALA_RESULT libre
    class AVEC_RESTREINT,AVEC_SEAFILE,SANS_RESTREINT,SANS_SEAFILE restreint
    class CONVERGENCE convergence
    class note1,note2,note3,note4,note5 note

    style AVEC_IMAGES_FLOW fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style SANS_IMAGES_FLOW fill:#fff8e1,stroke:#f57f17,stroke-width:2px
    style AVEC_LIBRE_FLOW fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style AVEC_RESTREINT_FLOW fill:#ffebee,stroke:#c62828,stroke-width:2px
    style SANS_LIBRE_FLOW fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style SANS_RESTREINT_FLOW fill:#ffebee,stroke:#c62828,stroke-width:2px
    style STATS fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 3 3
    style TOOLS fill:#e0f2f1,stroke:#00796b,stroke-width:2px,stroke-dasharray: 3 3

```

---
*Généré automatiquement depuis `flowchart-module8-diffusion.mmd`*
