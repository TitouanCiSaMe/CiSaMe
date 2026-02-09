# 📦 MODULE 8 - Diffusion des Données : Export Nakala

**Documentation du module de préparation et diffusion des corpus sur Nakala**

---

## 📋 Vue d'ensemble

Ce module gère la **diffusion finale** des données textuelles enrichies vers :
- **Nakala** : Plateforme ouverte pour les corpus libres de droits (DOI, archivage pérenne)
- **Seafile** : Stockage privé pour les corpus à droits restreints

**Entrées** : Sorties de PAGEtopage (MODULE 6) + Fiches de métadonnées
**Sorties** : Corpus publiés sur Nakala avec DOI / Corpus archivés sur Seafile

---

## 🔄 Workflow complet

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ENTRÉES (depuis MODULE 6)                     │
├─────────────────────────────────────────────────────────────────────┤
│  • Fiches .docx (métadonnées + Edi-XX + Libre de droits)            │
│  • Fichiers verticaux .txt (corpus annotés)                          │
│  • Dossiers textes/ (pages + pages_index.json)                       │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│     ÉTAPE 1 : VALIDATION                                            │
│     Script : validate_export.py                                      │
│     → Vérifie cohérence fiche ↔ vertical ↔ textes                   │
│     → Génère rapport de validation                                   │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│     ÉTAPE 2 : PRÉPARATION STRUCTURE                                 │
│     Script : prepare_nakala_export.py                                │
│     → Associe les données par Edi-XX                                 │
│     → Sépare Libre_de_droits / Non_libre_de_droits                  │
│     → Convertit fiches .docx → .pdf                                  │
└─────────────────────────────────────────────────────────────────────┘
          │
          ├──────────────────────────────────────┐
          ▼                                      ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│   LIBRE DE DROITS        │      │   NON LIBRE DE DROITS    │
├──────────────────────────┤      ├──────────────────────────┤
│     ÉTAPE 3A : UPLOAD    │      │     ÉTAPE 3B : ARCHIVE   │
│     Script : upload_     │      │     → Copie manuelle     │
│     nakala.py (Heimdall) │      │       vers Seafile       │
│     → Upload API Nakala  │      │     → Accès restreint    │
│     → Attribution DOI    │      │                          │
│     → Génère cisame.xml  │      │                          │
└──────────────────────────┘      └──────────────────────────┘
          │                                      │
          ▼                                      │
┌──────────────────────────┐                     │
│     ÉTAPE 4 : ENRICHIR   │                     │
│     Script : add_nakala_ │                     │
│     links.py             │                     │
│     → Ajoute URLs Nakala │                     │
│       dans verticaux     │                     │
└──────────────────────────┘                     │
          │                                      │
          ▼                                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SORTIES                                      │
├─────────────────────────────────────────────────────────────────────┤
│  • Nakala : Corpus publics avec DOI (→ MODULE 7 NoSketch-Engine)    │
│  • Seafile : Corpus privés pour usage recherche interne             │
│  • Verticaux enrichis : Attributs link="" et fiche="" pour MODULE 7 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Scripts disponibles

### Scripts principaux

| Script | Rôle | Entrée | Sortie |
|--------|------|--------|--------|
| `validate_export.py` | Valide la cohérence des données | Fiches + Verticaux + Textes | Rapport de validation |
| `prepare_nakala_export.py` | Crée la structure d'export | Fiches + Verticaux + Textes | Structure Libre/Non_libre |
| `upload_nakala.py` | Upload via Heimdall (script externe, repo nakala-uploader) | Structure préparée | DOI + cisame.xml |
| `add_nakala_links.py` | Enrichit les verticaux | cisame.xml | Verticaux avec URLs |

### Module partagé

| Module | Rôle |
|--------|------|
| `nakala_utils.py` | Fonctions communes (normalisation, extraction, tri Edi-XX, matching) |

### Scripts utilitaires

| Script | Rôle | Quand l'utiliser |
|--------|------|------------------|
| `convert_fiches_to_pdf.py` | Convertit .docx → .pdf | Si conversion séparée nécessaire |
| `clean_dates.py` | Nettoie dates vides | Si API refuse les dates "" |
| `flatten_textes.py` | Supprime fichiers vides + aplatit sous-dossiers (avec `--flatten`) | Si fichiers vides ou structure incorrecte |
| `collect_verticals.sh` | Collecte les vertical.txt | Pour rassembler les verticaux dispersés |
| `match_fiches_editions.py` | Matching fiches ↔ CSV | Si fiches sans Edi-XX (rare) |

---

## 📖 Guide pas à pas

### Étape 1 : Validation

```bash
cd Nakala/
python validate_export.py \
    --fiches ../Fiches_Editions_Metadonnee/ \
    --verticaux ../Verticaux/ \
    --textes ../Textes/
```

**Vérifie :**
- Présence des 3 sources pour chaque Edi-XX
- Validité des pages_index.json
- Champs obligatoires (source, author, type)

### Étape 2 : Préparation

```bash
python prepare_nakala_export.py \
    --fiches ../Fiches_Editions_Metadonnee/ \
    --verticaux ../Verticaux/ \
    --textes ../Textes/ \
    --output ./input/CiSaMe/
```

**Crée :**
```
input/CiSaMe/
├── Libre_de_droits/
│   └── Oeuvre_Edi-XX/
│       ├── pages_index.json
│       ├── vertical.txt
│       ├── fiche.pdf
│       └── page_*.txt
└── Non_libre_de_droits/
    └── ...
```

### Étape 3A : Upload Nakala (libres de droits)

```bash
# Configurer API_KEY et GROUP_KEY dans upload_nakala.py
python upload_nakala.py
```

**Génère :** `output/cisame.xml` avec DOI et métadonnées

### Étape 3B : Archive Seafile (droits restreints)

```bash
# Copie manuelle vers Seafile
cp -r input/CiSaMe/Non_libre_de_droits/* /chemin/vers/Seafile/
```

### Étape 4 : Enrichissement URLs

```bash
python add_nakala_links.py output/cisame.xml
```

**Ajoute dans les verticaux :**
```xml
<doc link="https://nakala.fr/DOI#hash" fiche="https://nakala.fr/DOI#hash2" ...>
```

---

## 🌐 Nakala : Plateforme de diffusion

### Qu'est-ce que Nakala ?

**Nakala** est l'entrepôt de données de recherche de Huma-Num (CNRS/EHESS).

**Caractéristiques :**
- Archivage pérenne des données de recherche
- Attribution de DOI pour citation
- Accès ouvert (Open Access)
- Respect des principes FAIR

### Métadonnées exportées

| Champ source | Métadonnée Nakala |
|--------------|-------------------|
| `source` (pages_index.json) | `dc:title` |
| `author` | `nakala:creator` |
| `type` | `dc:references` |
| `date` | `nakala:created` + `dc:date` |
| - | `dc:type` = "text" |
| - | `dc:license` = "etalab-2.0" |
| - | `dc:publisher` = "Université de Strasbourg" |

---

## 💾 Seafile : Stockage privé

### Organisation recommandée

```
Seafile/CiSaMe/
└── Corpus_Restreints/
    ├── Droit_canonique/
    │   └── Oeuvre_Edi-XX/
    └── Droit_romain/
        └── Oeuvre_Edi-YY/
```

### Accès

- Équipe CiSaMe uniquement
- Authentification universitaire
- Partage contrôlé (liens temporaires)

---

## ⚖️ Gestion des droits

### Critères de classification

| Type | Critère | Destination |
|------|---------|-------------|
| **Libre** | Manuscrits médiévaux (domaine public) | Nakala |
| **Libre** | Éditions avant 1900 | Nakala |
| **Libre** | Auteur décédé > 70 ans | Nakala |
| **Restreint** | Droits d'auteur actifs | Seafile |
| **Secret** | Éditions non publiées | Seafile |

### Détection automatique

Le script `prepare_nakala_export.py` détecte le statut via :
```
Libre de droits : Oui
```
dans les fiches .docx

---

## 📊 Statistiques indicatives

| Catégorie | Pourcentage |
|-----------|-------------|
| Libre de droits → Nakala | ~30% |
| Droits restreints → Seafile | ~68% |
| Secret → Seafile | ~2% |

---

## ⚠️ Dépendances

```bash
pip install python-docx requests tqdm heimdall defusedxml
```

- **python-docx** : Lecture fiches .docx
- **requests** : API Nakala
- **tqdm** : Barres de progression
- **heimdall** : Upload Nakala
- **defusedxml** : Parsing XML sécurisé (recommandé pour add_nakala_links.py)
- **LibreOffice** : Conversion PDF (`soffice`)

---

## 📁 Emplacement des scripts

Tous les scripts sont dans le dossier `/Nakala/` à la racine du projet :

```
CiSaMe/
├── Nakala/
│   ├── README.md                    ← Documentation complète
│   ├── nakala_utils.py              ← Module partagé (fonctions communes)
│   ├── validate_export.py           ← Validation
│   ├── prepare_nakala_export.py     ← Préparation
│   ├── add_nakala_links.py          ← Enrichissement URLs
│   ├── convert_fiches_to_pdf.py     ← Conversion PDF
│   ├── clean_dates.py               ← Nettoyage dates
│   ├── flatten_textes.py            ← Fichiers vides + aplatissement
│   ├── collect_verticals.sh         ← Collecte des verticaux
│   ├── match_fiches_editions.py     ← Matching fiches (obsolète)
│   ├── export_nakala_par_edition.py ← Ancien export (remplacé)
│   ├── export_nakala_par_oeuvre.py  ← Ancien export (remplacé)
│   └── tests/                       ← Tests unitaires + fixtures
└── Modules_projet/
    └── Module_8_Diffusion_Donnees/  ← Cette documentation
```

> **Note** : Le script `upload_nakala.py` (Étape 3) fait partie du dépôt externe `nakala-uploader`.

---

## ✅ État actuel

**MODULE 8 - Diffusion** : ✅ **Opérationnel**

- Scripts de validation : ✅
- Scripts de préparation : ✅
- Upload Heimdall/Nakala : ✅
- Enrichissement URLs : ✅
- Documentation : ✅

---

## 🔗 Liens avec les autres modules

| Module | Lien |
|--------|------|
| **MODULE 6 (PAGEtopage)** | Fournit les verticaux + textes + pages_index.json |
| **MODULE 7 (NoSketch-Engine)** | Reçoit les verticaux enrichis avec URLs Nakala |
| **Module Métadonnées (Heurist)** | Source des métadonnées bibliographiques |

---

## 📚 Ressources

- **Documentation complète** : `/Nakala/README.md`
- **Nakala** : https://www.nakala.fr/
- **API Nakala** : https://api.nakala.fr/doc
- **Heimdall** : https://gitlab.huma-num.fr/huma-num/heimdall

---

*Dernière mise à jour : Février 2026*
