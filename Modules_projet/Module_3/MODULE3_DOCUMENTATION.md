# MODULE 3 - Récupération d'Éditions de Manuscrits

**Documentation de l'acquisition et catégorisation des éditions**

---

## Vue d'ensemble

Le MODULE 3 gère l'acquisition des **éditions de manuscrits** (différent des manuscrits originaux du MODULE 1) et leur catégorisation selon les droits de diffusion.

**Entrée** : Besoins identifiés par les chercheurs
**Sortie** : Éditions numérisées et catégorisées sur Seafile
**Critère principal** : Statut des droits de diffusion

---

## Sources d'acquisition

### 1. Récupération libre de droit sur Internet

**Sources courantes** :
- Archive.org
- Gallica (BnF)
- Google Books
- Bibliothèques numériques universitaires

**Avantages** :
- Gratuit
- Immédiat
- Format numérique (PDF/JPG)

**Processus** :
1. Rechercher l'édition sur les plateformes
2. Télécharger le document
3. Vérifier la qualité
4. Uploader sur Seafile

### 2. Récupération informelle

**Principe** : Contacts personnels avec d'autres chercheurs ou institutions

**Usage** :
- Éditions rares non numérisées
- Partage entre projets de recherche
- Thèses non publiées

### 3. Prêt de bibliothèque

**Processus** :
1. Emprunter l'édition physique
2. Numériser via la BNU (convention)
3. Récupérer les fichiers numérisés

**Convention BNU** : Partenariat avec la Bibliothèque Nationale et Universitaire de Strasbourg permettant l'utilisation des images pour la transcription à but scientifique. Ce type de convention peut s'appliquer à d'autres bibliothèques numériques.

### 4. Achat d'édition

**Usage** : Éditions indisponibles autrement

**Processus** :
1. Acheter l'édition physique
2. Numériser via la BNU
3. Cataloguer et stocker

---

## Numérisation BNU

**Convention** : Partenariat permettant la numérisation professionnelle

**Caractéristiques** :
- Qualité professionnelle
- Format TIF 600 DPI
- Stockage temporaire sur cloud BNU
- Export vers cloud projet (Seafile)

**Workflow** :
```
Édition physique (prêt ou achat)
       ↓
Convention BNU
       ↓
Numérisation professionnelle (haute qualité)
       ↓
Stockage temporaire cloud BNU
       ↓
Export vers Seafile projet
```

---

## Catégorisation des droits

### Critères de classification

| Statut | Critère | Diffusion |
|--------|---------|-----------|
| **Libre de droit** | Auteur mort depuis +70 ans | Publication autorisée |
| **Restreint** | Auteur mort depuis -70 ans | Usage recherche uniquement |
| **Secret** | Éditions jamais publiées officiellement | Usage interne uniquement |

### Libre de droit

**Définition** : L'auteur (ou le dernier co-auteur) est décédé depuis plus de 70 ans.

**Exemples** :
- Éditions du 15e au début 20e siècle (généralement)
- Auteurs médiévaux
- Éditions critiques anciennes

**Diffusion** :
- Publication sur Nakala possible
- Partage académique autorisé
- Citation dans publications

### Restreint

**Définition** : L'auteur est décédé depuis moins de 70 ans, ou droits actifs.

**Exemples** :
- Éditions critiques récentes (20e-21e siècle)
- Traductions contemporaines

**Diffusion** :
- Usage recherche uniquement
- Stockage Seafile (privé)
- Pas de publication publique

### Secret

**Définition** : Éditions jamais officiellement publiées.

**Exemples** :
- Thèses non publiées
- Travaux inédits
- Documents de travail

**Diffusion** :
- Diffusion interdite
- Usage interne uniquement
- Stockage Seafile avec accès restreint

---

## Répartition statistique

D'après le corpus CiSaMe :

| Catégorie | Proportion |
|-----------|------------|
| Libre de droit | ~30% |
| Restreint | ~68% |
| Secret | ~2% |

---

## Workflow de catégorisation

```
Édition acquise
       ↓
Identifier l'auteur/éditeur scientifique
       ↓
Rechercher la date de décès
       ↓
Calculer : Décès + 70 ans < Année actuelle ?
       ↓
   ┌───┴───┐
   OUI     NON
   ↓       ↓
Libre   L'édition a-t-elle été publiée officiellement ?
   ↓           ↓
   ↓      ┌────┴────┐
   ↓      OUI       NON
   ↓      ↓         ↓
   ↓   Restreint  Secret
   ↓      ↓         ↓
   └──────┴─────────┘
          ↓
   Stocker sur Seafile avec métadonnée de droit
          ↓
   Vers MODULE 4 (eScriptorium)
```

---

## Stockage sur Seafile

**Organisation recommandée** :

```
Seafile/
└── CiSaMe/
    └── Editions/
        ├── Libre/
        │   ├── Edition_Friedberg_1879/
        │   └── Edition_Laspeyres_1860/
        ├── Restreint/
        │   ├── Edition_Moderne_2005/
        │   └── These_Durand_1998/
        └── Secret/
            └── Travail_Inedit_2020/
```

**Métadonnées à conserver** :
- Titre de l'édition
- Auteur/Éditeur scientifique
- Date de publication
- Statut de droit
- Source d'acquisition
- Date d'acquisition

---

## Points d'attention

### Vérification des droits

Avant toute diffusion publique :
1. Vérifier la date de décès de l'auteur
2. Vérifier la date de décès de l'éditeur scientifique (si applicable)
3. En cas de doute, classer comme "Restreint"

### Éditions critiques

Les **éditions critiques** ont deux couches de droits :
- Texte original : Généralement libre (auteur médiéval)
- Appareil critique : Protégé par les droits de l'éditeur scientifique

**Recommandation** : Considérer la date de l'édition critique, pas du texte original.

### Convention BNU et autres bibliothèques

La convention BNU permet :
- Utilisation des images pour transcription
- Usage scientifique et recherche
- Pas de diffusion commerciale

Ce type de partenariat peut être établi avec d'autres bibliothèques selon leurs politiques.

---

## Lien avec les autres modules

**En amont** : Besoins exprimés par les chercheurs

**En aval** :
- MODULE 4 : Traitement eScriptorium
- MODULE 8 : Diffusion (selon statut des droits)

**Transversal** : Module Métadonnées (Heurist)
- Les informations sur les éditions alimentent la base Heurist

---

## Fichiers associés

```
Modules_projet/
└── Module_3/
    ├── flowchart-module3.mmd          # Schéma du workflow
    └── MODULE3_DOCUMENTATION.md       # Cette documentation
```

---

## Statut

**MODULE 3** : Opérationnel

- Workflow de catégorisation : Défini
- Convention BNU : Active
- Organisation Seafile : En place

---

*Dernière mise à jour : Décembre 2025*
