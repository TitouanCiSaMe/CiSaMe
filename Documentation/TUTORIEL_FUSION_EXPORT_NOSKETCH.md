# Tutoriel : Fusion et Export vers NoSketch Engine

## Pour débutants en ligne de commande (Mac/Linux)

---

## Introduction

Ce tutoriel vous guide pas à pas pour :
1. **Fusionner** tous vos fichiers verticaux en un seul fichier
2. **Exporter** ce fichier vers le serveur NoSketch Engine

Pas de panique ! Chaque étape est expliquée en détail, même si vous n'avez jamais utilisé le Terminal.

---

## Prérequis

Avant de commencer, assurez-vous d'avoir :
- [ ] Python 3 installé sur votre ordinateur
- [ ] Les fichiers `.vertical.txt` générés par le Module 6 (PAGEtopage)
- [ ] Les identifiants de connexion au serveur NoSketch
- [ ] Environ 15 minutes devant vous

---

## 📋 Table des matières

1. [Ouvrir le Terminal](#1-ouvrir-le-terminal)
2. [Naviguer vers le bon dossier](#2-naviguer-vers-le-bon-dossier)
3. [Fusionner les fichiers verticaux](#3-fusionner-les-fichiers-verticaux)
4. [Exporter vers le serveur](#4-exporter-vers-le-serveur)
5. [Compiler le corpus](#5-compiler-le-corpus-sur-le-serveur)
6. [Résolution de problèmes](#6-résolution-de-problèmes)

---

## 1. Ouvrir le Terminal

### Sur Mac
1. Appuyez sur `Cmd + Espace` (ouvre Spotlight)
2. Tapez `Terminal`
3. Appuyez sur `Entrée`

### Sur Linux
1. Appuyez sur `Ctrl + Alt + T`

   **OU**

2. Cherchez "Terminal" dans vos applications

### À quoi ça ressemble ?

Vous verrez une fenêtre avec du texte qui ressemble à :
```
utilisateur@ordinateur:~$
```

C'est normal ! C'est votre **invite de commande**. Elle attend que vous tapiez des commandes.

---

## 2. Naviguer vers le bon dossier

### Comprendre où vous êtes

Le Terminal travaille toujours dans un **dossier** (aussi appelé "répertoire").

Pour savoir où vous êtes :
```bash
pwd
```

**Explication** : `pwd` = "Print Working Directory" (Afficher le dossier actuel)

Vous verrez quelque chose comme :
```
/Users/votrenom/
```

### Aller vers le dossier CiSaMe

Utilisez la commande `cd` (Change Directory = Changer de dossier) :

```bash
cd /chemin/vers/CiSaMe
```

**Exemple concret** :
```bash
cd /Users/titouan/Documents/Github/CiSaMe
```

> **💡 Astuce Mac/Linux** : Au lieu de taper le chemin, vous pouvez :
> 1. Taper `cd ` (avec un espace après)
> 2. Glisser-déposer le dossier CiSaMe dans le Terminal
> 3. Appuyer sur `Entrée`

### Vérifier que vous êtes au bon endroit

Listez les fichiers du dossier :
```bash
ls
```

Vous devriez voir le dossier `Documentation` apparaître dans la liste.

---

## 3. Fusionner les fichiers verticaux

### Étape 3.1 : Préparer vos fichiers

Assurez-vous que tous vos fichiers `.vertical.txt` sont dans un même dossier.

**Exemple de structure** :
```
/Users/votrenom/Documents/Corpus/
├── texte_edition_1.vertical.txt
├── texte_edition_2.vertical.txt
├── texte_edition_3.vertical.txt
└── ...
```

### Étape 3.2 : Créer un script de fusion simple

Nous allons créer un petit fichier pour faciliter la fusion.

#### Option A : Utilisation du script existant (recommandé)

Le script `Fusion_txt_NoSketch.py` est déjà dans le dossier `Documentation`.

Ouvrez-le avec un éditeur de texte et modifiez les lignes 53 et 56 :

```python
# Ligne 53 : Chemin vers votre dossier contenant les fichiers .vertical.txt
dossier = "/Users/votrenom/Documents/Corpus"

# Ligne 56 : Chemin où sauvegarder le fichier fusionné
fichier_sortie = "/Users/votrenom/Documents/Corpus/Corpus.txt"
```

**Ensuite, exécutez le script** :
```bash
python Documentation/Fusion_txt_NoSketch.py
```

#### Option B : Script simplifié en une commande

Si vous préférez ne pas modifier le fichier, voici une commande directe :

```bash
python -c "
import os

dossier = '/Users/votrenom/Documents/Corpus'  # ⚠️ MODIFIEZ CE CHEMIN
fichier_sortie = '/Users/votrenom/Documents/Corpus/Corpus.txt'  # ⚠️ ET CELUI-CI

fichiers = sorted([f for f in os.listdir(dossier) if f.endswith('.vertical.txt')])

with open(fichier_sortie, 'w', encoding='utf-8') as dest:
    for fichier in fichiers:
        print(f'Fusion de {fichier}...')
        with open(os.path.join(dossier, fichier), 'r', encoding='utf-8') as src:
            dest.write(src.read())
            dest.write('\n\n')  # Séparateur entre fichiers

print(f'✓ Fusion terminée ! Fichier créé : {fichier_sortie}')
"
```

> **⚠️ IMPORTANT** : Remplacez `/Users/votrenom/Documents/Corpus` par le vrai chemin vers votre dossier !

### Étape 3.3 : Vérifier le résultat

Vous devriez voir des messages comme :
```
Fusion de texte_edition_1.vertical.txt...
Fusion de texte_edition_2.vertical.txt...
Fusion de texte_edition_3.vertical.txt...
✓ Fusion terminée ! Fichier créé : /Users/votrenom/Documents/Corpus/Corpus.txt
```

Vérifiez que le fichier `Corpus.txt` existe :
```bash
ls -lh /Users/votrenom/Documents/Corpus/Corpus.txt
```

Vous verrez la taille du fichier (exemple : `15M` = 15 mégaoctets).

---

## 4. Exporter vers le serveur

### Étape 4.1 : Comprendre la commande SCP

`scp` = "Secure Copy" = Copier un fichier de manière sécurisée vers un autre ordinateur

**Structure de la commande** :
```bash
scp [fichier_source] [utilisateur]@[serveur]:[dossier_destination]
```

### Étape 4.2 : Exécuter l'export

**Commande complète** (exemple avec le serveur Unistra) :
```bash
scp /Users/votrenom/Documents/Corpus/Corpus.txt debian@fip-185-155-93-80.iaas.unistra.fr:/home/debian/NoSketch-Engine-Docker/corpora/cisame/vertical/
```

**Décomposition de la commande** :
- `scp` : la commande de copie sécurisée
- `/Users/votrenom/Documents/Corpus/Corpus.txt` : votre fichier local
- `debian` : nom d'utilisateur sur le serveur
- `@` : séparateur
- `fip-185-155-93-80.iaas.unistra.fr` : adresse du serveur
- `:` : séparateur
- `/home/debian/NoSketch-Engine-Docker/corpora/cisame/vertical/` : dossier sur le serveur

### Étape 4.3 : Entrer le mot de passe

Après avoir appuyé sur `Entrée`, on vous demandera :
```
debian@fip-185-155-93-80.iaas.unistra.fr's password:
```

Tapez le mot de passe (⚠️ vous ne verrez rien s'afficher, c'est normal !) puis appuyez sur `Entrée`.

### Étape 4.4 : Suivre la progression

Vous verrez une barre de progression :
```
Corpus.txt                    100%   15MB   2.5MB/s   00:06
```

Cela signifie que le fichier est en train d'être copié. Attendez que ce soit terminé.

---

## 5. Compiler le corpus sur le serveur

### Étape 5.1 : Se connecter au serveur

```bash
ssh debian@fip-185-155-93-80.iaas.unistra.fr
```

**Explication** : `ssh` = "Secure Shell" = Se connecter à un autre ordinateur en ligne de commande

On vous demandera à nouveau le mot de passe. Tapez-le et appuyez sur `Entrée`.

### Étape 5.2 : Aller dans le bon dossier

```bash
cd /home/debian/NoSketch-Engine-Docker/corpora/cisame/vertical/
```

### Étape 5.3 : Vérifier que le fichier est bien là

```bash
ls -lh Corpus.txt
```

Vous devriez voir :
```
-rw-r--r-- 1 debian debian 15M Dec 16 14:32 Corpus.txt
```

### Étape 5.4 : Compiler le corpus

```bash
compilecorp --config cisame_corpus.xml
```

**Explication** : Cette commande transforme votre fichier `.txt` en un format optimisé pour les recherches dans NoSketch.

La compilation peut prendre plusieurs minutes selon la taille de votre corpus.

Vous verrez des messages comme :
```
Indexing corpus...
Building frequency lists...
Creating concordance indices...
✓ Compilation complete!
```

### Étape 5.5 : Se déconnecter du serveur

```bash
exit
```

Vous revenez à votre Terminal local.

---

## 6. Résolution de problèmes

### Problème : "python: command not found"

**Solution** :
```bash
python3 Documentation/Fusion_txt_NoSketch.py
```

Sur certains systèmes, il faut utiliser `python3` au lieu de `python`.

---

### Problème : "Permission denied" lors du SCP

**Causes possibles** :
1. Mauvais mot de passe
2. Pas les droits d'écriture sur le serveur

**Solution** :
Vérifiez vos identifiants et contactez l'administrateur du serveur.

---

### Problème : "No such file or directory"

**Cause** : Le chemin que vous avez tapé n'existe pas.

**Solution** :
1. Vérifiez l'orthographe du chemin
2. Utilisez `pwd` pour savoir où vous êtes
3. Utilisez `ls` pour voir les dossiers disponibles

---

### Problème : "Connection refused" ou "Connection timeout"

**Causes possibles** :
1. Le serveur est éteint
2. Problème de connexion internet
3. Adresse du serveur incorrecte

**Solution** :
1. Vérifiez votre connexion internet
2. Vérifiez l'adresse du serveur
3. Contactez l'administrateur

---

### Problème : La fusion ne contient qu'un seul fichier

**Cause** : L'extension `.vertical.txt` n'est pas reconnue.

**Solution** :
Dans le script, modifiez la ligne pour chercher la bonne extension :
```python
fichiers = sorted([f for f in os.listdir(dossier) if f.endswith('.vertical.txt')])
```

---

## 📚 Récapitulatif des commandes

```bash
# 1. Naviguer vers CiSaMe
cd /chemin/vers/CiSaMe

# 2. Fusionner les fichiers
python Documentation/Fusion_txt_NoSketch.py

# 3. Exporter vers le serveur
scp /chemin/Corpus.txt debian@serveur:/chemin/destination/

# 4. Se connecter au serveur
ssh debian@serveur

# 5. Aller dans le dossier
cd /home/debian/NoSketch-Engine-Docker/corpora/cisame/vertical/

# 6. Compiler
compilecorp --config cisame_corpus.xml

# 7. Se déconnecter
exit
```

---

## 💡 Astuces pour gagner du temps

### Astuce 1 : Historique des commandes
Utilisez la flèche `↑` (haut) pour rappeler les commandes précédentes au lieu de les retaper.

### Astuce 2 : Autocomplétion
Appuyez sur `Tab` pour compléter automatiquement les noms de fichiers et dossiers.

Exemple :
```bash
cd Doc[Tab]
# Devient automatiquement :
cd Documentation/
```

### Astuce 3 : Copier-coller dans le Terminal
- **Mac** : `Cmd + C` pour copier, `Cmd + V` pour coller
- **Linux** : `Ctrl + Shift + C` pour copier, `Ctrl + Shift + V` pour coller

### Astuce 4 : Créer un alias
Pour ne pas retaper la longue commande SCP à chaque fois, ajoutez ceci à votre fichier `~/.bashrc` ou `~/.zshrc` :

```bash
alias export-nosketch='scp /Users/votrenom/Documents/Corpus/Corpus.txt debian@fip-185-155-93-80.iaas.unistra.fr:/home/debian/NoSketch-Engine-Docker/corpora/cisame/vertical/'
```

Ensuite, vous pourrez simplement taper :
```bash
export-nosketch
```

---

## ✅ Checklist finale

Avant de commencer, vérifiez que vous avez :
- [ ] Python installé (`python --version` ou `python3 --version`)
- [ ] Les fichiers `.vertical.txt` prêts
- [ ] Les identifiants du serveur (utilisateur, mot de passe, adresse)
- [ ] Une connexion internet stable

Pendant le processus :
- [ ] Fusion réussie → fichier `Corpus.txt` créé
- [ ] Export SCP terminé → barre de progression à 100%
- [ ] Connexion SSH réussie → vous êtes sur le serveur
- [ ] Compilation terminée → message de succès

---

## 📞 Besoin d'aide ?

Si vous rencontrez un problème non listé dans ce tutoriel :

1. Notez le **message d'erreur exact**
2. Notez la **commande** que vous avez tapée
3. Consultez la documentation complète dans :
   - `Modules_projet/Module_7_NoSketch_Engine/MODULE_NOSKETCH_ENGINE_DOCUMENTATION.md`
   - `PAGEtopage/README.md`

---

## 🎓 Pour aller plus loin

Une fois à l'aise avec ces commandes, vous pouvez :
- Automatiser le processus avec des scripts Bash
- Configurer une connexion SSH sans mot de passe (avec des clés SSH)
- Utiliser `rsync` au lieu de `scp` pour des transferts plus rapides
- Planifier des tâches automatiques avec `cron`

---

**Dernière mise à jour** : Décembre 2024
**Testé sur** : macOS Sonoma, Ubuntu 22.04, Debian 11
