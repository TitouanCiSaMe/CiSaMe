# MODULE 9 - Visualisation et Générateur de Requêtes

## 📋 Vue d'ensemble

Le MODULE 9 est un outil complet d'analyse et de visualisation pour le corpus NoSketch-Engine. Il combine deux fonctionnalités principales :
1. **Générateur de requêtes CQL** : Création assistée de requêtes complexes
2. **Visualisation et analyse** : Exploration visuelle des résultats avec comparaison possible

## 🎯 Objectifs

- Faciliter la création de requêtes CQL complexes
- Visualiser les résultats de manière interactive
- Comparer deux exports pour analyses contrastives
- Exporter les analyses dans plusieurs formats

---

## 1️⃣ Générateur de Requêtes CQL

### 1.1 Types de requêtes disponibles

#### 📍 1.1.1 Proximité
**Recherche de mots à proximité l'un de l'autre**

- Distance configurable entre les termes
- Ordre strict ou flexible
- Exemple : "lex" à 5 mots de "canonicus"

**Cas d'usage :**
- Étudier les collocations juridiques
- Analyser les expressions figées
- Identifier les contextes d'usage

#### 🔄 1.1.2 Variations
**Recherche de formes alternatives d'un même concept**

- Variations orthographiques
- Formes fléchies (déclinaisons, conjugaisons)
- Lemmes et leurs dérivés

**Cas d'usage :**
- Compte des occurrences totales d'un concept
- Analyse diachronique des graphies
- Étude morphologique

#### 📍🔄 1.1.3 Proximité + Variations
**Combinaison des deux approches**

- Recherche de variations de termes à proximité
- Exemple : variations de "lex" près de variations de "canon"

**Cas d'usage :**
- Analyses sémantiques fines
- Étude des champs lexicaux
- Identification de familles de termes

#### 🧠 1.1.4 Contexte Sémantique
**Recherche basée sur le sens et les relations sémantiques**

- Co-occurrences sémantiques
- Contextes thématiques
- Relations conceptuelles

**Cas d'usage :**
- Analyse thématique
- Cartographie conceptuelle
- Études de réseaux sémantiques

### 1.2 Génération CQL (1.1.1.1)

Le module génère automatiquement la requête en **Corpus Query Language** (CQL), le langage standard de NoSketch-Engine.

**Exemple de requête générée :**
```cql
[lemma="lex"] []{0,5} [lemma="canonicus"]
```

### 1.3 Options d'export

#### 📋 1.1.1.1.1 Copier-coller
- Copie de la requête CQL générée
- Utilisation manuelle dans NoSketch-Engine
- Possibilité de modification avant exécution

#### 🚀 1.1.1.1.2 Export direct vers NoSketch-Engine
- Connexion API avec NoSketch-Engine
- Exécution automatique de la requête
- Récupération directe des résultats
- Gain de temps et réduction d'erreurs

---

## 2️⃣ Visualisation - 1 Export NoSketch

### 2.1 Import (1.2.1)

Import d'un export NoSketch-Engine au **format normé** :
- Format CSV standardisé
- Colonnes requises : Mot, Fréquence, Contexte gauche, Contexte droit, Métadonnées
- Encodage UTF-8

### 2.2 Filtres configurables (1.2.1.1)

Application de filtres personnalisés :
- **Fréquence** : Seuil minimum/maximum d'occurrences
- **POS (Part-of-Speech)** : Sélection par catégorie grammaticale
- **Lemme** : Filtrage par lemme spécifique
- **Période** : Restriction temporelle (si métadonnées temporelles)
- **Source** : Filtrage par manuscrit ou édition

### 2.3 Six Panels de visualisation (1.2.1.1.1)

#### 📊 Panel 1 : Distribution des fréquences
- Histogramme des fréquences
- Analyse de Zipf
- Termes les plus/moins fréquents

#### 📊 Panel 2 : Concordances KWIC
- Affichage "KeyWord In Context"
- Contexte gauche et droit
- Navigation interactive
- Export contextes

#### 📊 Panel 3 : Collocations
- Termes co-occurrents
- Score de significativité (MI, T-score, Log-likelihood)
- Réseau de collocations
- Force des associations

#### 📊 Panel 4 : Timeline temporel
- Évolution temporelle des occurrences
- Courbes de fréquence
- Périodisation
- Identification de pics

#### 📊 Panel 5 : Répartition par source
- Distribution par manuscrit/édition
- Heatmap de présence
- Sources principales/secondaires
- Statistiques par source

#### 📊 Panel 6 : Réseau sémantique
- Graphe des relations
- Proximité sémantique
- Clusters thématiques
- Visualisation force-directed

### 2.4 Export des panels (1.2.1.1.1.1)

Chaque panel exportable en :
- **CSV** : Données brutes pour analyse statistique
- **JSON** : Données structurées pour réutilisation
- **PNG** : Image haute résolution pour publication

---

## 3️⃣ Visualisation - Comparaison 2 Exports

### 3.1 Import double (1.2.2)

Import de deux exports NoSketch-Engine normés pour analyse comparative :
- Export A : Corpus de référence
- Export B : Corpus à comparer

**Cas d'usage :**
- Comparer deux périodes
- Comparer deux auteurs
- Comparer deux genres textuels
- Évolution diachronique

### 3.2 Filtres indépendants (1.2.2.1)

Filtres applicables séparément à chaque export :
- Même filtres que pour 1 export
- Configuration indépendante
- Harmonisation possible

### 3.3 Panels pour Export 1 (1.2.2.1.1)

Les 6 panels standards appliqués au premier export :
- Distribution fréquences Export 1
- Concordances Export 1
- Collocations Export 1
- Timeline Export 1
- Répartition par source Export 1
- Réseau sémantique Export 1

### 3.4 Panel de Comparaison (1.2.2.1.2)

**Panel spécial d'analyse différentielle** :

#### 🔀 Analyses comparatives

**Écarts de fréquences**
- Différences absolues et relatives
- Termes surreprésentés / sous-représentés
- Significativité statistique (Chi², Log-likelihood)

**Collocations distinctives**
- Collocations spécifiques à chaque corpus
- Collocations partagées
- Différences d'intensité

**Évolution temporelle**
- Courbes comparatives
- Identification de divergences
- Périodes de rupture

**Statistiques comparatives**
- Taille des corpus
- Richesse lexicale
- Diversité
- Tableau de synthèse

**Visualisations**
- Graphiques superposés
- Heatmaps différentielles
- Nuages de mots comparatifs
- Scatter plots

### 3.5 Export complet

Export de **tous les panels** (6 + 1 de comparaison) :
- CSV : Toutes les données
- JSON : Structure complète
- PNG : Toutes les visualisations

---

## 🛠️ Technologies utilisées

### Backend
- **Python 3.10+** : Traitement des données
- **Pandas** : Manipulation et analyse
- **NumPy** : Calculs statistiques
- **SciPy** : Tests statistiques

### Visualisation
- **Matplotlib** : Graphiques statiques
- **Plotly** : Visualisations interactives
- **NetworkX** : Graphes de réseaux
- **Seaborn** : Visualisations statistiques

### Connexion NoSketch-Engine
- **Requests** : API HTTP
- **Beautiful Soup** : Parsing HTML
- Format CQL natif

### Export
- **Pandas** : Export CSV
- **JSON** : Export structuré
- **PIL/Pillow** : Export PNG haute résolution

---

## 📊 Format des données

### Export normé NoSketch-Engine (CSV)

```csv
Word,Lemma,POS,Frequency,Left_Context,Right_Context,Source,Date
lex,lex,NOUN,142,"in causa",". Sed etiam","Decretum_Gratiani",1140
canonicus,canonicus,ADJ,89,"iure",".",Liber_Extra,1234
```

**Colonnes requises :**
- `Word` : Forme du mot
- `Lemma` : Lemme
- `POS` : Part-of-Speech (catégorie grammaticale)
- `Frequency` : Fréquence d'occurrence
- `Left_Context` : Contexte gauche (3-5 mots)
- `Right_Context` : Contexte droit (3-5 mots)
- `Source` : Manuscrit ou édition source
- `Date` : Date ou période (optionnel)

---

## 🎯 Cas d'usage

### Recherche thématique
1. Générer requête "Proximité + Variations" pour "peccatum" et "poena"
2. Export direct vers NoSketch-Engine
3. Import résultat dans visualisation
4. Panel 3 (Collocations) : Identifier les termes associés
5. Panel 6 (Réseau) : Cartographier le champ sémantique

### Analyse diachronique
1. Créer 2 exports NoSketch : Corpus XIIe siècle vs Corpus XIIIe siècle
2. Import double dans visualisation
3. Panel Comparaison : Identifier évolutions lexicales
4. Panel 4 comparatif : Courbes d'évolution
5. Export PNG pour publication

### Étude d'auteur
1. Export NoSketch pour Gratien
2. Visualisation 1 export
3. Panel 2 (KWIC) : Analyse contextes
4. Panel 5 : Répartition dans les sources
5. Export CSV pour analyse quantitative

---

## 📈 Workflow typique

```
┌─────────────────────────────────────────┐
│ 1. Génération requête CQL               │
│    Type : Proximité + Variations        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. Export direct vers NoSketch-Engine   │
│    Exécution automatique                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 3. Import résultat normé                │
│    Format CSV standardisé                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 4. Application filtres                  │
│    Fréquence > 10, POS = NOUN           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 5. Exploration 6 panels                 │
│    Analyse visuelle interactive          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 6. Export CSV + JSON + PNG              │
│    Pour publication et archivage         │
└─────────────────────────────────────────┘
```

---

## 🔍 Exemples de requêtes CQL

### Proximité simple
```cql
[lemma="ecclesia"] []{0,3} [lemma="potestas"]
```
Recherche "ecclesia" à maximum 3 mots de "potestas"

### Variations orthographiques
```cql
[word="ecclesia|aecclesia|eclesia"]
```
Recherche toutes les variantes orthographiques

### Contexte sémantique
```cql
[lemma="lex|canon|decretum"] []{0,5} [lemma="interpretatio|glossa|expositio"]
```
Recherche termes juridiques près de termes d'interprétation

### Requête complexe
```cql
[lemma="papa|pontifex"] [pos="VERB"] []{0,2} [lemma="decretum"]
```
Recherche Pape + Verbe + Décret

---

## 📁 Structure des fichiers

```
Module_9_Visualisation_Requetes/
├── flowchart-module9-visualisation.mmd
├── MODULE9_VISUALISATION_DOCUMENTATION.md
└── (futur) src/
    ├── query_generator.py
    ├── nosketch_connector.py
    ├── visualization.py
    ├── comparison.py
    └── export_utils.py
```

---

## 🔗 Liens avec autres modules

- **MODULE 7 (NoSketch-Engine)** : Source des données
- **MODULE 6 (PAGEtopage)** : Format corpus_vertical.txt utilisé par NoSketch
- **MODULE 8 (Diffusion)** : Métadonnées Nakala intégrables

---

## 📧 Contact

**Projet** : CiSaMe - Université de Strasbourg
**Module** : 9 - Visualisation et Générateur de Requêtes
**Repository** : TitouanCiSaMe/canon-law-toolkit

---

*Pour revenir à la documentation des modules, voir [`../README.md`](../README.md)*
