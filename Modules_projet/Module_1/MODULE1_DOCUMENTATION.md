# 📜 MODULE 1 - RÉCUPÉRATION DE MANUSCRITS

**Documentation de la méthode actuelle**

---

## 📋 Vue d'ensemble

MODULE 1 gère l'acquisition des manuscrits juridiques médiévaux, soit par **achat** auprès des bibliothèques, soit par **scraping web** depuis les bibliothèques numériques.

**Corpus** : 317 manuscrits juridiques médiévaux
**Source** : Liste fournie par les chercheurs (`Liste MSS juridiques.docx`)

---

## 🔄 Workflow actuel

### Étape 1 : Liste initiale des manuscrits

Les chercheurs fournissent une liste des manuscrits à acquérir au format DOCX avec :
- **Colonne 1** : Nom du manuscrit (ex: "Admont, Stiftsbibl., 7")
- **Colonne 2** : Informations sur la numérisation
  - URL de la bibliothèque numérique si disponible
  - Note "CiSaMe has full HD ms" si déjà téléchargé
  - "/" si non disponible
  - Notes diverses ("Pas de manifest iiif", "Impossible bonne qualité", etc.)

**Format actuel** : Document Word avec tableau
**Conversion** : Extraction en CSV pour faciliter l'analyse programmatique

### Étape 2 : Identification de la source (Manuel)

Pour chaque manuscrit, identification de la méthode d'acquisition :

**A. Achat nécessaire**
- Manuscrit non numérisé
- Manuscrit numérisé mais pas en ligne
- Contact direct avec la bibliothèque

**B. Scraping web possible**
- Manuscrit disponible sur bibliothèque numérique
- Accès libre ou restreint

### Étape 3 : Choix de la méthode de téléchargement (Manuel)

Quand le scraping est possible, choix de la méthode selon la bibliothèque et la qualité :

**Ordre de préférence (selon facilité ET qualité)** :

1. **PDF direct** ⭐⭐
   - Si export PDF complet et bonne qualité
   - Méthode la plus simple
   - Qualité : variable

2. **IIIF** ⭐⭐⭐
   - Recherche du `manifest.json`
   - Format standard international
   - Qualité : bonne à excellente
   - **Défi** : "J'ai beaucoup galéré pour trouver les manifest.json"

3. **Méthode Hexadécimale** ⭐⭐⭐⭐
   - British Library principalement
   - URLs en format hexadécimal
   - Algorithme spécial nécessaire
   - Qualité : très bonne

4. **Méthode des Tuiles** ⭐⭐⭐⭐⭐
   - Bibliothèque numérique spécifique (je ne sais plus laquelle)
   - Reconstruction d'image par tuiles
   - Algorithme complexe (perdu, à recréer)
   - Qualité : excellente

5. **Manuel** ⭐ (dernier recours)
   - Page par page, clic droit → enregistrer
   - Chronophage
   - Qualité disparate
   - Utilisé uniquement si rien d'autre ne fonctionne

**Remarque importante** : Une fois la méthode identifiée pour une bibliothèque, elle est la même pour tous les manuscrits de cette bibliothèque.

**Exemples de correspondances** :
- Gallica, Vatican, BNF → IIIF
- British Library → Hexadécimale
- Münchener → Tuiles (algorithme perdu)

### Étape 4 : Téléchargement

**Script principal** : `download_images.py`

**Fonctionnalités** :
- Lecture du manifest.json IIIF
- Extraction des URLs des images
- Téléchargement parallèle (configurable)
- Skip automatique des fichiers déjà téléchargés
- Retry avec backoff exponentiel
- Progress bar détaillée
- Rate limiting pour respecter les serveurs

**Paramètres configurables** :
```python
MANIFEST_PATH = "chemin/vers/manifest.json"
OUTPUT_DIR = "chemin/vers/sortie"
FILENAME_TEMPLATE = "{manuscript}_{index:04d}.jpg"
MAX_CONCURRENT = 10
RATE_LIMIT_DELAY = 5.0
```

**Autres scripts** :
- Script British Library (méthode hexadécimale) - existe
- Script Tuiles - perdu, à recréer si besoin

### Étape 5 : Upload sur Seafile

Les images téléchargées sont uploadées sur le cloud universitaire Seafile avec :
- **Nom** : Nom du manuscrit + numéro de page
- **Format** : TIF ou JPG
- **Résolution** : 300-600 DPI (qualité native)

---

## 📊 Statistiques

**Corpus total** : 317 manuscrits juridiques médiévaux

**Répartition observée** (d'après la liste) :
- ~20 manuscrits déjà téléchargés ("CiSaMe has full HD ms")
- ~200 manuscrits avec URLs actives (à télécharger)
- ~50 manuscrits non disponibles ("/" ou "Pas trouvé")
- Quelques cas avec problèmes de qualité ("Impossible bonne qualité")

**Bibliothèques principales identifiées** :
- BVMM (bvmm.irht.cnrs.fr) - IIIF
- Gallica (gallica.bnf.fr) - IIIF
- Vatican (mss.vatlib.it) - IIIF
- manuscripta.at - Pas IIIF
- EMMSM Université de Caen (emmsm.unicaen.fr) - IIIF
- British Library - Hexadécimale
- Münchener Digitale - Tuiles
- Manoscritti giuridici medievali (beic.it) - Variable

---

## ⏱️ Temps de traitement

**Temps moyen par manuscrit** : ~10 minutes

**Détail** :
- Identification source : 1-2 min
- Recherche manifest.json (si IIIF) : 5-8 min (phase la plus chronophage)
- Configuration et lancement script : 1-2 min
- Téléchargement : automatique (dépend du nombre de pages)

**Pour 317 manuscrits** : ~53 heures de travail

**Facteur de répétition** : Élevé
- Même bibliothèque = même méthode
- Mais tests refaits à chaque manuscrit

---

## 🎯 Points forts de la méthode

1. ✅ **Scripts de téléchargement robustes**
   - Gestion d'erreurs complète
   - Reprise automatique
   - Skip des fichiers existants
   - Très fiable

2. ✅ **Priorisation qualité**
   - Choix de la méthode selon qualité finale
   - Pas de compromis sur la résolution

3. ✅ **Stockage organisé**
   - Noms de fichiers clairs
   - Cloud universitaire sécurisé
   - Métadonnées préservées

4. ✅ **Flexibilité**
   - Multiple méthodes disponibles
   - Adaptation selon la bibliothèque
   - Fallback sur manuel si nécessaire

---

## 💡 Pistes d'amélioration possibles

_Note : Ces améliorations ne sont que des pistes pour économiser du temps à l'avenir si le projet devait traiter davantage de manuscrits._

### 1. Capitalisation du savoir
Une base de données simple (JSON ou CSV) pourrait documenter quelle méthode fonctionne pour chaque bibliothèque, évitant ainsi de refaire les tests à chaque manuscrit de la même source.

### 2. Détection automatique des manifest.json
Les manifest IIIF suivent souvent des patterns d'URL prévisibles selon la bibliothèque. Un script pourrait automatiser leur détection une fois les patterns documentés.

### 3. Enrichissement de la liste
La liste CSV pourrait être enrichie avec des colonnes supplémentaires (Bibliothèque, Méthode, Statut) pour faciliter le suivi de la progression et le filtrage.

### 4. Batch processing
Pour les manuscrits IIIF d'une même bibliothèque, un script pourrait automatiser le téléchargement en série une fois les manifest identifiés.

---

## 🛠️ Outils et technologies

**Scripts Python** :
- `download_images.py` : Téléchargement IIIF
- Script British Library : Méthode hexadécimale
- (Script Tuiles : perdu)

**Bibliothèques Python utilisées** :
- `requests` : Requêtes HTTP
- `tqdm` : Progress bars
- Standard library : `json`, `pathlib`, etc.

**Stockage** :
- Seafile : Cloud universitaire
- Format : TIF/JPG haute résolution (300-600 DPI)

**Format des données** :
- Liste manuscrits : DOCX → CSV
- Manifests IIIF : JSON
- Images : TIF/JPG

---

## 📁 Fichiers du MODULE 1

```
/
├── Liste MSS juridiques.docx          # Liste originale des chercheurs
├── liste_manuscrits.csv               # Extraction CSV (317 manuscrits)
├── download_images.py                 # Script téléchargement IIIF
├── README_MANUSCRIPT_DOWNLOADER.md    # Documentation du script
└── (script British Library)           # Méthode hexadécimale
```

---

## 📝 Notes de terrain

**Difficultés rencontrées** :
- Recherche des manifest.json chronophage et répétitive
- Chaque bibliothèque a sa propre structure d'URL
- Pas de documentation centralisée des méthodes par bibliothèque
- Script Tuiles perdu (haute qualité mais à recréer si besoin)

**Solutions adoptées** :
- Tests manuels systématiques par ordre de préférence
- Documentation au fur et à mesure dans la liste
- Scripts robustes avec gestion d'erreurs

**Cas spéciaux identifiés** :
- "Pas de manifest iiif" → Fallback sur PDF ou autre méthode
- "Impossible bonne qualité" → Manuscrit disponible mais qualité insuffisante
- "CiSaMe has full HD ms" → Déjà traité, skip

---

## 🔗 Lien avec les modules suivants

**Sortie du MODULE 1** : Images haute résolution sur Seafile

**Entre dans MODULE 4** : Traitement eScriptorium
- Les images téléchargées servent de base pour la segmentation et transcription
- Qualité 300-600 DPI essentielle pour la reconnaissance automatique
- Format TIF/JPG compatible avec eScriptorium

---

## ✅ État actuel

**MODULE 1** : ✅ **Opérationnel et terminé**

- Scripts de téléchargement fonctionnels
- Méthodes identifiées et testées
- Workflow stabilisé
- Prêt pour traitement de nouveaux manuscrits si nécessaire

**Améliorations futures** : Optionnelles, uniquement si volume de manuscrits augmente significativement.
