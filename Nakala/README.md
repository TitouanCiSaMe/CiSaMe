# 📦 Nakala - Scripts d'export pour le projet CiSaMe

**Suite d'outils pour préparer et uploader les corpus sur Nakala (MODULE 8)**

---

## 📋 Vue d'ensemble

Ce dossier contient tous les scripts nécessaires pour :
1. **Valider** les données avant export
2. **Préparer** la structure pour Heimdall
3. **Uploader** sur Nakala via l'API
4. **Enrichir** les corpus avec les URLs Nakala

---

## 🔄 Workflow complet

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ENTRÉES                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Fiches_Editions_Metadonnee/     ← Fiches .docx avec Edi-XX         │
│  Verticaux/                       ← Fichiers .txt                   │
│  Textes/                          ← Dossiers avec pages_index.json  │
│       └── (générés par PAGEtopage MODULE 6)                         │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 : VALIDATION (optionnel mais recommandé)                   │
│  $ python validate_export.py --fiches ... --verticaux ... --textes  │
│  → Génère rapport de cohérence                                      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 : PRÉPARATION STRUCTURE                                    │
│  $ python prepare_nakala_export.py --fiches ... --verticaux ...     │
│  → Crée input/CiSaMe/Libre_de_droits/ et Non_libre_de_droits/       │
│  → Convertit fiches .docx → .pdf                                    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 : UPLOAD NAKALA (via Heimdall)                             │
│  $ python upload_nakala.py   (sur chaque dossier séparément)        │
│  → Upload sur Nakala API                                            │
│  → Génère cisame.xml                                                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 4 : ENRICHISSEMENT URLs                                      │
│  $ python add_nakala_links.py cisame.xml                            │
│  → Ajoute link="" et fiche="" dans les <doc> des verticaux          │
│  → Option -o : fusionne les verticaux modifiés en un fichier unique │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SORTIES                                     │
├─────────────────────────────────────────────────────────────────────┤
│  Nakala : Corpus publics avec DOI                                   │
│  Seafile : Corpus privés (droits restreints)                        │
│  NoSketch-Engine : Verticaux enrichis avec URLs (MODULE 7)          │
│  Corpus fusionné : Fichier unique pour NoSketch-Engine (si -o)      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Scripts disponibles

### Scripts principaux (workflow standard)

| Script | Description | Usage |
|--------|-------------|-------|
| **validate_export.py** | Valide la cohérence des données | `python validate_export.py -f fiches/ -v verticaux/ -t textes/` |
| **prepare_nakala_export.py** | Prépare la structure pour Heimdall | `python prepare_nakala_export.py -f fiches/ -v verticaux/ -t textes/ -o output/` |
| **upload_nakala.py** | Upload sur Nakala via Heimdall | ⚠️ Script externe (repo nakala-uploader) |
| **add_nakala_links.py** | Enrichit les verticaux avec URLs + fusion optionnelle | `NAKALA_API_KEY=... python add_nakala_links.py cisame.xml [-o corpus.txt]` |

### Scripts utilitaires (usage ponctuel)

| Script | Description | Usage |
|--------|-------------|-------|
| **convert_fiches_to_pdf.py** | Convertit .docx → .pdf | `python convert_fiches_to_pdf.py chemin/ [--delete-docx] [--dry-run]` |
| **clean_dates.py** | Nettoie dates vides dans JSON | `python clean_dates.py chemin/ [--dry-run] [--recursive]` |
| **flatten_textes.py** | Supprime fichiers vides + aplatit sous-dossiers textes/ | `python flatten_textes.py chemin/ [--flatten] [--dry-run]` |
| **collect_verticals.sh** | Collecte les vertical.txt depuis les sous-dossiers | `./collect_verticals.sh [source] [destination]` |
| **match_fiches_editions.py** | Matching flou fiches ↔ CSV | ⚠️ Obsolète si fiches ont déjà Edi-XX |
| **export_nakala_par_edition.py** | Export groupé par ID | ⚠️ Remplacé par prepare_nakala_export.py |
| **export_nakala_par_oeuvre.py** | Export séparé par œuvre | ⚠️ Remplacé par prepare_nakala_export.py |

---

## 📖 Guide d'utilisation détaillé

### ÉTAPE 1 : Validation (validate_export.py)

**Objectif** : Vérifier la cohérence des données avant export

```bash
python validate_export.py \
    --fiches ./Fiches_Editions_Metadonnee/ \
    --verticaux ./Verticaux/ \
    --textes ./Textes/ \
    --output rapport_validation.txt
```

**Ce que le script vérifie :**
- ✅ Chaque Edi-XX a bien une fiche, un vertical et des textes
- ✅ Les pages_index.json existent et sont valides
- ✅ Les champs obligatoires sont présents (source, author, type)
- ✅ Cohérence des métadonnées entre les sources

**Sortie :**
```
STATISTIQUES GLOBALES
────────────────────────────────
Total Edi-XX trouvés: 153
  - Complets (fiche + vertical + textes): 89
  - Exportables (vertical + textes): 122
  - Non exportables: 31

ITEMS COMPLETS (prêts pour export)
════════════════════════════════════════
  ✓ Edi-1 [LIBRE]
  ✓ Edi-3 [NON LIBRE]
  ...

NON EXPORTABLES (données manquantes)
════════════════════════════════════════
  ✗ Edi-45 - Manque: vertical, textes
  ...
```

---

### ÉTAPE 2 : Préparation (prepare_nakala_export.py)

**Objectif** : Créer la structure de dossiers pour Heimdall

```bash
python prepare_nakala_export.py \
    --fiches ./Fiches_Editions_Metadonnee/ \
    --verticaux ./Verticaux/ \
    --textes ./Textes/ \
    --output ./input/CiSaMe/
```

**Ce que le script fait :**
1. Parse les fiches .docx → extrait Edi-XX et "Libre de droits"
2. Scanne les verticaux → extrait Edi-XX depuis `<doc edition_id="...">`
3. Scanne les textes → lit pages_index.json
4. Associe tout par Edi-XX
5. Crée la structure de sortie :

```
input/CiSaMe/
├── Libre_de_droits/
│   ├── Brachylogus_Edi-101/
│   │   ├── pages_index.json    ← Métadonnées pour Heimdall
│   │   ├── vertical.txt        ← Corpus annoté
│   │   ├── fiche.pdf           ← Converti depuis .docx
│   │   ├── page_0001_xxx.txt
│   │   ├── page_0002_xxx.txt
│   │   └── ...
│   └── Autre_oeuvre_Edi-XX/
│       └── ...
│
└── Non_libre_de_droits/
    └── Oeuvre_restreinte_Edi-YY/
        └── ...
```

6. Convertit automatiquement les fiches .docx → .pdf via LibreOffice
7. Génère `rapport_export.txt` avec statistiques

**Options :**
- `--quiet` : Mode silencieux (moins de logs)

---

### ÉTAPE 3 : Upload Nakala (upload_nakala.py)

> **Note** : Le script `upload_nakala.py` n'est pas dans ce dépôt. Il fait partie du dépôt externe `nakala-uploader`. Voir les instructions ci-dessous pour son utilisation.

**Objectif** : Uploader les corpus sur Nakala via Heimdall

**Prérequis :**
- Installer Heimdall : `pip install heimdall`
- Avoir une clé API Nakala
- Cloner le dépôt `nakala-uploader`

**Configuration :**
Éditer le script pour configurer :
```python
API_KEY = 'votre-clé-api-nakala'
GROUP_KEY = 'votre-groupe-nakala'
```

**Exécution :**
```bash
# Pour les libres de droits
cd input/CiSaMe/Libre_de_droits/
python upload_nakala.py

# Pour les non libres (sur Seafile, pas Nakala)
# → Copier manuellement vers Seafile
```

**Paramètres importants dans le script :**
- `private=True` : Dépôt privé (mettre False pour public)
- `test=True` : Utilise l'API de test (mettre False pour production)

**Sortie :**
- Upload des fichiers sur Nakala
- Génère `output/cisame.xml` avec les DOI et métadonnées

---

### ÉTAPE 4 : Enrichissement URLs (add_nakala_links.py)

**Objectif** : Ajouter les liens Nakala dans les fichiers verticaux

**Prérequis :**
```bash
# Clé API obligatoire (variable d'environnement)
export NAKALA_API_KEY='votre-clé-api-nakala'

# Dépendance recommandée pour la sécurité XML
pip install defusedxml
```

```bash
python add_nakala_links.py cisame.xml [--test] [--dry-run] [--output corpus.txt] [--verbose]
```

**Options :**
- `--test` : Utilise l'API de test Nakala
- `--dry-run` : Simule sans modifier les fichiers
- `--output` / `-o` : Crée un fichier fusionnant tous les verticaux modifiés (utile pour NoSketch-Engine)
- `--verbose` / `-v` : Active les logs de debug

**Sécurité et robustesse :**
- La clé API est lue depuis la variable d'environnement `NAKALA_API_KEY` (jamais en dur dans le code)
- Le parsing XML utilise `defusedxml` si disponible (protection contre les attaques XXE)
- Les appels HTTP ont un timeout de 30s et un retry automatique (3 tentatives) sur les erreurs serveur
- Les URLs sont échappées avant insertion dans les attributs XML
- Un rapport de synthèse détaillé est affiché en fin d'exécution

**Ce que le script fait :**
1. Parse `cisame.xml` pour extraire les DOI
2. Récupère les hash SHA1 des fichiers via l'API Nakala (avec retry automatique)
3. Construit les URLs pour chaque page
4. Modifie les balises `<doc>` dans les verticaux
5. *(si `--output`)* Fusionne tous les verticaux modifiés en un fichier unique, trié par nom de fichier

**Modification des balises `<doc>` :**

**Avant :**
```xml
<doc edition_id="Edi-101" source="Brachylogus" page_number="1">
```

**Après :**
```xml
<doc link="https://nakala.fr/10.34847/xxx#sha1" fiche="https://nakala.fr/10.34847/xxx#sha2" edition_id="Edi-101" source="Brachylogus" page_number="1">
```

**Utilité :**
Ces attributs sont utilisés par NoSketch-Engine (MODULE 7) pour afficher :
- `link` : Lien vers l'image de la page sur Nakala
- `fiche` : Lien vers la fiche PDF sur Nakala

---

## 🛠️ Scripts utilitaires

### convert_fiches_to_pdf.py

**Quand l'utiliser :** Si vous devez convertir des fiches séparément

```bash
python convert_fiches_to_pdf.py ./dossier_fiches/ [--delete-docx] [--dry-run] [--verbose]
```

**Options :**
- `--delete-docx` : Supprime les .docx après conversion réussie
- `--dry-run` / `-n` : Simule sans convertir
- `--verbose` / `-v` : Active les logs de debug

**Prérequis :** LibreOffice installé (`soffice` dans le PATH). Le script vérifie automatiquement la disponibilité de `soffice` au démarrage.

**Robustesse :**
- Timeout de 120s par conversion (évite les blocages de LibreOffice)
- Try-except sur la suppression des .docx
- Rapport de synthèse en fin d'exécution (succès, erreurs)

---

### clean_dates.py

**Quand l'utiliser :** Si l'API Nakala refuse des dates vides

```bash
python clean_dates.py ./input/CiSaMe/ [--dry-run] [--recursive] [--verbose]
```

**Options :**
- `--dry-run` / `-n` : Simule sans modifier les fichiers
- `--recursive` / `-r` : Parcourt récursivement les sous-dossiers (par défaut : un seul niveau)
- `--verbose` / `-v` : Active les logs de debug

**Ce que ça fait :**
- Parcourt tous les `pages_index.json`
- Supprime la clé `date` lorsqu'elle est vide (`""`)
- Gère les deux formats de JSON (avec et sans clé `metadata`)

**Robustesse :**
- Try-except sur les lectures/écritures JSON
- Gestion des fichiers JSON malformés (warning au lieu de crash)

---

### flatten_textes.py

**Quand l'utiliser :** Si la structure des dossiers textes contient des fichiers vides ou des sous-dossiers `textes/` inutiles (provoque l'erreur `Unable to upload an empty file` lors de l'upload).

```bash
# Supprimer uniquement les fichiers vides (comportement par défaut)
python flatten_textes.py ./input/CiSaMe/ [--dry-run]

# Supprimer les fichiers vides ET aplatir les dossiers textes/
python flatten_textes.py ./input/CiSaMe/ --flatten [--dry-run]
```

**Options :**
- `--flatten` / `-f` : En plus de supprimer les fichiers vides, déplace le contenu des sous-dossiers `textes/` vers leur parent
- `--dry-run` / `-n` : Simule sans modifier les fichiers

**Ce que ça fait :**
- **Par défaut** : Supprime les fichiers de 0 octets (récursivement)
- **Avec `--flatten`** : En plus, trouve les sous-dossiers nommés `textes/`, déplace leur contenu vers le dossier parent, et supprime les dossiers `textes/` vides
- Génère un log des opérations

**Robustesse :**
- Limite de sécurité sur les conflits de noms de fichiers (max 10 000 tentatives)

---

### collect_verticals.sh

**Quand l'utiliser :** Pour collecter tous les fichiers `vertical.txt` dispersés dans les sous-dossiers et les rassembler dans un dossier unique (avec renommage pour éviter les conflits).

```bash
./collect_verticals.sh [chemin_source] [chemin_destination]
```

**Ce que ça fait :**
- Parcourt récursivement le dossier source
- Copie chaque `vertical.txt` en le préfixant avec le nom du dossier parent
- Exemple : `Brachylogus_Edi-101/vertical.txt` → `Brachylogus_Edi-101_vertical.txt`

---

### match_fiches_editions.py (usage rare)

**Quand l'utiliser :** Si les fiches n'ont PAS encore d'identifiant Edi-XX

```bash
python match_fiches_editions.py \
    --csv export-cisame.csv \
    --libres Ouvrages_libres_de_droits.docx \
    --dossier ./Fiches_Originales/ \
    --output ./Fiches_Enrichies/
```

**Ce que ça fait :**
- Matching flou entre fiches et base CSV (titre, auteur)
- Ajoute "Identifiant édition : Edi-XX" à la fin des fiches
- Ajoute "Libre de droits : Oui/Non"
- Normalisation des accents via `unicodedata` (gestion complète des caractères Unicode)
- Score de similarité plafonné à 1.0

**Note :** Ce script n'est plus nécessaire si les fiches contiennent déjà les identifiants.

---

### nakala_utils.py (module partagé)

**Ce fichier n'est pas un script exécutable.** C'est un module Python importé par les autres scripts du dossier. Il contient les fonctions communes :

- `normalize_filename()` : Normalise un nom pour le système de fichiers
- `normalize_text()` : Normalise le texte pour la comparaison (via `unicodedata`)
- `extract_info_from_docx()` : Extrait Edi-XX et métadonnées d'une fiche .docx
- `extract_info_from_vertical()` : Extrait Edi-XX d'un fichier vertical
- `load_libres_de_droits()` : Charge la liste des identifiants libres de droits
- `parse_edi_id_number()` : Parse un identifiant Edi-XX de manière sécurisée
- `edi_sort_key()` : Clé de tri pour les identifiants Edi-XX
- `match_textes_to_oeuvres()` : Matching des dossiers textes vers les oeuvres
- `validate_path_exists()` : Vérifie qu'un chemin existe avec log d'erreur
- `setup_logging()` : Configuration centralisée du logging

---

## 📊 Structure des données

### pages_index.json (lu par Heimdall)

```json
{
  "pages": [
    {
      "metadata": {
        "source": "Brachylogus",
        "author": "Anonyme",
        "type": "Droit romain",
        "date": "1166",
        "edition_id": "Edi-101"
      },
      "page_number": 1,
      "file": "page_0001_xxx.txt"
    }
  ]
}
```

### Métadonnées Nakala générées

| Champ JSON | Métadonnée Nakala |
|------------|-------------------|
| `source` | `dc:title` |
| `author` | `nakala:creator` |
| `type` | `dc:references` |
| `date` | `nakala:created` + `dc:date` |
| - | `dc:type` = "text" |
| - | `dc:license` = "etalab-2.0" |
| - | `dc:publisher` = "Université de Strasbourg" |

---

## ⚠️ Dépendances

```bash
pip install python-docx requests tqdm heimdall defusedxml
```

- **python-docx** : Lecture des fiches .docx
- **requests** : API Nakala
- **tqdm** : Barres de progression
- **heimdall** : Upload Nakala
- **defusedxml** : Parsing XML sécurisé (recommandé pour add_nakala_links.py)
- **LibreOffice** : Conversion PDF (`soffice`)

---

## 📚 Ressources

- **Nakala** : https://www.nakala.fr/
- **API Nakala** : https://api.nakala.fr/doc
- **Heimdall** : https://gitlab.huma-num.fr/huma-num/heimdall

---

## ✅ Checklist export

```
☐ 1. Vérifier que PAGEtopage a généré les verticaux + textes + pages_index.json
☐ 2. Lancer validate_export.py pour vérifier la cohérence
☐ 3. Corriger les erreurs identifiées
☐ 4. Lancer prepare_nakala_export.py pour créer la structure
☐ 5. Vérifier le rapport_export.txt
☐ 6. Configurer upload_nakala.py (API_KEY, GROUP_KEY, private, test)
☐ 7. Lancer l'upload sur Libre_de_droits/
☐ 8. Vérifier les DOI attribués
☐ 9. Lancer add_nakala_links.py pour enrichir les verticaux (avec -o pour le corpus fusionné)
☐ 10. Copier Non_libre_de_droits/ vers Seafile
```

---

*Dernière mise à jour : Février 2026*
