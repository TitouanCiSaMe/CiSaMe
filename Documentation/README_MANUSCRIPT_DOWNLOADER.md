# 📥 Téléchargeur de Manuscrits IIIF

Script Python robuste pour télécharger des manuscrits numérisés depuis des manifests JSON IIIF.

## ✨ Fonctionnalités

- ✅ **Téléchargement intelligent** : Skip automatique des pages déjà téléchargées
- ✅ **Reprise automatique** : Relancez le script après une interruption, seules les pages manquantes seront téléchargées
- ✅ **Gestion d'erreurs robuste** : Retry automatique avec backoff exponentiel
- ✅ **Validation complète** : Vérification des codes HTTP, timeouts, gestion des exceptions
- ✅ **Progress bar détaillée** : Suivi en temps réel (téléchargées/ignorées/échouées)
- ✅ **Logging complet** : Fichier de log pour diagnostiquer les problèmes
- ✅ **Chemins configurables** : Pas de chemins codés en dur
- ✅ **Rate limiting** : Délai configurable pour respecter les serveurs

## 🚀 Installation

### Prérequis

Python 3.7 ou supérieur

### Dépendances

```bash
pip install requests tqdm
```

Ou avec le fichier requirements (si disponible) :

```bash
pip install -r requirements.txt
```

## 📖 Utilisation

### Configuration de base

1. **Éditez le script** `download_images.py` (à la racine du projet) et modifiez la section CONFIGURATION :

```python
MANIFEST_PATH = "/chemin/vers/votre/manifest.json"
OUTPUT_DIR = "/chemin/vers/dossier/sortie/NomManuscrit"
FILENAME_TEMPLATE = "{manuscript}_{index:04d}.jpg"
DELAY = 2.0          # Délai entre chaque téléchargement (secondes)
MAX_RETRIES = 3      # Nombre de tentatives en cas d'échec
```

2. **Lancez le script** :

```bash
python download_images.py
```

### Exemple complet

```python
# Configuration pour télécharger le manuscrit Latin 18108
MANIFEST_PATH = "/home/titouan/Téléchargements/Manuscrit_télécharger/manifest.json"
OUTPUT_DIR = "/home/titouan/Téléchargements/Manuscrit_télécharger/Latin_18108"
FILENAME_TEMPLATE = "{manuscript}_{index:04d}.jpg"
DELAY = 2.0
```

Résultat : Les images seront téléchargées avec les noms :
- `Latin_18108_0001.jpg`
- `Latin_18108_0002.jpg`
- `Latin_18108_0003.jpg`
- ...

### Templates de noms de fichiers

Le paramètre `FILENAME_TEMPLATE` supporte plusieurs variables :

```python
# Exemples de templates :

# Numérotation simple avec padding
"{manuscript}_{index:04d}.jpg"  # → Latin_18108_0001.jpg

# Sans padding
"page_{index}.jpg"  # → page_1.jpg, page_2.jpg

# Avec total de pages
"{manuscript}_page_{index}_sur_{total}.jpg"  # → Latin_18108_page_1_sur_500.jpg

# Nom fixe avec index
"manuscrit_{index:05d}.jpg"  # → manuscrit_00001.jpg
```

## 📊 Exemple de sortie

```
======================================================================
📥 TÉLÉCHARGEMENT DE MANUSCRIT DEPUIS MANIFEST IIIF
======================================================================
Manifest       : /home/titouan/Téléchargements/manifest.json
Dossier sortie : /home/titouan/Téléchargements/Latin_18108
Délai/image    : 2.0s
Max retries    : 3
======================================================================

📖 Lecture du manifest : /home/titouan/Téléchargements/manifest.json
   → 1523 IDs trouvés
   → 487 URLs d'images .jpg
💾 URLs sauvegardées dans : Latin_18108/urls_downloaded.txt

📥 Téléchargement de 487 images...

Téléchargement: 100%|████████████████| 487/487 [15:24<00:00, 1.90s/img]
                téléchargées: 50, ignorées: 435, échouées: 2

======================================================================
📊 RÉSUMÉ DU TÉLÉCHARGEMENT
======================================================================
Total d'images       : 487
✓ Téléchargées       : 50
⊘ Ignorées (existent): 435
✗ Échouées           : 2
Taille téléchargée   : 125.3 MB
Taux de succès       : 99.6%
======================================================================

⚠️  2 image(s) n'ont pas pu être téléchargée(s)
   Consultez le log : Latin_18108/download.log

✅ 50 nouvelle(s) image(s) téléchargée(s) avec succès!
ℹ️  435 image(s) déjà présente(s), ignorée(s)
```

## 🔧 Cas d'utilisation

### 1. Téléchargement initial complet

```bash
python download_images.py
```

Télécharge toutes les pages du manuscrit.

### 2. Reprise après interruption

Si le téléchargement est interrompu (Ctrl+C, panne réseau, etc.), relancez simplement :

```bash
python download_images.py
```

Le script **détecte automatiquement** les pages déjà téléchargées et ne télécharge que les manquantes.

### 3. Téléchargement de pages manquantes

Vous avez téléchargé un manuscrit mais il vous manque des pages ?

**Aucune action spéciale nécessaire !** Relancez simplement le script :

```bash
python download_images.py
```

Le script :
1. ✅ Ignore les pages déjà présentes (affichées comme "ignorées")
2. ✅ Télécharge uniquement les pages manquantes
3. ✅ Conserve votre progression

### 4. Forcer le re-téléchargement

Si vous voulez re-télécharger toutes les images (par exemple, si certaines sont corrompues) :

1. Supprimez le dossier de sortie ou les images spécifiques
2. Relancez le script

## 📁 Structure des fichiers générés

```
Dossier_de_sortie/
├── Latin_18108_0001.jpg      # Images téléchargées
├── Latin_18108_0002.jpg
├── Latin_18108_0003.jpg
├── ...
├── urls_downloaded.txt        # Liste des URLs (optionnel)
└── download.log              # Fichier de log détaillé
```

## 🐛 Dépannage

### Le manifest n'est pas trouvé

```
❌ Manifest non trouvé : /chemin/vers/manifest.json
```

**Solution** : Vérifiez que le chemin `MANIFEST_PATH` dans le script est correct.

### Échecs de téléchargement

```
⚠️  Échec tentative 1/3 pour Latin_18108_0042.jpg: Connection timeout
⏳ Nouvelle tentative dans 2s...
```

**Normal** : Le script réessaie automatiquement (3 tentatives par défaut).

**Si l'échec persiste** : Consultez le fichier `download.log` pour plus de détails.

### Trop lent / Trop rapide

Ajustez le paramètre `DELAY` :

```python
DELAY = 0.5   # Plus rapide (attention à ne pas surcharger le serveur)
DELAY = 5.0   # Plus lent (plus respectueux du serveur)
```

### Problème de mémoire

Le script utilise le streaming pour télécharger les images, il ne devrait pas consommer beaucoup de mémoire. Si vous rencontrez des problèmes, vérifiez l'espace disque disponible.

## 🆚 Comparaison avec le script original

| Aspect | Script original | Script amélioré |
|--------|----------------|-----------------|
| **Bug range(1, len)** | ❌ Manque la 1ère image | ✅ Corrigé |
| **Skip fichiers existants** | ❌ Non | ✅ Oui (fonctionnalité clé) |
| **Gestion d'erreurs** | ❌ Aucune | ✅ Retry + validation HTTP |
| **Reprise après crash** | ❌ Recommence à zéro | ✅ Reprend où c'était arrêté |
| **Validation HTTP** | ❌ Non | ✅ Status codes vérifiés |
| **Timeouts** | ❌ Blocage possible | ✅ Timeout de 30s |
| **Logging** | ❌ Aucun | ✅ Fichier log détaillé |
| **Chemins configurables** | ❌ Codés en dur | ✅ Variables en haut du script |
| **Progress bar** | ✅ Basique | ✅ Détaillée avec compteurs |
| **Double slash bug** | ❌ `//home/...` | ✅ Chemins corrects avec Path |

## 📝 Corrections apportées

### Bug critique : range(1, len)

**Avant** :
```python
for i in range(1, len(jpg_ids)):  # ❌ Saute la 1ère image
```

**Après** :
```python
for i in range(len(jpg_ids)):  # ✅ Toutes les images
```

### Chemin invalide

**Avant** :
```python
f'//home/titouan/...'  # ❌ Double slash
```

**Après** :
```python
file_path = self.output_dir / filename  # ✅ Path correct
```

### Pas de gestion d'erreurs

**Avant** :
```python
response = requests.get(url)  # ❌ Pas de timeout, pas de validation
```

**Après** :
```python
response = requests.get(url, timeout=30, stream=True)
response.raise_for_status()  # ✅ Lève une exception si erreur HTTP
```

## 🤝 Contribution

N'hésitez pas à améliorer ce script en ajoutant :
- Support pour d'autres formats (PDF, TIFF, etc.)
- Téléchargement parallèle pour plus de vitesse
- Interface graphique
- Configuration via fichier JSON/YAML

## 📄 Licence

Ce script est fourni tel quel, sans garantie. Utilisez-le librement pour vos projets de recherche et de numérisation.

## 🙏 Crédits

Développé pour faciliter le téléchargement de manuscrits numérisés depuis les bibliothèques numériques utilisant le standard IIIF.

---

**Astuce** : Pour télécharger plusieurs manuscrits, dupliquez le script avec des noms différents (ex: `download_latin_18108.py`, `download_grec_1234.py`) ou créez une boucle qui itère sur plusieurs manifests.
