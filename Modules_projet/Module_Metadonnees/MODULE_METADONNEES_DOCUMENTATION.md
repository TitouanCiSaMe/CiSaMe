# 🗂️ MODULE - Fiches de Métadonnées : Structuration Heurist

**Documentation du module de gestion des métadonnées dans Heurist**

---

## 📋 Vue d'ensemble

Ce module gère l'**extraction, la structuration et le stockage** des métadonnées bibliographiques dans la base de données Heurist.

**Objectif** : Créer une base structurée de métadonnées utilisable par l'ensemble du pipeline
**Source** : Fiches de métadonnées fournies par les chercheurs
**Destination** : Base de données Heurist
**Usage** : Alimentation des autres modules (PAGEtopage, exports finaux)

---

## 📝 Contenu des fiches de métadonnées

### Informations généralement présentes

Les fiches de métadonnées contiennent typiquement :

**Sur l'œuvre** :
- Titre de l'œuvre
- Auteur(s) avec variantes de noms
- Date ou période de rédaction
- Lieu ou aire géographique de rédaction

**Sur l'édition** :
- Titre de l'édition
- Éditeur scientifique
- Maison d'édition et/ou Collection
- Lieu d'édition
- Date d'édition
- Pagination
- Remarque(s) éventuelle(s)
- Indications bibliographiques

**Métadonnées de gestion** :
- Responsable de la fiche (chercheur)
- Date de création
- Type de document (Droit canonique, Théologie, Droit romain)

---

## 🔄 Workflow d'extraction

```
Fiches de métadonnées (format variable)
    ↓
Extraction des informations
    ↓
Structuration en 3 tables parallèles :
    ├─→ Table AUTEURS
    ├─→ Table OEUVRES
    └─→ Table ÉDITIONS
    ↓
Insertion dans Heurist avec relations (clés étrangères)
    ↓
Base de données Heurist complète
```

---

## 🗄️ Structure des 3 tables

### **Table AUTEURS**

Stocke les informations sur les auteurs des œuvres.

**Métadonnées** :
- `Identifiant de l'auteur` : ID unique (ex: "Auteur-1")
- `Nom` : Nom principal (ex: "Bernardus Papiensis")
- `Alias` : Variantes de noms séparées par `|`
  - Exemple : "Bernard de Pavie|Bernardo Balbi|Bernard of Pavia|Bernhard von Pavia"

**Type Heurist** : Person (Type 10)

**Gestion des variantes** :
Les multiples orthographes d'un même auteur sont stockées dans le champ "Alternate name(s)" avec séparation par `|`. Cela permet :
- Recherche par n'importe quelle variante
- Pas de doublons
- Traçabilité des formes anciennes/modernes

**Exemple d'enregistrement** :
```
ID: 5265 (Auteur-1)
Nom: Bernardus Papiensis
Variantes: Bernard de Pavie|Bernardo Balbi|Bernardus Balbi Ticinensis|
          Bernardus Balbus|Bernard of Pavia|Bernhard von Pavia|
          Bernardo da Pavia
```

---

### **Table OEUVRES (Sources)**

Stocke les informations sur les œuvres sources.

**Métadonnées** :
- `Identifiant de l'oeuvre` : ID unique (ex: "Oeuv-1")
- `Titre` : Titre de l'œuvre
- `Identifiant de l'auteur` : Clé étrangère → Table Auteurs
- `Date ou période de rédaction` : Format JSON temporel
- `Lieu ou aire géographique de rédaction` : Ex: "Italie", "France"
- `Auteur de la notice` : Chercheur responsable (ex: "Yann")
- `Type` : "Droit canonique", "Théologie", "Droit romain"

**Type Heurist** : Oeuvre (Type 107)

**Format des dates** :
```json
{
  "start": {"earliest": "1191"},
  "end": {"latest": "1198"},
  "estMinDate": 1191,
  "estMaxDate": 1198.1231
}
```

Cela permet de gérer :
- Dates précises : 1164
- Plages : 1191-1198
- Dates approximatives : ~1165
- Incertitude

**Exemple d'enregistrement** :
```
ID: 5283 (Oeuv-1)
Titre: Summa titulorum decretalium
Auteur: 5265 (Auteur-1 : Bernardus Papiensis)
Date: 1191-1198
Lieu: Italie
Type: Droit canonique
Responsable: Yann
```

---

### **Table ÉDITIONS**

Stocke les informations sur les éditions imprimées des œuvres.

**Métadonnées** :
- `Identifiant de l'édition` : ID unique (ex: "Edi-1")
- `Titre` : Titre complet de l'édition
- `Éditeur` : Éditeur scientifique
- `Maison d'édition et/ou Collection`
- `Lieu d'édition` : Ville de publication
- `Date d'édition` : Année de publication
- `Pagination` : Pages (ex: "1-366")
- `Remarque(s) éventuelle(s)` : Notes diverses
- `Auteur de la notice` : Chercheur responsable
- `Identifiant de l'oeuvre` : Clé étrangère → Table Oeuvres
- `Type` : Hérité de l'œuvre

**Type Heurist** : Edition (Type 105)

**Exemple d'enregistrement** :
```
ID: 5312 (Edi-1)
Titre: Bernardus Papiensis Faventini episcopi Summa decretalium
Éditeur: E Laspeyres
Collection: /
Pages: 1-366
Date: 1860
Lieu: Regensburg
Remarque: réimpr. Graz, 1956
Oeuvre: 5283 (Oeuv-1)
```

---

## 🔗 Relations entre tables

### Structure relationnelle

```
AUTEUR (Type 10)
    ↑
    | (1:n - Un auteur peut avoir plusieurs œuvres)
    |
OEUVRE (Type 107)
    ↑
    | (1:n - Une œuvre peut avoir plusieurs éditions)
    |
ÉDITION (Type 105)
```

**Relations via clés étrangères** :
- Édition → Oeuvre : Champ "Has edited" (Pointer)
- Oeuvre → Auteur : Champ "Author" (Pointer)

**Cardinalités** :
- 1 Auteur → n Oeuvres
- 1 Oeuvre → n Éditions
- 1 Oeuvre → 1+ Auteur (cas des co-auteurs)

**Gestion des co-auteurs** :
Pour une œuvre avec plusieurs auteurs, deux approches possibles :
1. Plusieurs relations Pointer vers différents auteurs
2. Champ texte avec séparation par `|` (ex: "Yann|Raphaël Eckert")

---

## 💾 Base de données Heurist

### Qu'est-ce que Heurist ?

**Heurist** est un système de gestion de base de données flexible pour la recherche en sciences humaines.

**Caractéristiques** :
- Architecture record-based (enregistrements)
- Schéma flexible (ajout de champs sans migration SQL)
- Interface web intégrée
- Gestion des utilisateurs native
- Vocabulaires contrôlés (Terms)
- Export facile (CSV, XML, JSON)

**Instance du projet** :
- Nom : `hdb_cisame_misha`
- Hébergement : Serveur Heurist
- Utilisateurs : 7 actifs (Yann, Raphaël Eckert, Guillaume Porte, etc.)
- Enregistrements : 5 768
- Éditions documentées : 129

---

## 📊 Statistiques du corpus

### Répartition par type

D'après les 129 éditions documentées :

**Par type d'œuvre** :
- Droit canonique : ~38 éditions
- Théologie : ~61 éditions
- Droit romain : ~17 éditions
- Autres : ~13 éditions

**Période couverte** :
- Du Moyen Âge (XIIe siècle) aux éditions modernes (XXIe siècle)
- Ex: 1125-2018

**Responsables principaux** :
- Yann (principal)
- Raphaël Eckert
- Christophe Grellard
- Autres contributeurs

---

## 🔧 Utilisation des métadonnées

### Par MODULE 6 (PAGEtopage)

Les métadonnées Heurist sont **consultées manuellement** puis renseignées dans `config.yaml` de PAGEtopage.

**Processus** :
1. Chercheur identifie l'édition à traiter
2. Consulte Heurist pour récupérer les métadonnées
3. Copie les informations pertinentes dans config.yaml

**Exemple de métadonnées copiées** :
```yaml
metadata:
  edition_id: "Edi-7"
  title: "Magistri Honorii Summa ''De iure canonico tractaturus''"
  language: "Latin"
  author: "Honorius"
  source: "Summa ''De iure canonico tractaturus''"
  type: "Droit canonique"
  date: "1188"
  lieu: "France"
  ville: "Paris"
```

**Métadonnées utilisées** :
- `edition_id` : Identifiant Heurist (ex: "Edi-7")
- `title` : Titre complet de l'édition
- `language` : Latin / Français
- `author` : Nom de l'auteur
- `source` : Titre de l'œuvre source
- `type` : Type de droit
- `date` : Date de rédaction de l'œuvre
- `lieu` : Lieu de rédaction
- `ville` : Ville précise

### Par Module Données Textuelles

Les métadonnées Heurist enrichissent les packages Nakala pour publication.

**Métadonnées exportées** :
- Titre du corpus
- Auteur(s)
- Date
- Type
- Institution
- Description

### Par exports académiques

Les métadonnées peuvent être exportées pour :
- BibTeX (pour LaTeX)
- Zotero/EndNote
- TEI XML (édition numérique)
- Bibliographies formatées

---

## 🎯 Exemple complet

### Fiche de métadonnées initiale

```
Titre : Summa titulorum decretalium
Auteur(s) : Bernardus Papiensis (Bernard de Pavie ; Bernardo Balbi ;
            Bernardus Balbi Ticinensis ; Bernardus Balbus ;
            Bernard of Pavia ; Bernhard von Pavia ; Bernardo da Pavia)
Date ou période de rédaction : 1191-1198
Lieu ou aire géographique de rédaction : Italie
Type : Droit canonique

Édition :
  Titre : Bernardus Papiensis Faventini episcopi Summa decretalium
  Éditeur : E Laspeyres
  Maison d'édition/Collection : /
  Lieu d'édition : Regensburg
  Date d'édition : 1860
  Pagination : 1-366
  Remarque(s) : réimpr. Graz, 1956
  Indications bibliographiques : S. Kuttner, Repertorium, p. 322-323

Responsable de la fiche : Yann
```

### Après extraction et insertion dans Heurist

**Table Auteurs** :
```
ID: 5265 (Auteur-1)
Nom: Bernardus Papiensis
Variantes: Bernard de Pavie|Bernardo Balbi|Bernardus Balbi Ticinensis|
          Bernardus Balbus|Bernard of Pavia|Bernhard von Pavia|
          Bernardo da Pavia
```

**Table Oeuvres** :
```
ID: 5283 (Oeuv-1)
Titre: Summa titulorum decretalium
Auteur: → 5265 (Auteur-1)
Date: {JSON: 1191-1198}
Lieu: Italie
Type: Droit canonique
Responsable: Yann
```

**Table Éditions** :
```
ID: 5312 (Edi-1)
Titre: Bernardus Papiensis Faventini episcopi Summa decretalium
Éditeur: E Laspeyres
Collection: /
Pages: 1-366
Date: 1860
Lieu: Regensburg
Remarque: réimpr. Graz, 1956
Oeuvre: → 5283 (Oeuv-1)
```

**Relations établies** :
- Edi-1 édite → Oeuv-1
- Oeuv-1 écrite par → Auteur-1

---

## 🔗 Lien avec le schéma initial

Ce module correspond exactement à l'analyse faite dans `ANALYSE_SCHEMAS_DOCUMENTATION.md` :

**Entités créées dans Heurist** :
- ✅ Auteur (Person, Type 10)
- ✅ Oeuvre/Source (Type 107)
- ✅ Edition (Type 105)
- ✅ Date_de_prod (Type 104)
- ✅ Commentaire (Type 103)
- ✅ Allegation (Type 109)

**Entités manquantes identifiées** :
- ❌ Chapitre (bloque Source → Chapitre → Allegation)
- ⚠️ Manuscrit/Document (Type 89 à clarifier)
- ❌ Lien (ou champs sur Manuscrit)

---

## 📝 Workflows de saisie

### Créer une nouvelle édition complète

**Ordre recommandé** :
1. Vérifier si l'auteur existe déjà
   - Si non : Créer l'auteur avec variantes
2. Créer la Date de production (si applicable)
3. Créer l'Oeuvre
   - Lier à l'auteur
   - Lier à la date
4. Créer l'Edition
   - Lier à l'oeuvre
5. Vérifier les relations

**Champs obligatoires** :
- Auteur : Nom
- Oeuvre : Titre, Type
- Edition : Titre, Date d'édition

---

## 🛠️ Outils et exports

### Export CSV depuis Heurist

Heurist permet d'exporter les données en CSV pour :
- Analyse programmatique
- Import dans autres outils
- Backup
- Partage

**Exemple d'export** :
```bash
# Export éditions
export-cisame-misha-t105-edition.csv

# Colonnes :
# ID, Identifiant interne, Titre, Éditeur, Maison d'édition,
# Pages, Date, Lieu, Remarques, Oeuvre (ID + Titre)
```

### Scripts d'import/export

**Scripts potentiels** (à développer si besoin) :
- `parse_fiche_to_heurist.py` : Parsing fiches → Heurist
- `export_heurist_to_bibtex.py` : Export BibTeX
- `export_heurist_to_zotero.py` : Export Zotero
- `export_heurist_to_tei.py` : Export TEI XML

---

## ✅ Points forts

1. **Structure relationnelle claire** : 3 tables bien définies
2. **Gestion des variantes de noms** : Alias séparés par `|`
3. **Identifiants internes humainement lisibles** : Edi-1, Oeuv-1, Auteur-1
4. **Dates flexibles** : Format JSON pour plages et incertitudes
5. **Métadonnées riches** : Lieux, types, responsables
6. **Traçabilité** : Qui a créé quelle fiche
7. **Réutilisation** : Métadonnées utilisées par MODULE 6 et exports

---

## ⚠️ Points d'attention

### Saisie manuelle actuelle

Les métadonnées sont actuellement saisies manuellement dans Heurist.

**Risques** :
- Erreurs de frappe
- Incohérences
- Doublons possibles

**Recommandations** :
- Vérifier systématiquement avant création
- Utiliser vocabulaires contrôlés Heurist
- Valider les relations

### Copie manuelle vers PAGEtopage

Les métadonnées sont copiées manuellement de Heurist vers config.yaml de PAGEtopage.

**Risques** :
- Erreur de copie
- Désynchronisation si mise à jour Heurist

**Amélioration future possible** :
- Export automatique Heurist → config.yaml
- Via API Heurist ou CSV intermédiaire

---

## 📚 Documentation complémentaire

**Fichiers du projet** :
- `ANALYSE_SCHEMAS_DOCUMENTATION.md` : Analyse complète de la base Heurist

**Schémas** :
- `flowchart-metadonnees.mmd` : Schéma d'extraction vers Heurist

**Exports CSV** :
- `Liste MSS juridiques.docx` (liste initiale)
- `liste_manuscrits.csv` (conversion)
- Exports Heurist (à générer)

---

## ✅ État actuel

**MODULE Fiches Métadonnées** : ✅ **Opérationnel**

- Structure Heurist : ✅ (3 tables créées)
- 129 éditions documentées : ✅
- Relations fonctionnelles : ✅
- Métadonnées riches : ✅
- Utilisation par MODULE 6 : ✅

**Base stable et utilisable** pour l'ensemble du pipeline.

---

## 🚀 Améliorations futures possibles

1. **Automatisation saisie** : Parsing fiches → Heurist
2. **Export automatique** : Heurist → config.yaml PAGEtopage
3. **Validation automatique** : Détection doublons
4. **Enrichissement** : Ajout identifiants externes (VIAF, Wikidata)
5. **Interface simplifiée** : Formulaire de saisie guidé
