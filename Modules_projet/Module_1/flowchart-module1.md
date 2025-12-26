# Module1

> **Note**: Ce diagramme est également disponible en format image PNG dans le même dossier.

```mermaid
flowchart TD
    %% ========================================
    %% MODULE 1 - RÉCUPÉRATION DE MANUSCRITS
    %% ========================================

    START([📜 MODULE 1<br/>Récupération de manuscrits])

    %% ========================================
    %% DÉCISION PRINCIPALE
    %% ========================================
    DECISION{Quelle source ?}

    START --> DECISION

    %% ========================================
    %% BRANCHE ACHAT
    %% ========================================
    subgraph ACHAT_FLOW [💰 Processus d'Achat]
        ACHAT_DECISION{Déjà<br/>numérisé ?}
        ACHAT_OUI[✅ Manuscrits déjà<br/>numérisés]
        ACHAT_NON[❌ Manuscrits pas<br/>numérisés]
        ACHAT_NUMERISATION[🖨️ Numérisation<br/>par bibliothèque/organisme]
        ACHAT_RESULT[📦 Manuscrits<br/>numérisés reçus]

        ACHAT_DECISION -->|Oui| ACHAT_OUI
        ACHAT_DECISION -->|Non| ACHAT_NON
        ACHAT_NON --> ACHAT_NUMERISATION
        ACHAT_NUMERISATION --> ACHAT_RESULT
        ACHAT_OUI --> ACHAT_RESULT
    end

    %% ========================================
    %% BRANCHE SCRAPING WEB
    %% ========================================
    subgraph SCRAPING_FLOW [🌐 Scraping Web]
        SCRAPING_DECISION{Méthode<br/>disponible ?}
        SCRAPING_IIIF[🖼️ IIIF]
        SCRAPING_PDF[📄 PDF direct<br/>sur site web]
        SCRAPING_COMPLEXE[⚙️ Méthodes<br/>complexes]

        SCRAPING_DECISION -->|IIIF manifest| SCRAPING_IIIF
        SCRAPING_DECISION -->|PDF disponible| SCRAPING_PDF
        SCRAPING_DECISION -->|Autre| SCRAPING_COMPLEXE
    end

    %% ========================================
    %% POINT DE CONVERGENCE
    %% ========================================
    CONVERGENCE[✨ Numérisation de très bonne qualité<br/>Format: TIF, Résolution: 300-600 DPI]

    OUTPUT([📤 SORTIE MODULE 1<br/>Vers Stockage Cloud])

    %% ========================================
    %% CONNEXIONS PRINCIPALES
    %% ========================================
    DECISION -->|Achat| ACHAT_DECISION
    DECISION -->|Scraping| SCRAPING_DECISION

    ACHAT_RESULT --> CONVERGENCE
    SCRAPING_IIIF -.->|Voir MODULE 2| CONVERGENCE
    SCRAPING_PDF -.->|Voir MODULE 2| CONVERGENCE
    SCRAPING_COMPLEXE -.->|Voir MODULE 2| CONVERGENCE

    CONVERGENCE --> OUTPUT

    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 Scraping:<br/>Gratuit mais complexe<br/>Légalité à vérifier]
    note2[💡 Qualité requise:<br/>Minimum 300 DPI<br/>Format TIF recommandé]

    SCRAPING_COMPLEXE -.-> note1
    CONVERGENCE -.-> note2

    %% ========================================
    %% LIENS VERS AUTRES MODULES
    %% ========================================
    link1[🔗 MODULE 2:<br/>Détails téléchargement]

    SCRAPING_COMPLEXE -.->|Pour plus de détails| link1

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef decision fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    classDef achat fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    classDef scraping fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px
    classDef convergence fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    classDef note fill:#ffccbc,stroke:#d84315,stroke-width:1px,stroke-dasharray: 5 5
    classDef link fill:#e0e0e0,stroke:#757575,stroke-width:1px,stroke-dasharray: 3 3

    class START,OUTPUT startEnd
    class DECISION,ACHAT_DECISION,SCRAPING_DECISION decision
    class ACHAT_OUI,ACHAT_NON,ACHAT_NUMERISATION,ACHAT_RESULT achat
    class SCRAPING_IIIF,SCRAPING_PDF,SCRAPING_COMPLEXE scraping
    class CONVERGENCE convergence
    class note1,note2 note
    class link1 link

    style ACHAT_FLOW fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style SCRAPING_FLOW fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px

```

---
*Généré automatiquement depuis `flowchart-module1.mmd`*
