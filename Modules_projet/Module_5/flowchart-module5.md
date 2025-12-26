# Module5

> **Note**: Ce diagramme est également disponible en format image PNG dans le même dossier.

```mermaid
flowchart TD
    %% ========================================
    %% MODULE 5 - NETTOYAGE POST-ESCRIPTORIUM
    %% ========================================

    START([🧹 MODULE 5<br/>Nettoyage Post-eScriptorium])

    %% ========================================
    %% IMPORT ET STOCKAGE
    %% ========================================
    IMPORT[📥 Import XML Pages<br/>depuis eScriptorium]
    STOCKAGE[☁️ Stockage sur Seafile<br/>Format: NOMÉDITION_ID.xml]
    EXPORT[📤 Export pour<br/>traitement local]

    START --> IMPORT
    IMPORT --> STOCKAGE
    STOCKAGE --> EXPORT

    %% ========================================
    %% DÉCISION LAYOUT
    %% ========================================
    DECISION{Quel type<br/>de layout ?}

    EXPORT --> DECISION

    %% ========================================
    %% BRANCHE SIMPLE PAGE - 1 région Main
    %% ========================================
    subgraph SIMPLE_FLOW [Simple Page - 1 région Main]
        SIMPLE_TITLE[Une seule région Main<br/>par page]
        SIMPLE_OXYGEN[🔧 Ouvrir avec Oxygène<br/>Onglet rechercher]
        SIMPLE_XPATH["🎯 XPath: 1 région<br/>//TextRegion[contains(@custom, 'type:MainZone')]<br/>//TextLine//Unicode/text"]
        SIMPLE_REGEX[⚙️ Application Regex<br/>Corrections automatiques]
        SIMPLE_RESULT[✅ Page nettoyée]

        SIMPLE_TITLE --> SIMPLE_OXYGEN
        SIMPLE_OXYGEN --> SIMPLE_XPATH
        SIMPLE_XPATH --> SIMPLE_REGEX
        SIMPLE_REGEX --> SIMPLE_RESULT
    end

    %% ========================================
    %% BRANCHE DEUX PAGES - 2 régions Main
    %% ========================================
    subgraph DEUX_FLOW [Deux Pages - 2 régions Main]
        DEUX_TITLE[Deux régions Main<br/>par page<br/>Recto-Verso ou colonnes]
        DEUX_OXYGEN[🔧 Ouvrir avec Oxygène<br/>Onglet rechercher]
        DEUX_XPATH1["🎯 XPath colonne 1<br/>//TextRegion[contains(@custom, 'type:MainZone:column#1')]<br/>//TextLine//Unicode/text"]
        DEUX_REGEX1[⚙️ Application Regex<br/>sur colonne 1]
        DEUX_XPATH2["🎯 XPath colonne 2<br/>//TextRegion[contains(@custom, 'type:MainZone:column#2')]<br/>//TextLine//Unicode/text"]
        DEUX_REGEX2[⚙️ Application Regex<br/>sur colonne 2]
        DEUX_RESULT[✅ Page nettoyée]

        DEUX_TITLE --> DEUX_OXYGEN
        DEUX_OXYGEN --> DEUX_XPATH1
        DEUX_XPATH1 --> DEUX_REGEX1
        DEUX_REGEX1 --> DEUX_XPATH2
        DEUX_XPATH2 --> DEUX_REGEX2
        DEUX_REGEX2 --> DEUX_RESULT
    end

    %% ========================================
    %% BRANCHE QUATRE PAGES - 4 régions Main
    %% ========================================
    subgraph QUATRE_FLOW [Quatre Pages - 4 régions Main]
        QUATRE_TITLE[Quatre régions Main<br/>par page<br/>Layout complexe]
        QUATRE_OXYGEN[🔧 Ouvrir avec Oxygène<br/>Onglet rechercher]
        QUATRE_XPATH_ALL[🎯 XPath 4 colonnes<br/>column#1, #2, #3, #4<br/>Application séquentielle]
        QUATRE_REGEX_ALL[⚙️ Application Regex<br/>sur chaque colonne]
        QUATRE_RESULT[✅ Page nettoyée]

        QUATRE_TITLE --> QUATRE_OXYGEN
        QUATRE_OXYGEN --> QUATRE_XPATH_ALL
        QUATRE_XPATH_ALL --> QUATRE_REGEX_ALL
        QUATRE_REGEX_ALL --> QUATRE_RESULT
    end

    %% ========================================
    %% CONNEXIONS PRINCIPALES
    %% ========================================
    DECISION -->|1 région| SIMPLE_TITLE
    DECISION -->|2 régions| DEUX_TITLE
    DECISION -->|4 régions| QUATRE_TITLE

    %% ========================================
    %% VÉRIFICATION ET FINALISATION
    %% ========================================
    VERIFICATION[✅ Vérification<br/>Contrôle pagination<br/>Détection erreurs OCR<br/>Cohérence globale]
    CORRECTIONS{Erreurs<br/>détectées ?}
    CORRECTION_MANUELLE[✍️ Corrections<br/>manuelles<br/>Pages sans lignes détectées<br/>Bugs de segmentation]
    VERSION_FINALE[✨ Version finale<br/>des transcriptions<br/>au format XML Page]

    SIMPLE_RESULT --> VERIFICATION
    DEUX_RESULT --> VERIFICATION
    QUATRE_RESULT --> VERIFICATION

    VERIFICATION --> CORRECTIONS
    CORRECTIONS -->|Oui| CORRECTION_MANUELLE
    CORRECTIONS -->|Non| VERSION_FINALE
    CORRECTION_MANUELLE --> VERIFICATION

    OUTPUT([📤 SORTIE MODULE 5<br/>Transcriptions finalisées])

    VERSION_FINALE --> OUTPUT

    %% ========================================
    %% DÉTAIL DES REGEX UTILISÉES
    %% ========================================
    subgraph REGEX_DETAIL [🔧 Regex Utilisées]
        REGEX_TITLE[📋 Expressions Régulières]

        subgraph REGEX_COMMUNES [Regex Communes - Espaces et Ponctuation]
            R1[Normalisation espaces<br/>Doubles espaces → Simple]
            R2[Correction ponctuation<br/>Espaces avant/après]
        end

        subgraph REGEX_SPECIFIQUES [Regex Spécifiques au Texte]
            R3["Caractères spéciaux:<br/>[!?''`–—…\[\]{}«»/\\&*@#§¶†‡°^~¨]<br/>Suppression sélective"]
            R4["Chiffres: \\d+<br/>Détection numérotation"]
            R5["Folios: T f[°'] [A-Z\\d{1,2}][a-z]{2}<br/>Références manuscrit"]
            R6["Folios alt: T f[°'] [A-Z0-9][a-z]{2}<br/>Variante références"]
            R7["Suppressions: \\|[^\\]]*\\]<br/>Contenu entre | et ]"]
        end
    end

    %% ========================================
    %% PROCÉDURE OXYGÈNE DÉTAILLÉE
    %% ========================================
    subgraph OXYGEN_PROC [📚 Procédure Oxygène - TRÈS IMPORTANT]
        OXY_STEP1[1. Ouvrir avec Oxygène]
        OXY_STEP2[2. Onglet rechercher]
        OXY_STEP3[3. Regex dans texte à rechercher]
        OXY_STEP4[4. ✓ Cocher Expression régulière]
        OXY_STEP5[5. ✓ Cocher chemin indiqué]
        OXY_STEP6[6. Limiter à XPath selon layout]
        OXY_STEP7[7. Chercher/Remplacer séquentiellement]
    end

    %% ========================================
    %% ANNOTATIONS
    %% ========================================
    note1[💡 Oxygène:<br/>Outil XML professionnel<br/>Recherche XPath puissante<br/>Regex avancées]
    note2[💡 XPath:<br/>Cible précisément<br/>les zones MainZone<br/>Évite zones marginales]
    note3[💡 Regex:<br/>Personnalisées selon texte<br/>Ajout/suppression flexible<br/>selon le manuscrit]
    note4[💡 Vérification:<br/>Pages sans lignes MainZone<br/>Souvent fin de chapitre<br/>Pages non régulières]

    SIMPLE_OXYGEN -.-> note1
    SIMPLE_XPATH -.-> note2
    SIMPLE_REGEX -.-> note3
    VERIFICATION -.-> note4

    %% ========================================
    %% STATISTIQUES
    %% ========================================
    subgraph STATS [📊 Statistiques Indicatives]
        S1[Temps nettoyage: ~20 min par œuvre]
        S2[Pages problématiques: Fins de chapitres]
        S3[Cause bugs: Mauvaise segmentation MainZone]
    end

    %% ========================================
    %% OUTILS
    %% ========================================
    subgraph TOOLS [🛠️ Outils Utilisés]
        T1[Oxygène XML Editor]
        T2[Expressions régulières Regex]
    end

    %% ========================================
    %% STYLES
    %% ========================================
    classDef startEnd fill:#4caf50,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef decision fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    classDef import fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef stockage fill:#bbdefb,stroke:#1976d2,stroke-width:2px
    classDef simple fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef deux fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef quatre fill:#ffccbc,stroke:#d84315,stroke-width:2px
    classDef regex fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    classDef verification fill:#b2dfdb,stroke:#00796b,stroke-width:2px
    classDef finale fill:#a5d6a7,stroke:#2e7d32,stroke-width:3px
    classDef note fill:#fff9c4,stroke:#f57f17,stroke-width:1px,stroke-dasharray: 5 5
    classDef title fill:#e0e0e0,stroke:#757575,stroke-width:2px
    classDef oxygen fill:#e1f5fe,stroke:#01579b,stroke-width:2px

    class START,OUTPUT startEnd
    class DECISION,CORRECTIONS decision
    class IMPORT,EXPORT import
    class STOCKAGE stockage
    class SIMPLE_TITLE,SIMPLE_OXYGEN,SIMPLE_XPATH,SIMPLE_REGEX,SIMPLE_RESULT simple
    class DEUX_TITLE,DEUX_OXYGEN,DEUX_XPATH1,DEUX_REGEX1,DEUX_XPATH2,DEUX_REGEX2,DEUX_RESULT deux
    class QUATRE_TITLE,QUATRE_OXYGEN,QUATRE_XPATH_ALL,QUATRE_REGEX_ALL,QUATRE_RESULT quatre
    class R1,R2,R3,R4,R5,R6,R7 regex
    class VERIFICATION,CORRECTION_MANUELLE verification
    class VERSION_FINALE finale
    class note1,note2,note3,note4 note
    class REGEX_TITLE title
    class OXY_STEP1,OXY_STEP2,OXY_STEP3,OXY_STEP4,OXY_STEP5,OXY_STEP6,OXY_STEP7 oxygen

    style SIMPLE_FLOW fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style DEUX_FLOW fill:#fff8e1,stroke:#f57f17,stroke-width:2px
    style QUATRE_FLOW fill:#fbe9e7,stroke:#d84315,stroke-width:2px
    style REGEX_DETAIL fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,stroke-dasharray: 5 5
    style REGEX_COMMUNES fill:#e1bee7,stroke:#8e24aa,stroke-width:1px
    style REGEX_SPECIFIQUES fill:#e1bee7,stroke:#8e24aa,stroke-width:1px
    style STATS fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 3 3
    style TOOLS fill:#e0f2f1,stroke:#00796b,stroke-width:2px,stroke-dasharray: 3 3
    style OXYGEN_PROC fill:#e1f5fe,stroke:#01579b,stroke-width:3px

```

---
*Généré automatiquement depuis `flowchart-module5.mmd`*
