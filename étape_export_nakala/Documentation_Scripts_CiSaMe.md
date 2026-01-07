# Scripts d'automatisation CiSaMe - Documentation complète

## Contexte du projet

Dans le cadre du projet **CiSaMe** (Circulation des Savoirs Médiévaux au XIIe siècle), nous disposons de plusieurs types de fichiers issus de la numérisation et de l'analyse de manuscrits médiévaux :

- **Fiches d'œuvres** (`.docx`) : Fiches bibliographiques décrivant chaque œuvre (titre, auteur, édition, éditeur, date, etc.)
- **Fichiers verticaux** (`.txt`) : Textes annotés avec informations morphosyntaxiques (format utilisé pour les corpus linguistiques)
- **Dossiers de textes** : Pages extraites des manuscrits + fichier de fusion

L'objectif est de préparer ces données pour un dépôt sur **Nakala** (entrepôt de données de recherche), en organisant les fichiers par œuvre et en distinguant les éditions libres de droits des autres.

---

## Problématique initiale

### Problème 1 : Les fiches n'ont pas d'identifiant

Les fiches d'œuvres ne contiennent pas l'identifiant de l'édition (`Edi-XX`) utilisé dans la base de données CiSaMe. Il faut donc :
1. Faire correspondre chaque fiche avec la bonne entrée dans le CSV de la base
2. Ajouter l'identifiant à la fiche
3. Indiquer si l'édition est libre de droits

### Problème 2 : Les fichiers sont dispersés

Les fichiers sont dans des dossiers séparés et il faut les regrouper intelligemment pour l'export :
- Associer chaque fiche avec son fichier vertical et son dossier de textes
- Séparer les libres de droits des non libres de droits
- Gérer les cas incomplets (fiche sans vertical, vertical sans fiche, etc.)

### Problème 3 : Une édition peut contenir plusieurs œuvres

Certaines éditions physiques regroupent plusieurs œuvres distinctes. Il faut donc choisir :
- Regrouper par édition (1 dossier = 1 ID) ?
- Ou séparer par œuvre (1 dossier = 1 fichier vertical) ?

---

## Solutions développées

### Script 1 : `match_fiches_editions.py`

**Objectif :** Enrichir automatiquement les fiches avec l'identifiant d'édition et le statut libre de droits.

**Approche :**

Le script utilise un algorithme de **matching flou** (fuzzy matching) pour trouver la correspondance entre une fiche et une entrée du CSV. Trois stratégies sont essayées par ordre de priorité :

1. **Correspondance par titre d'édition** : Si le titre de l'édition dans la fiche ressemble à plus de 80% à un titre du CSV
2. **Correspondance par titre d'œuvre + auteur** : Si le titre de l'œuvre matche (>80%) et que l'auteur matche aussi (>60%)
3. **Correspondance floue générale** : Meilleure correspondance au-dessus d'un seuil de 70%

Le texte est normalisé avant comparaison (minuscules, sans accents, sans ponctuation).

**Détection libre de droits :**

On fournit au script un fichier `.docx` listant les œuvres libres de droits. Le script extrait :
- Les identifiants explicites (`Edi-XX`)
- Les titres des œuvres marquées "/ ?" (sans identifiant connu)

Une œuvre est marquée libre de droits si son ID ou son titre correspond.

**Résultat :** Chaque fiche est enrichie avec :
```
Identifiant édition : Edi-39
Libre de droits : Oui
```

---

### Script 2 : `export_nakala.py` (version par édition)

**Objectif :** Regrouper les fichiers par ID d'édition pour créer l'arborescence d'export.

**Logique :**
- Scanner les 3 sources (fiches, verticaux, textes)
- Extraire l'ID de chaque fichier
- Indexer par ID → tous les fichiers avec le même `Edi-XX` vont dans le même dossier

**Règle de création :**
- Un dossier est créé **seulement si** on a un fichier vertical **ET** un dossier de textes
- Les fiches seules ne génèrent pas de dossier (mais sont loggées)

**Structure produite :**
```
Export_Nakala/
├── Libre_de_droits/
│   └── Nom_oeuvre_Edi-XX/
│       ├── fiche.docx
│       ├── vertical_1.txt
│       ├── vertical_2.txt    ← Si plusieurs œuvres
│       ├── textes_1/
│       └── textes_2/
└── Non_libre_de_droits/
    └── ...
```

**Résultat avec les données CiSaMe :** 87 dossiers (car plusieurs œuvres partagent le même ID)

---

### Script 3 : `export_nakala.py` (version par œuvre)

**Objectif :** Créer un dossier distinct pour chaque œuvre, même si elles partagent le même ID d'édition.

**Pourquoi cette variante ?**

Pour Nakala, il peut être préférable d'avoir un dépôt par œuvre plutôt que par édition. Cela permet :
- Une granularité plus fine
- Des métadonnées spécifiques à chaque œuvre
- Une meilleure traçabilité

**Logique :**
- Chaque fichier vertical = une œuvre distincte
- Les dossiers textes sont matchés **par nom** (ils sont nommés comme les verticaux dont ils sont issus)
- Les fiches sont matchées **par ID** et dupliquées dans chaque dossier d'œuvre concerné

**Structure produite :**
```
Export_Nakala/
├── Libre_de_droits/
│   ├── Oeuvre_A_Edi-41/
│   │   ├── fiche.docx      ← Même fiche, dupliquée
│   │   ├── vertical.txt
│   │   └── textes/
│   └── Oeuvre_B_Edi-41/
│       ├── fiche.docx      ← Même fiche, dupliquée
│       ├── vertical.txt
│       └── textes/
└── Non_libre_de_droits/
    └── ...
```

**Résultat avec les données CiSaMe :** 122 dossiers (1 par fichier vertical)

---

## Tableau récapitulatif

| Script | Entrée | Sortie | Indexation |
|--------|--------|--------|------------|
| `match_fiches_editions.py` | Fiches .docx + CSV | Fiches enrichies | Par matching flou |
| `export_nakala.py` (v1) | Fiches + Verticaux + Textes | 87 dossiers | Par ID d'édition |
| `export_nakala.py` (v2) | Fiches + Verticaux + Textes | 122 dossiers | Par fichier vertical |

---

## Workflow complet

```bash
# Étape 1 : Enrichir les fiches avec les identifiants
python match_fiches_editions.py \
    --csv export-cisame.csv \
    --libres Ouvrages_libres_de_droits.docx \
    --dossier ./Fiches_Originales/ \
    --output ./Fiches_Enrichies/

# Étape 2 : Créer l'export Nakala (choisir une version)
python export_nakala.py \
    --fiches ./Fiches_Enrichies/ \
    --verticaux ./Fichiers_verticaux/ \
    --textes ./Dossiers_textes/ \
    --output ./Export_Nakala

# Étape 3 : Nettoyer les fichiers inutiles
find ./Export_Nakala -type f \( -name "corpus_stats.json" -o -name "images_mapping.txt" \) -delete
```

---

## Fichiers de log

Les scripts génèrent des logs détaillés permettant de :
- Vérifier le nombre de correspondances trouvées
- Identifier les fiches/verticaux/textes sans match
- Lister les exports incomplets (sans fiche, etc.)
- Diagnostiquer les problèmes (fichiers sans ID détecté, etc.)

---

## Dépendances

```bash
pip install python-docx
```

---

## Auteur

Scripts développés pour le projet CiSaMe - Décembre 2024
