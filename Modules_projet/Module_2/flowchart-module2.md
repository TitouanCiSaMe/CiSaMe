# Module2

> **Note**: Ce diagramme est également disponible en format image PNG dans le même dossier.

```mermaid
flowchart TD
    %% ========================================
    %% MODULE 2 - MÉTHODES DE TÉLÉCHARGEMENT
    %% ========================================
    %%
    %% Ce schéma présente les différentes méthodes pour télécharger
    %% des images de manuscrits depuis des bibliothèques numériques.
    %%
    %% Trois approches principales :
    %% 1. IIIF : Standard international, automatisé via manifest.json
    %% 2. PDF : Téléchargement direct puis extraction, qualité variable
    %% 3. Méthodes complexes : Manuel, Hexadécimal, ou par Tuiles
    %%
    %% Toutes convergent vers le stockage cloud Seafile pour
    %% centraliser les images avant traitement eScriptorium.
    %% ========================================

    START([📥 MODULE 2<br/>Méthodes de téléchargement])

    %% ========================================
    %% MÉTHODE IIIF
    %% ========================================
    subgraph IIIF_FLOW [🖼️ Méthode IIIF - International Image Interoperability Framework]
        IIIF_MANIFEST[🔍 Retrouver le<br/>manifest.json<br/>sur le site de la<br/>bibliothèque numérique]
        IIIF_ALGO[⚙️ Script Python<br/>download_images.py]
        IIIF_DL[📥 Téléchargement<br/>automatique]
        IIIF_RESULT[✅ Images de<br/>bonne qualité<br/>Format: JPG/PNG<br/>Résolution: 300-600 DPI]

        IIIF_MANIFEST --> IIIF_ALGO
        IIIF_ALGO --> IIIF_DL
        IIIF_DL --> IIIF_RESULT
    end

    %% ========================================
    %% MÉTHODE PDF
    %% ========================================
    subgraph PDF_FLOW [📄 Méthode PDF Direct]
        PDF_SITE[🌐 Téléchargement<br/>direct depuis site<br/>des bibliothèques<br/>numériques]
        PDF_DL[📥 Téléchargement<br/>du PDF]
        PDF_EXTRACT[📤 Extraction<br/>des images]
        PDF_RESULT[⚠️ Images de qualité<br/>variable<br/>Dépend du PDF source]

        PDF_SITE --> PDF_DL
        PDF_DL --> PDF_EXTRACT
        PDF_EXTRACT --> PDF_RESULT
    end

    %% ========================================
    %% MÉTHODES COMPLEXES
    %% ========================================
    subgraph COMPLEXE_FLOW [⚙️ Méthodes Complexes]
        COMPLEXE_DECISION{Type de<br/>méthode ?}

        %% Sous-branche Manuelle
        MANUEL[👤 Méthode Manuelle]
        MANUEL_DL[📥 Téléchargement<br/>manuel page par page<br/>clic droit + enregistrer]
        MANUEL_RESULT[⚠️ Images de qualité<br/>très disparates<br/>Chronophage]

        %% Sous-branche Hexadécimale
        HEXA[🔢 Méthode Hexadécimale]
        HEXA_ALGO[⚙️ Algorithme<br/>British_Library]
        HEXA_DL[📥 Téléchargement<br/>via URLs hexadécimales]
        HEXA_RESULT[✅ Images de très<br/>bonne qualité<br/>Résolution élevée]

        %% Sous-branche Tuiles
        TUILES[🧩 Méthode des Tuiles]
        TUILES_ALGO[⚙️ Algorithme perdu<br/>Reconstruction d'image<br/>à partir de tuiles]
        TUILES_DL[📥 Téléchargement<br/>et assemblage]
        TUILES_RESULT[⭐ Images d'extrêmement<br/>bonne qualité<br/>Haute résolution]

        COMPLEXE_DECISION -->|Manuel| MANUEL
        COMPLEXE_DECISION -->|Hexadécimal| HEXA
        COMPLEXE_DECISION -->|Tuiles| TUILES

        MANUEL --> MANUEL_DL
        MANUEL_DL --> MANUEL_RESULT

        HEXA --> HEXA_ALGO
        HEXA_ALGO --> HEXA_DL
        HEXA_DL --> HEXA_RESULT

        TUILES --> TUILES_ALGO
        TUILES_ALGO --> TUILES_DL
        TUILES_DL --> TUILES_RESULT
    end

    %% ========================================
    %% POINT DE CONVERGENCE
    %% ========================================
    CONVERGENCE[☁️ Service Cloud Universitaire<br/>SEAFILE<br/>Stockage centralisé]

    OUTPUT([📤 SORTIE MODULE 2<br/>Images prêtes pour traitement])

    %% ========================================
    %% CONNEXIONS PRINCIPALES
    %% ========================================
    START -->|Source: MODULE 1| IIIF_FLOW
    START -->|Source: MODULE 1| PDF_FLOW
    START -->|Source: MODULE 1| COMPLEXE_FLOW

    IIIF_RESULT -->|Export local → Cloud| CONVERGENCE
    PDF_RESULT -->|Export local → Cloud| CONVERGENCE
    MANUEL_RESULT -->|Export local → Cloud| CONVERGENCE
    HEXA_RESULT -->|Export local → Cloud| CONVERGENCE
    TUILES_RESULT -->|Export local → Cloud| CONVERGENCE

    CONVERGENCE --> OUTPUT

    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 IIIF:<br/>Méthode recommandée<br/>Standard international<br/>Automatisable]
    note2[💡 Méthode des Tuiles:<br/>Qualité maximale<br/>Complexe à implémenter<br/>Algorithme à recréer]
    note3[💡 British Library:<br/>Spécifique à certains sites<br/>Format hexadécimal des URLs<br/>Script Python disponible]
    note4[💡 Stockage Seafile:<br/>Organisé par ID manuscrit<br/>Métadonnées incluses<br/>Accès sécurisé]

    IIIF_RESULT -.-> note1
    TUILES_RESULT -.-> note2
    HEXA_RESULT -.-> note3
    CONVERGENCE -.-> note4

    %% ========================================
    %% COMPARAISON QUALITÉ
    %% ========================================
    subgraph QUALITY [📊 Comparaison Qualité]
        Q1[⭐⭐⭐⭐⭐ Tuiles - Excellente]
        Q2[⭐⭐⭐⭐ Hexadécimale - Très bonne]
        Q3[⭐⭐⭐ IIIF - Bonne]
        Q4[⭐⭐ PDF - Variable]
        Q5[⭐ Manuelle - Disparate]
    end

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef decision fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    classDef iiif fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef pdf fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef manuel fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    classDef hexa fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    classDef tuiles fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef convergence fill:#bbdefb,stroke:#1976d2,stroke-width:3px
    classDef note fill:#fff9c4,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5
    classDef excellent fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px
    classDef warning fill:#ffab91,stroke:#d84315,stroke-width:2px

    class START,OUTPUT startEnd
    class COMPLEXE_DECISION decision
    class IIIF_MANIFEST,IIIF_ALGO,IIIF_DL,IIIF_RESULT iiif
    class PDF_SITE,PDF_DL,PDF_EXTRACT,PDF_RESULT pdf
    class MANUEL,MANUEL_DL,MANUEL_RESULT manuel
    class HEXA,HEXA_ALGO,HEXA_DL,HEXA_RESULT hexa
    class TUILES,TUILES_ALGO,TUILES_DL,TUILES_RESULT tuiles
    class CONVERGENCE convergence
    class note1,note2,note3,note4 note
    class TUILES_RESULT,HEXA_RESULT excellent
    class PDF_RESULT,MANUEL_RESULT warning

    style IIIF_FLOW fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style PDF_FLOW fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style COMPLEXE_FLOW fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style QUALITY fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 3 3

```

---
*Généré automatiquement depuis `flowchart-module2.mmd`*
