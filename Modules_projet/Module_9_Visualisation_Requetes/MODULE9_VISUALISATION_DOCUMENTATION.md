# MODULE 9 - Outil_d'analyse_CiSaMe

## 📋 Vue d'ensemble

Le MODULE 9 est une plateforme d'outils web pour l'analyse du droit canon médiéval, développée par CiSaMe (Circulation des Savoirs médiévaux). Elle se compose de deux modules principaux :

1. **Query Generator** : Générateur de requêtes CQL pour NoSketch Engine
2. **Concordance Analyzer** : Analyse approfondie de concordances avec enrichissement métadonnées

**Repository** : [TitouanCiSaMe/canon-law-toolkit](https://github.com/TitouanCiSaMe/canon-law-toolkit)

---

## 🔍 Module 1 : Query Generator

### Fonctionnalités

Le Query Generator permet de créer des requêtes CQL (Corpus Query Language) complexes pour NoSketch Engine via une interface intuitive.

#### 4 Types de recherche

**1. Proximité**
- Recherche de deux mots à distance configurable
- Distance : 1-20 tokens
- Ordre strict ou flexible
- Exemple : "lex" à 5 mots de "canonicus"

**2. Variations orthographiques médiévales**

Génère automatiquement toutes les variantes orthographiques médiévales :
- **ae/e** : caelum → celum, aecclesia → ecclesia
- **v/u** : servus → seruus, vivere → uiuere
- **j/i** : justitia → iustitia, juris → iuris
- **ti/ci** : gratia → gracia, justitia → justicia

**Jusqu'à 96 variantes possibles** par combinaison de ces règles

**3. Sémantique**
- Recherche conceptuelle avancée
- Relations sémantiques
- Contextes thématiques

**4. Proximité + Variations**
- Combinaison des approches proximité et variations
- Recherche de variations de termes à proximité
- Puissance maximale pour l'analyse lexicale médiévale

### Configuration

Interface de configuration intuitive :
- **Distance entre mots** : Slider 1-20 tokens
- **Types de variations** : Checkboxes pour activer/désactiver chaque type
- **Options de lemmatisation** : Recherche sur lemmes ou formes
- **Validation en temps réel** : Prévisualisation de la requête CQL
- **Messages d'aide contextuels** : Guide l'utilisateur

### Export

**Copier-coller**
- Copie de la requête CQL générée
- Utilisation manuelle dans NoSketch Engine
- Possibilité de modification avant exécution

**Lancer directement**
- Export direct vers NoSketch Engine
- Exécution automatique de la requête
- Récupération des résultats

### Exemples de requêtes CQL générées

**Proximité simple**
```cql
[lemma="ecclesia"] []{0,3} [lemma="potestas"]
```

**Variations ae/e**
```cql
[word="(c|C)(a|ae)lum"]
```

**Variations complètes (ae/e + v/u + j/i + ti/ci)**
```cql
[word="(g|G)ra(t|c)(i|j)(a|ae)"]
```
Génère : gratia, gracia, gratja, gracja, graetia, graecia, graetja, graecja (et variantes majuscules)

**Proximité + Variations**
```cql
[word="(l|L)e(x|ks)"] []{0,5} [word="(c|C)(a|ae)non(i|j)(c|k)(us|vs)"]
```

---

## 📊 Module 2 : Concordance Analyzer

### Gestion des données

#### Préparation des exports depuis NoSketch Engine

Avant d'utiliser le Concordance Analyzer, vous devez préparer vos exports depuis NoSketch Engine. Voici le workflow complet :

**Étape 1 : Recherche sur NoSketch Engine**
- Lancez votre requête CQL sur NoSketch Engine
- Utilisez le Query Generator (MODULE 9) pour créer des requêtes optimisées
- La requête peut provenir du Query Generator ou être créée manuellement

**Étape 2 : Analyse des résultats**
- Examinez les concordances KWIC affichées
- Évaluez la pertinence des résultats
- Identifiez les résultats à conserver pour l'analyse

**Étape 3 : Sélection des résultats**
- **Résultats voulus** : Cochez les concordances pertinentes pour votre analyse
- **Résultats à analyser** : Sélectionnez les occurrences nécessitant un examen approfondi
- Possibilité de sélectionner tous les résultats ou une partie seulement

**Étape 4 : Enrichissement avec métadonnées**
- ☑️ **Cocher ID Édition (Edi-XX)** : Identifiants des collections canoniques médiévales
- ☑️ **Cocher numéros de pages** : Références précises de localisation dans les manuscrits
- Ces métadonnées permettront l'enrichissement automatique dans le Concordance Analyzer

**Étape 5 : Export CSV enrichi**
- **Maximum de contexte KWIC** :
  - Sélectionnez le plus grand nombre de **tokens AVANT** le KWIC (mot-clé en contexte)
  - Sélectionnez le plus grand nombre de **tokens APRÈS** le KWIC
  - Contexte étendu = meilleure analyse sémantique
- **Format d'export** : CSV (format normé NoSketch Engine)
- **Contenu de l'export** :
  - Concordances sélectionnées
  - Contexte gauche étendu
  - KWIC (mot-clé)
  - Contexte droit étendu
  - Métadonnées (ID Édition + n° pages)
- **Export NoSketch normé** : Le fichier CSV généré est prêt pour l'upload dans le Concordance Analyzer

> **💡 Conseil** : Plus le contexte KWIC est étendu, plus l'analyse terminologique et sémantique sera riche. Privilégiez toujours le maximum de tokens disponibles.

#### Upload de fichiers

Une fois vos exports préparés (voir section précédente), vous pouvez les uploader dans le Concordance Analyzer.

**Fichiers requis :**

1. **Métadonnées CSV** (avec identifiants Edi-XX)
   - Identifiants des collections canoniques médiévales
   - Informations bibliographiques complètes
   - Pré-chargement automatique au démarrage

2. **Export NoSketch Engine** (CSV avec concordances)
   - Fichier CSV généré selon le workflow de préparation
   - Format normé NoSketch Engine
   - Doit contenir : ID Édition (Edi-XX) + numéros de pages + contexte KWIC étendu

#### Persistance automatique

- **Sauvegarde automatique** : Les données sont sauvegardées dans sessionStorage
- **Restauration automatique** : Au rechargement de la page, vos données sont restaurées
- **Messages de statut** : Indicateurs persistants du statut de vos données
- **Pré-chargement intelligent** : Métadonnées par défaut chargées automatiquement

### Enrichissement automatique

Le module enrichit automatiquement les concordances avec les métadonnées :

- **Matching références Edi-XX** : Association automatique avec les métadonnées
- **Parsing intelligent** : Détection de structure complexe (pipe-separated multiple works)
- **Fallback robuste** : Conservation des données même sans match parfait
- **Taux de correspondance** : Calcul et affichage du taux d'enrichissement

### 9 Vues d'analyse spécialisées

#### 1. Vue d'ensemble
- **Statistiques globales** : Nombre de concordances, taux d'enrichissement
- **Distribution générale** : Aperçu des données
- **Tableau récapitulatif** : Métriques clés

#### 2. Domaines juridiques
- **Répartition par domaine** : Droit canon, droit civil, procédure, etc.
- **Bar charts** : Visualisation des proportions
- **Statistiques détaillées** : Nombre d'occurrences par domaine

#### 3. Auteurs
- **Analyse par auteur** : Gratien, Raymond de Peñafort, etc.
- **Fréquences d'utilisation** : Classement des auteurs les plus cités
- **Graphiques** : Distribution visuelle

#### 4. Périodes
- **Analyse temporelle** : Distribution chronologique
- **Granularités variables** :
  - Par années
  - Par décennies
  - Par quarts de siècle
  - Par demi-siècles
- **Temporal charts** : Évolution dans le temps

#### 5. Lieux
- **Répartition géographique** : Lieux de production/rédaction
- **Bar charts** : Distribution spatiale
- **Statistiques par lieu**

#### 6. Timeline interactive
- **Timeline Gantt** : Visualisation des plages temporelles des œuvres
- **Navigation interactive** : Zoom, pan
- **Visualisation D3.js** : Haute qualité graphique

#### 7. Analyse terminologique
- **Termes KWIC** : Mots-clés en contexte
- **Fréquences** : Termes les plus fréquents
- **Collocations** : Associations de termes

#### 8. Nuage de mots
- **Word cloud** : Visualisation des termes KWIC les plus fréquents
- **Taille proportionnelle** : À la fréquence d'occurrence
- **Interactif** : Clic pour filtrer

#### 9. Graphiques
- **Bar charts** : Distributions catégorielles
- **Temporal charts** : Évolutions temporelles
- **Timeline Gantt** : Plages chronologiques

### Filtres avancés

**Filtres disponibles :**
- **Recherche textuelle** : Full-text dans les concordances
- **Auteur** : Sélection par auteur spécifique
- **Domaine juridique** : Filtrage par type de droit
- **Période** : Restriction temporelle
- **Lieu** : Filtrage géographique

**Fonctionnalités :**
- **Combinaisons multiples** : Plusieurs filtres simultanés
- **Mise à jour en temps réel** : Visualisations instantanées
- **Persistance** : Filtres conservés pendant la session

### Pagination

Gestion efficace de gros volumes de données :
- Navigation par pages
- Nombre d'éléments configurable
- Performance optimisée

### Comparaison de 2 corpus

#### Upload

Upload de **2 fichiers de concordances** :
- **Corpus A** : Corpus de référence
- **Corpus B** : Corpus à comparer
- **Métadonnées CSV** : Partagées ou distinctes

#### Analyses comparatives

**5 dimensions de comparaison :**

1. **Volumes**
   - Tailles respectives des corpus
   - Nombre de concordances
   - Statistiques comparées

2. **Auteurs**
   - Répartitions comparées
   - Auteurs présents/absents
   - Différences de fréquence

3. **Domaines juridiques**
   - Comparaison des domaines
   - Évolutions thématiques
   - Spécificités de chaque corpus

4. **Temporalité**
   - Évolutions chronologiques
   - Périodes couvertes
   - Différences temporelles

5. **Terminologie**
   - Termes KWIC comparés
   - Vocabulaire distinctif
   - Termes partagés vs spécifiques

#### Visualisations comparatives

- **Charts parallèles** : Visualisations côte à côte
- **Graphiques superposés** : Comparaison directe
- **Tables de différences** : Écarts chiffrés

#### Filtres indépendants

Chaque corpus peut être filtré indépendamment :
- Filtres spécifiques au Corpus A
- Filtres spécifiques au Corpus B
- Comparaison avec filtres appliqués

### Export multi-formats

**3 formats disponibles :**

1. **CSV** (Concordances filtrées)
   - Données brutes
   - Avec enrichissements métadonnées
   - Importable dans Excel, R, Python

2. **JSON** (Analytics complètes)
   - Données structurées
   - Toutes les métriques
   - Réutilisable programmatiquement

3. **PNG** (Graphiques)
   - Haute résolution
   - Pour publications
   - Tous les graphiques exportables

---

## 🛠️ Stack technique

### Frontend

- **React 18.2** : Framework UI moderne
- **Vite 5.0** : Build tool ultra-rapide
- **React Router DOM v6** : Navigation SPA
- **CSS Modules** : Styling modulaire et scopé
- **Inline styles** : Styling dynamique

### Visualisations

- **Recharts** : Bibliothèque de charts React
  - Bar charts
  - Line charts
  - Temporal charts
- **D3.js** : Visualisations avancées
  - Timeline Gantt
  - Graphes personnalisés

### Internationalisation

- **react-i18next** : i18n complète
- **Traductions** : Français / Anglais
- **Toutes les chaînes UI traduites**

### Tests

- **Vitest** : Test runner moderne
- **React Testing Library** : Tests orientés utilisateur
- **93/93 tests** pour Query Generator UI ✅
- **64/91 tests** pour Query Generator Views ✅

### Build & Déploiement

- **Vite** : Optimisations production
- **Lazy loading** : Chargement différé des composants
- **Memoization** : Optimisation des recalculs (useMemo)
- **Debouncing** : Optimisation des filtres temps réel

---

## 📁 Structure du projet

```
canon-law-toolkit/
├── src/
│   ├── modules/
│   │   ├── query-generator/           # MODULE 1
│   │   │   ├── components/
│   │   │   │   ├── ui/               # 4 composants UI (CSS Modules)
│   │   │   │   └── views/            # 4 vues principales
│   │   │   ├── utils/                # Générateurs de requêtes
│   │   │   ├── docs/                 # Documentation complète
│   │   │   └── __tests__/            # Tests unitaires
│   │   │
│   │   └── concordance-analyzer/     # MODULE 2
│   │       ├── components/           # Composants UI
│   │       ├── hooks/                # Logic réutilisable
│   │       ├── utils/                # Parsers & exports
│   │       └── config/               # Configuration
│   │
│   └── shared/
│       ├── i18n/                     # Traductions FR/EN
│       ├── theme/                    # Thème visuel
│       └── components/               # Layout global
│
├── vitest.config.js                  # Configuration tests
├── vite.config.js                    # Configuration build
└── README.md                         # Documentation principale
```

---

## 🎯 Cas d'usage

### Recherche lexicale médiévale

**Objectif** : Étudier les variantes orthographiques de "gratia" dans le Décret de Gratien

1. **Query Generator** : Type "Variations"
2. Entrer : "gratia"
3. Activer : ae/e, j/i, ti/ci
4. **Généré** : `[word="(g|G)ra(t|c)(i|j)(a|ae)"]`
5. Copier dans NoSketch Engine
6. Exporter les résultats
7. **Concordance Analyzer** : Upload + analyse terminologique

### Comparaison diachronique

**Objectif** : Comparer l'usage du vocabulaire entre XIIe et XIIIe siècles

1. **NoSketch Engine** : 2 exports (période XIIe / période XIIIe)
2. **Concordance Analyzer** : Mode comparaison
3. Upload des 2 corpus
4. **Analyse** : Temporalité + Terminologie
5. Identifier les évolutions lexicales
6. Export PNG pour publication

### Analyse d'auteur

**Objectif** : Étudier la réception de Gratien par Raymond de Peñafort

1. **Query Generator** : Proximité + Variations
   - Terme 1 : "Gratianus" (avec variations)
   - Terme 2 : "decretum" (avec variations)
   - Distance : 10 tokens
2. Export résultats NoSketch
3. **Concordance Analyzer** : Upload
4. Filtrer : Auteur = "Raymond de Peñafort"
5. **Analyses** : Vue d'ensemble, Domaines, Timeline
6. Export JSON pour analyse quantitative

---

## 🚀 Déploiement

### Options recommandées

**Vercel** (⭐ Recommandé)
- Déploiement automatique depuis Git
- HTTPS automatique
- CDN global ultra-rapide
- Preview deployments pour chaque PR

**Netlify**
- Interface intuitive
- Drag & drop du dossier `dist/`
- Redirects automatiques pour React Router

**Cloudflare Pages**
- Bandwidth illimité
- CDN Cloudflare
- Builds illimités

### Configuration

Pour Vercel, créer `vercel.json` :
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

Pour Netlify, créer `public/_redirects` :
```
/*    /index.html   200
```

---

## 🔗 Liens avec autres modules CiSaMe

- **MODULE 7 (NoSketch-Engine)** : Source des données pour Concordance Analyzer
- **MODULE 6 (PAGEtopage)** : Produit le format corpus_vertical.txt utilisé par NoSketch
- **Module Métadonnées (Heurist)** : Source des métadonnées Edi-XX

---

## 📚 Documentation complète

**Repository** : [github.com/TitouanCiSaMe/canon-law-toolkit](https://github.com/TitouanCiSaMe/canon-law-toolkit)

**Documentation modules :**
- [Query Generator README](https://github.com/TitouanCiSaMe/canon-law-toolkit/blob/main/src/modules/query-generator/README.md)
- [Components Documentation](https://github.com/TitouanCiSaMe/canon-law-toolkit/blob/main/src/modules/query-generator/docs/COMPONENTS.md)
- [User Guide](https://github.com/TitouanCiSaMe/canon-law-toolkit/blob/main/src/modules/query-generator/docs/USER_GUIDE.md)
- [QUICKSTART.md](https://github.com/TitouanCiSaMe/canon-law-toolkit/blob/main/QUICKSTART.md)
- [ARCHITECTURE.md](https://github.com/TitouanCiSaMe/canon-law-toolkit/blob/main/ARCHITECTURE.md)

---

## 📧 Contact

**Projet** : CiSaMe - Circulation des Savoirs médiévaux
**Université** : Strasbourg
**Développeur** : Titouan
**GitHub** : [github.com/TitouanCiSaMe](https://github.com/TitouanCiSaMe)

---

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| Version | 1.4.0 |
| Status | Production-ready ✅ |
| Modules | 2 (Query Generator + Concordance Analyzer) |
| Types de requêtes CQL | 4 |
| Vues d'analyse | 9 |
| Formats export | 3 (CSV, JSON, PNG) |
| Langues | 2 (FR/EN) |
| Tests | 157/184 ✅ (85%) |

---

## 📚 Fichiers et ressources

**Schémas** :
- `flowchart-module9-visualisation.mmd` : Schéma du module de visualisation et générateur de requêtes

**Repository** :
- GitHub : https://github.com/TitouanCiSaMe/canon-law-toolkit

**Documentation** :
- README principal du toolkit
- Documentation Query Generator
- Documentation Concordance Analyzer

---

*Pour revenir à la documentation des modules, voir [`../README.md`](../README.md)*
