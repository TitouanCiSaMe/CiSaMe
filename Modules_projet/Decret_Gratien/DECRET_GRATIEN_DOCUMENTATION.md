# MODULE SPÉCIAL - Décret de Gratien

**Documentation du pipeline spécifique au Décret de Gratien**

---

## Vue d'ensemble

Le Décret de Gratien est un corpus canonique majeur qui dispose de son **propre pipeline de traitement**, distinct du workflow général CiSaMe.

**Important** : Ce corpus **NE PASSE PAS** par le MODULE 6 (PAGEtopage). Il possède son propre format .txt et est déjà opérationnel sur NoSketch-Engine.

---

## Caractéristiques du corpus

### Statistiques

| Métrique | Valeur |
|----------|--------|
| Nombre de fichiers | 4 149 fichiers .txt |
| Taille totale | ~5 Mo |
| Canons | ~4 000 canons |
| Distinctions | ~150 distinctions |
| Causae | ~36 causae |
| Quaestiones | ~150 quaestiones |

### Format des identifiants

**Pattern** : `Grat_XXXX`

Exemples :
- `Grat_0001`
- `Grat_1234`
- `Grat_4149`

---

## Structure du Décret

Le Décret de Gratien est organisé en **trois parties** :

### Première partie (Distinctiones)

- 101 distinctions (D.1 à D.101)
- Traite des sources du droit canon
- Structure : `Premiere_partie/D.X/`

### Deuxième partie (Causae)

- 36 causae (C.1 à C.36)
- Chaque causa contient des quaestiones
- Structure : `Deuxieme_partie/C.X/q.X/`

**Cas spécial** : Causa 33, Quaestio 3 contient le **Tractatus de Penitencia** avec 7 distinctions internes (D.1 à D.7).

### Troisième partie (De Consecratione)

- 5 distinctions (D.1 à D.5)
- Traite des sacrements
- Structure : `Troisieme_partie/D.X/`

---

## Arborescence des fichiers

```
Decret_Gratien/
├── Premiere_partie/
│   ├── D.1/
│   ├── D.2/
│   ├── ...
│   ├── D.100/
│   └── D.101/
│
├── Deuxieme_partie/
│   ├── C.1/
│   │   ├── q.1/
│   │   ├── q.2/
│   │   └── ...
│   ├── C.2/
│   │   └── ...
│   ├── ...
│   ├── C.33/
│   │   ├── q.1/
│   │   ├── q.2/
│   │   ├── QUESTIO_III_TRACTATUS_DE_PENITENCIA/
│   │   │   ├── D.1/
│   │   │   ├── D.2/
│   │   │   ├── D.3/
│   │   │   ├── D.4/
│   │   │   ├── D.5/
│   │   │   ├── D.6/
│   │   │   └── D.7/
│   │   ├── q.4/
│   │   └── q.5/
│   └── C.36/
│       ├── q.1/
│       └── q.2/
│
└── Troisieme_partie/
    ├── D.1/
    ├── D.2/
    ├── D.3/
    ├── D.4/
    └── D.5/
```

### Cas particuliers de numérotation

Certaines quaestiones sont fusionnées dans la structure :
- `q.2_3` : Quaestiones 2 et 3 fusionnées
- `q.3_4` : Quaestiones 3 et 4 fusionnées
- `q.5_6` : Quaestiones 5 et 6 fusionnées
- `q.1_2` : Quaestiones 1 et 2 fusionnées

---

## Sources du corpus

### 1. Allégations (Ochoa et Diez)

**Source** : Recueil d'allégations historique d'Ochoa et Diez

**Contenu** :
- Catalogue des sources du Décret
- ~3 800 allégations recensées
- Référencement des citations canoniques

**Traitement** :
1. Extraction algorithmique
2. Génération CSV brut (numéro allégation + suffixe)
3. Ajout d'ID unique
4. Ajout manuel des allégations non détectées automatiquement
5. Correction et enrichissement
6. Validation → `Allegations.csv` final

### 2. Édition Friedberg

**Source** : Édition critique standard (1879-1881), Corpus Iuris Canonici

**Contenu** :
- Texte intégral du Décret de Gratien
- Appareil critique
- XML PAGE + Images

### 3. Münchener Digitale Bibliothek

**Source** : Version numérisée accessible en ligne

**Usage** : Complément et vérification

---

## Workflow de traitement

```
Sources parallèles
    │
    ├── Ochoa et Diez ──────┐
    │   (Allégations)       │
    │         ↓             │
    │   Extraction algo     │
    │         ↓             │
    │   CSV brut            │
    │         ↓             │
    │   Ajout ID + manuel   │
    │         ↓             │
    │   Validation          │
    │         ↓             │
    │   Allegations.csv ────┼──→ Mapping ID
    │                       │         ↓
    ├── Friedberg ──────────┼──→ Fusion sources
    │   (XML PAGE)          │         ↓
    │                       │   Extraction canons (.txt)
    └── Münchener ──────────┘         ↓
        (Web)                   Répartition dossiers
                                      ↓
                                Structure hiérarchique
                                      ↓
                                Ajout ID (via Allegations.csv)
                                      ↓
                                Enrichissement métadonnées
                                      ↓
                                Validation
                                      ↓
                                Corpus final
                                      ↓
                                NoSketch-Engine
```

---

## Statut actuel

**Corpus Décret de Gratien** : **Opérationnel**

- Corpus complet : 4 149 fichiers
- Structure hiérarchique : Complète
- NoSketch-Engine : Déjà en service
- Interrogeable en ligne

---

## Différences avec le pipeline général

| Aspect | Pipeline général | Décret de Gratien |
|--------|------------------|-------------------|
| MODULE 6 (PAGEtopage) | Oui | **Non** |
| Format de sortie | corpus_vertical.txt | .txt structuré |
| Lemmatisation | TreeTagger | Traitement spécifique |
| Structure | Par édition | Par partie/causa/quaestio |
| NoSketch | Via MODULE 7 | Déjà intégré |

---

## Interrogation du corpus

Le corpus est interrogeable sur NoSketch-Engine avec les fonctionnalités :
- Recherche par forme
- Recherche par lemme
- Concordances KWIC
- Collocations
- Statistiques de fréquence

---

## Lien avec les autres modules

**En amont** :
- MODULE 4 : Source des XML PAGE (Friedberg)
- MODULE 5 : Nettoyage (si applicable)

**En parallèle** :
- MODULE 7 : Corpus déjà sur NoSketch-Engine
- Module Métadonnées : Référencement dans Heurist

**Pas de passage par** :
- MODULE 6 (PAGEtopage)

---

## Fichiers associés

```
Modules_projet/
└── Decret_Gratien/
    ├── flowchart-decret-gratien.mmd      # Schéma du workflow
    └── DECRET_GRATIEN_DOCUMENTATION.md   # Cette documentation
```

---

## Références académiques

- **Friedberg, Emil** : *Corpus Iuris Canonici*, Leipzig, 1879-1881
- **Ochoa, X. et Diez, A.** : *Indices Canonum, Titulorum et Capitulorum Corporis Iuris Canonici*, Rome, 1964
- **Münchener Digitale Bibliothek** : https://www.digitale-sammlungen.de/

---

*Dernière mise à jour : Décembre 2025*
