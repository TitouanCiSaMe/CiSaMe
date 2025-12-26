# Module3

> **Note**: Ce diagramme est également disponible en format image PNG dans le même dossier.

```mermaid
flowchart TD
    %% ========================================
    %% MODULE 3 - RÉCUPÉRATION D'ÉDITIONS
    %% ========================================

    START([📚 MODULE 3<br/>Récupération d'éditions de manuscrits])

    %% ========================================
    %% DÉCISION PRINCIPALE
    %% ========================================
    DECISION{Quelle source<br/>d'acquisition ?}

    START --> DECISION

    %% ========================================
    %% SOURCES D'ACQUISITION
    %% ========================================
    subgraph SOURCES [📥 Sources d'Acquisition]
        LIBRE[🌐 Récupération<br/>libre de droit<br/>sur Internet]
        INFORMEL[🤝 Récupération<br/>informelle<br/>Contacts personnels]
        PRET[🏛️ Prêt de<br/>Bibliothèque]
        ACHAT[💰 Achat<br/>d'Édition]
    end

    DECISION -->|Gratuit en ligne| LIBRE
    DECISION -->|Contact direct| INFORMEL
    DECISION -->|Prêt| PRET
    DECISION -->|Achat| ACHAT

    %% ========================================
    %% NUMÉRISATION BNU
    %% ========================================
    subgraph BNU_FLOW [🏛️ Numérisation BNU]
        BNU_CONVENTION[📝 Convention BNU<br/>Bibliothèque Nationale<br/>Universitaire Strasbourg]
        BNU_SCAN[🖨️ Numérisation<br/>professionnelle<br/>Haute qualité]
        BNU_CLOUD[☁️ Cloud sécurisé BNU<br/>Stockage temporaire]
        BNU_EXPORT[📤 Export vers<br/>Cloud projet]

        BNU_CONVENTION --> BNU_SCAN
        BNU_SCAN --> BNU_CLOUD
        BNU_CLOUD --> BNU_EXPORT
    end

    %% ========================================
    %% CATÉGORISATION
    %% ========================================
    CATEGORISATION[📋 Catégorisation<br/>des éditions]

    subgraph CATEGORIES [⚖️ Catégories selon Droits d'Auteur]
        CAT_15_20[📜 Domaine public<br/>Auteur décédé +70 ans<br/>Principalement anciennes éditions]
        CAT_JAMAIS[🔒 Éditions jamais<br/>officiellement sorties<br/>Thèses, travaux inédits]
        CAT_20_21[📖 Sous droits<br/>Auteur décédé <70 ans<br/>Éditions récentes]
    end

    %% ========================================
    %% STATUTS DE DROIT
    %% ========================================
    subgraph DROITS [⚖️ Statuts de Droit]
        LIBRE_DROIT[✅ Libre de droit<br/>Domaine public<br/>Diffusion autorisée]
        SECRET[🔒 Secret<br/>Diffusion interdite<br/>Usage interne uniquement]
        RESTREINT[⚠️ Très restreint<br/>Droits d'auteur actifs<br/>Usage limité]
    end

    %% ========================================
    %% CONNEXIONS - SOURCES VERS NUMÉRISATION/CATÉGORISATION
    %% ========================================
    LIBRE -->|Déjà numérique<br/>Export local → Cloud| CATEGORISATION
    INFORMEL -->|Format variable<br/>Export local → Cloud| CATEGORISATION
    PRET --> BNU_CONVENTION
    ACHAT --> BNU_CONVENTION
    BNU_EXPORT --> CATEGORISATION

    %% ========================================
    %% CONNEXIONS - CATÉGORISATION VERS DROITS
    %% ========================================
    CATEGORISATION --> CAT_15_20
    CATEGORISATION --> CAT_JAMAIS
    CATEGORISATION --> CAT_20_21

    CAT_15_20 --> LIBRE_DROIT
    CAT_JAMAIS --> SECRET
    CAT_20_21 --> RESTREINT

    %% ========================================
    %% CONVERGENCE
    %% ========================================
    CONVERGENCE[☁️ Stockage Seafile<br/>Éditions numérisées<br/>avec métadonnées de droit]

    LIBRE_DROIT --> CONVERGENCE
    SECRET --> CONVERGENCE
    RESTREINT --> CONVERGENCE

    OUTPUT([📤 SORTIE MODULE 3<br/>Vers Traitement eScriptorium])

    CONVERGENCE --> OUTPUT

    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 Internet:<br/>Archive.org, Gallica<br/>Bibliothèques numériques<br/>Format PDF/JPG]
    note2[💡 BNU:<br/>Qualité professionnelle<br/>Format TIF 600 DPI<br/>Coût: Variable]
    note3[💡 Catégorisation:<br/>Essentielle pour gérer<br/>les droits de diffusion<br/>Critère: décès auteur +70 ans]
    note4[💡 Libre de droit:<br/>Publication possible<br/>Critère légal: auteur décédé<br/>depuis plus de 70 ans]
    note5[💡 Secret/Restreint:<br/>Usage recherche uniquement<br/>Pas de diffusion publique]

    LIBRE -.-> note1
    BNU_SCAN -.-> note2
    CATEGORISATION -.-> note3
    LIBRE_DROIT -.-> note4
    SECRET -.-> note5

    %% ========================================
    %% STATISTIQUES
    %% ========================================
    subgraph STATS [📊 Répartition Indicative]
        S1[Libre de droit: environ 30%]
        S2[Restreint: environ 68%]
        S3[Secret: environ 2%]
    end

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef decision fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    classDef source fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef bnu fill:#ffccbc,stroke:#d84315,stroke-width:2px
    classDef categorisation fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    classDef categorie fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    classDef libreDroit fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef secret fill:#ef9a9a,stroke:#c62828,stroke-width:2px
    classDef restreint fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef convergence fill:#bbdefb,stroke:#1976d2,stroke-width:3px
    classDef note fill:#fff9c4,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5

    class START,OUTPUT startEnd
    class DECISION decision
    class LIBRE,INFORMEL,PRET,ACHAT source
    class BNU_CONVENTION,BNU_SCAN,BNU_CLOUD,BNU_EXPORT bnu
    class CATEGORISATION categorisation
    class CAT_15_20,CAT_JAMAIS,CAT_20_21 categorie
    class LIBRE_DROIT libreDroit
    class SECRET secret
    class RESTREINT restreint
    class CONVERGENCE convergence
    class note1,note2,note3,note4,note5 note

    style SOURCES fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style BNU_FLOW fill:#ffccbc,stroke:#d84315,stroke-width:2px
    style CATEGORIES fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style DROITS fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style STATS fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 3 3

```

---
*Généré automatiquement depuis `flowchart-module3.mmd`*
