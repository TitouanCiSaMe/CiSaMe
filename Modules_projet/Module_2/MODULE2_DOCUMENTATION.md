# MODULE 2 - Méthodes de Téléchargement

**Documentation des différentes méthodes d'acquisition d'images de manuscrits**

---

## Vue d'ensemble

Le MODULE 2 détaille les différentes méthodes techniques pour télécharger les images de manuscrits identifiées dans le MODULE 1. Selon la bibliothèque numérique source, différentes approches sont nécessaires.

**Entrée** : URLs et sources identifiées (MODULE 1)
**Sortie** : Images haute résolution stockées sur Seafile
**Script principal** : `download_images.py` (à la racine du repository)

---

## Méthodes de téléchargement

### 1. Méthode IIIF (Recommandée)

**International Image Interoperability Framework**

**Avantages** :
- Standard international
- Automatisable via `manifest.json`
- Bonne à excellente qualité

**Processus** :
1. Retrouver le `manifest.json` sur le site de la bibliothèque numérique
2. Utiliser le script `download_images.py`
3. Téléchargement automatique des images

**Comment trouver le manifest.json** :
- Chercher dans les informations détaillées du manuscrit sur le site
- Souvent accessible via un bouton "IIIF" ou dans les métadonnées
- Pattern d'URL courant : `https://[domaine]/iiif/[id]/manifest.json`

**Bibliothèques compatibles** :
- Gallica (gallica.bnf.fr)
- Vatican (mss.vatlib.it)
- BVMM (bvmm.irht.cnrs.fr)
- EMMSM Université de Caen

**Script** : `download_images.py` (racine du repo)

```python
# Configuration dans le script
MANIFEST_PATH = "chemin/vers/manifest.json"
OUTPUT_DIR = "chemin/vers/sortie"
FILENAME_TEMPLATE = "{manuscript}_{index:04d}.jpg"
MAX_CONCURRENT = 10
RATE_LIMIT_DELAY = 5.0
```

---

### 2. Méthode PDF Direct

**Téléchargement et extraction depuis PDF**

**Avantages** :
- Méthode la plus simple quand disponible
- Pas besoin de script complexe

**Inconvénients** :
- Qualité variable selon le PDF source
- Nécessite extraction des images du PDF

**Processus** :
1. Télécharger le PDF depuis le site de la bibliothèque
2. Extraire les images du PDF (outils : `pdfimages`, Acrobat, etc.)
3. Vérifier la qualité des images extraites

**Qualité** : Variable (dépend du PDF source)

---

### 3. Méthodes Complexes

#### 3.1 Méthode Hexadécimale (British Library)

**Usage** : Spécifique à la British Library et sites similaires

**Principe** : Les URLs des images sont encodées en format hexadécimal

**Script** : Script British Library disponible dans le projet

**Qualité** : Très bonne

#### 3.2 Méthode des Tuiles

**Usage** : Certaines bibliothèques numériques (ex: Münchener Digitale)

**Principe** : Les images sont servies en tuiles qu'il faut reconstituer

**Qualité** : Excellente (haute résolution)

**Statut** : Script actuellement perdu, à recréer si besoin

#### 3.3 Méthode Manuelle

**Usage** : Dernier recours uniquement

**Processus** : Téléchargement page par page (clic droit → enregistrer)

**Inconvénients** :
- Très chronophage
- Qualité disparate
- Risque d'erreurs

---

## Comparaison des méthodes

| Méthode | Qualité | Automatisation | Difficulté |
|---------|---------|----------------|------------|
| **IIIF** | Bonne | Haute | Moyenne (trouver manifest) |
| **PDF** | Variable | Moyenne | Facile |
| **Hexadécimale** | Très bonne | Haute | Facile (script existant) |
| **Tuiles** | Excellente | Haute | Difficile (script perdu) |
| **Manuelle** | Disparate | Aucune | Fastidieuse |

---

## Stockage sur Seafile

Une fois téléchargées, toutes les images convergent vers le cloud universitaire Seafile.

**Organisation** :
- Nom : Nom du manuscrit + numéro de page
- Format : TIF ou JPG
- Résolution : 300-600 DPI (qualité native)

**Structure recommandée** :
```
Seafile/
└── CiSaMe/
    └── Manuscrits/
        ├── Admont_Stiftsbibl_7/
        │   ├── page_0001.jpg
        │   ├── page_0002.jpg
        │   └── ...
        ├── Vatican_Lat_123/
        └── ...
```

---

## Workflow recommandé

```
1. Identifier la source (MODULE 1)
       ↓
2. Déterminer la méthode selon la bibliothèque :
   - IIIF disponible ? → Utiliser download_images.py
   - PDF disponible ? → Télécharger et extraire
   - British Library ? → Méthode hexadécimale
   - Autre ? → Méthode manuelle (dernier recours)
       ↓
3. Télécharger les images
       ↓
4. Vérifier la qualité (300-600 DPI minimum)
       ↓
5. Uploader sur Seafile
       ↓
6. Vers MODULE 4 (eScriptorium)
```

---

## Conseils pratiques

### Trouver un manifest.json

1. Ouvrir la page du manuscrit sur la bibliothèque numérique
2. Chercher un bouton/lien "IIIF" (souvent un logo en forme de "II")
3. Inspecter les métadonnées ou informations détaillées
4. Utiliser les outils de développement du navigateur (F12) pour chercher les requêtes contenant "manifest" ou "iiif"

### Qualité des images

- **Minimum requis** : 300 DPI pour OCR/HTR correct
- **Idéal** : 400-600 DPI pour meilleure précision
- **Formats préférés** : TIF (sans perte) ou JPG haute qualité

### Rate limiting

Le script `download_images.py` inclut un délai configurable pour respecter les serveurs :
- Défaut : 5 secondes entre chaque téléchargement
- Ajuster selon les politiques de la bibliothèque

---

## Outils et technologies

**Script principal** : `download_images.py`

**Bibliothèques Python** :
- `requests` : Requêtes HTTP
- `tqdm` : Progress bars
- `json` : Parsing des manifests
- `pathlib` : Gestion des chemins

**Fonctionnalités du script** :
- Lecture du manifest.json IIIF
- Extraction des URLs des images
- Téléchargement parallèle (configurable)
- Skip automatique des fichiers existants
- Retry avec backoff exponentiel
- Rate limiting

---

## Lien avec les autres modules

**En amont** : MODULE 1 (Identification des sources)

**En aval** : MODULE 4 (Traitement eScriptorium)
- Les images téléchargées servent de base pour la segmentation et transcription
- Qualité 300-600 DPI essentielle pour la reconnaissance automatique

---

## Fichiers associés

```
/
├── download_images.py                    # Script principal IIIF
├── Documentation/
│   └── README_MANUSCRIPT_DOWNLOADER.md   # Documentation du script
└── Modules_projet/
    └── Module_2/
        ├── flowchart-module2.mmd         # Schéma du workflow
        └── MODULE2_DOCUMENTATION.md      # Cette documentation
```

---

## Statut

**MODULE 2** : Opérationnel

- Script IIIF : Fonctionnel
- Script hexadécimal : Fonctionnel
- Script tuiles : Perdu (à recréer si besoin)
- Méthode manuelle : Toujours disponible en fallback

---

*Dernière mise à jour : Décembre 2025*
