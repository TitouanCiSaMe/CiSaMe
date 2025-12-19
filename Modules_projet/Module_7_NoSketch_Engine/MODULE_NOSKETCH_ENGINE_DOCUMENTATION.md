# MODULE NOSKETCH-ENGINE - Documentation complète

## Vue d'ensemble

Le module NoSketch-Engine constitue la dernière étape du pipeline CiSaMe, permettant l'analyse linguistique interactive des corpus enrichis. Il transforme les fichiers verticaux lemmatisés (sortie du MODULE 6) en corpus interrogeables via l'interface NoSketch-Engine.

## Objectif

Créer un corpus interrogeable sur NoSketch-Engine permettant :
- Des recherches par lemme, forme de surface, ou POS-tag
- Des analyses de cooccurrences et de collocations
- Des concordances contextuelles
- Des statistiques de fréquence

## Workflow du module

```
Fichiers verticaux lemmatisés
         ↓
    Fusion textes
         ↓
    Copie locale
         ↓
  Vérification test
         ↓
    Export serveur
         ↓
    Compilation
         ↓
       Run
         ↓
  Corpus disponible
```

## Étapes détaillées

### 1. Préparation : Fichiers verticaux lemmatisés

**Source** : Sortie du MODULE 6 (PAGEtopage)

**Format attendu** :
- Fichiers `.vertical.txt` nommés selon le titre de l'édition
- Format vertical : un mot par ligne avec annotations
- Structure : `forme<TAB>POS<TAB>lemme`

**Organisation** :
- Tous les fichiers regroupés dans un même dossier
- Nomenclature cohérente pour faciliter la fusion

**Exemple de contenu** :
```
In      R       in
principio       N       principium
erat    V       sum
verbum  N       verbum
```

### 2. Fusion des textes

**Outil** : `PAGEtopage/fusion_vertical.py` (interface CLI moderne)

**Localisation** : Le script de fusion a été déplacé dans le dossier PAGEtopage pour une meilleure organisation du workflow.

**Processus** :
1. Lecture de tous les fichiers `.vertical.txt` du dossier source
2. Concaténation séquentielle des contenus
3. Préservation des métadonnées de séparation entre textes
4. Génération du fichier `Corpus.txt` unique

**Usage** :
```bash
python PAGEtopage/fusion_vertical.py -i /path/to/vertical/files -o Corpus.txt
```

**Sortie** : `Corpus.txt` - fichier vertical unique contenant tous les textes fusionnés

**Caractéristiques** :
- Maintien de la structure verticale
- Séparateurs entre textes pour traçabilité
- Encodage UTF-8
- Interface CLI avec arguments (--input, --output, --extension, --separator)

### 3. Copie dans le projet local

**Action** : Copie manuelle de `Corpus.txt` dans le projet NoSketch-Engine local

**Objectif** : Préparer le fichier pour la vérification sur l'instance de test

**Emplacement** :
- Répertoire du projet NoSketch-Engine local
- Selon la structure attendue par l'instance de test

### 4. Vérification sur instance de test

**Pré-requis** : Instance test NoSketch-Engine opérationnelle

**Objectif** : Valider la viabilité du corpus avant export sur serveur de production

**Vérifications effectuées** :
- ✅ Format vertical correct
- ✅ Encodage UTF-8 valide
- ✅ Structure des annotations conforme
- ✅ Compilation sans erreur
- ✅ Recherches basiques fonctionnelles

**Résultats possibles** :

#### ✅ **Corpus viable** → Passage à l'export serveur
- Toutes les vérifications passées
- Corpus prêt pour la production

#### ❌ **Corpus non viable** → Retour aux données sources
- Erreurs de format détectées
- Encodage incorrect
- Annotations manquantes ou malformées
- **Action** : Retour à l'étape 1 pour correction des données verticales

### 5. Export sur le serveur de production

**Condition** : Corpus validé sur l'instance de test

**Processus** :

#### 5.1 Connexion Shell au serveur
```bash
ssh user@nosketch-server.domain
```

#### 5.2 Transfert via SCP
```bash
scp Corpus.txt user@nosketch-server:/path/to/nosketch/data/
```

**Caractéristiques** :
- Transfert sécurisé via SSH
- Vérification de l'intégrité du fichier transféré
- Droits d'accès appropriés sur le serveur

### 6. Compilation du corpus

**Emplacement** : Sur le serveur NoSketch-Engine

**Commandes** :
```bash
cd /home/debian/NoSketch-Engine-Docker/corpora/cisame/vertical/
make compile
```

**Processus** :
- Indexation du fichier vertical
- Création des structures de données optimisées
- Génération des statistiques de fréquence
- Construction des index de recherche

**Fichiers générés** :
- Index de lemmes
- Index de formes
- Index de POS-tags
- Statistiques de corpus

### 7. Mise en service (Run)

**Action** : Activation du corpus dans l'interface NoSketch-Engine

**Commande** :
```bash
make run
```

**Résultat** : Corpus interrogeable via l'interface web NoSketch-Engine

**Fonctionnalités disponibles** :
- Recherche par lemme
- Recherche par forme de surface
- Recherche par POS-tag
- Concordances (KWIC - Key Word In Context)
- Collocations
- Fréquences
- Analyse de cooccurrences

## Points d'attention

### 🔧 Instance de test obligatoire

Une instance test NoSketch-Engine est **nécessaire** pour valider le corpus avant export en production. Cette étape prévient :
- Les erreurs de compilation sur le serveur
- Les corpus malformés en production
- La perte de temps sur des exports non viables

### 🔄 Boucle de correction

En cas de corpus non viable détecté lors de la vérification :
1. **Ne pas** forcer l'export vers le serveur
2. **Retourner** aux données verticales sources (MODULE 6)
3. **Corriger** les erreurs de format/encodage/annotations
4. **Refusionner** avec `Fusion_txt_NoSketch.py`
5. **Retester** sur l'instance locale

### 📊 Nomenclature des fichiers

Les fichiers verticaux doivent être nommés selon le titre de l'édition :
- Facilite l'identification des sources
- Permet la traçabilité
- Aide à la gestion des mises à jour partielles

### 🔐 Accès serveur

Nécessite :
- Accès SSH au serveur NoSketch-Engine
- Droits d'écriture dans le répertoire de données
- Droits d'exécution pour la compilation

### 💾 Gestion des versions

Stratégie recommandée :
- Conserver une copie locale de chaque `Corpus.txt` exporté
- Versioning avec date : `Corpus_YYYY-MM-DD.txt`
- Documentation des modifications entre versions

## Cas particulier : Décret de Gratien

⚠️ **Le Décret de Gratien ne passe PAS par ce pipeline**

Le Décret de Gratien :
- Possède son propre format `.txt` adapté
- Est déjà présent sur NoSketch-Engine
- Utilise un pipeline spécifique différent du workflow général

## Outils et technologies

### PAGEtopage/fusion_vertical.py
- **Fonction** : Fusion des fichiers verticaux
- **Langage** : Python 3
- **Interface** : CLI avec argparse
- **Entrée** : Dossier contenant fichiers `.vertical.txt`
- **Sortie** : `Corpus.txt` unique
- **Localisation** : `PAGEtopage/fusion_vertical.py`

### NoSketch-Engine
- **Type** : Corpus query system
- **Interface** : Web
- **Fonctionnalités** : Concordances, collocations, statistiques
- **Format** : Vertical (un token par ligne)

### SCP (Secure Copy Protocol)
- **Fonction** : Transfert sécurisé de fichiers
- **Protocole** : SSH
- **Usage** : Export du corpus vers le serveur

### Shell SSH
- **Fonction** : Connexion distante au serveur
- **Usage** : Compilation et mise en service du corpus

## Flux de données

```
MODULE 6 (PAGEtopage)
        ↓
Fichiers .vertical.txt
(texte_edition_1.vertical.txt,
 texte_edition_2.vertical.txt, ...)
        ↓
Fusion_txt_NoSketch.py
        ↓
Corpus.txt (local)
        ↓
Instance Test NoSketch
        ↓ (si viable)
SCP → Serveur Production
        ↓
Compilation
        ↓
Corpus interrogeable
```

## Relation avec les autres modules

### En amont : MODULE 6 (PAGEtopage)
- **Fournit** : Fichiers verticaux lemmatisés
- **Format** : `.vertical.txt` avec annotations linguistiques
- **Contenu** : Forme, POS, Lemme pour chaque token

### En parallèle : MODULE Données Textuelles
- **Rôle différent** : Diffusion des textes bruts
- **Pas de lien direct** : Workflows indépendants
- **Destinations différentes** : NoSketch vs Nakala/Seafile

### En parallèle : MODULE Métadonnées
- **Consultation** : Métadonnées Heurist pour contexte
- **Pas d'intégration automatique** : Métadonnées non incluses dans corpus NoSketch
- **Usage** : Référence pour l'interprétation des résultats

## Exemple de commandes

### Fusion des fichiers verticaux
```bash
python PAGEtopage/fusion_vertical.py -i /path/to/vertical/files -o Corpus.txt

# Ou avec extension personnalisée
python PAGEtopage/fusion_vertical.py -i /path/to/output -o Corpus.txt -e .vertical.txt
```

### Copie vers instance de test
```bash
cp Corpus.txt /path/to/nosketch-test/data/
```

### Vérification locale (exemple)
```bash
# Dépend de la configuration de l'instance test
cd /path/to/nosketch-test
./test_corpus.sh Corpus.txt
```

### Export vers serveur
```bash
scp Corpus.txt user@nosketch-prod.server:/data/nosketch/corpora/
```

### Connexion et compilation sur serveur
```bash
ssh debian@fip-185-155-93-80.iaas.unistra.fr
cd /home/debian/NoSketch-Engine-Docker/corpora/cisame/vertical/
make compile
make run
```

## Métriques et statistiques

Une fois le corpus compilé et actif, NoSketch-Engine génère automatiquement :

- **Nombre total de tokens** : Toutes les formes du corpus
- **Nombre de lemmes uniques** : Vocabulaire lemmatisé
- **Nombre de formes uniques** : Vocabulaire de surface
- **Distribution POS** : Répartition par catégorie grammaticale
- **Fréquences** : Par lemme, forme, POS

Ces statistiques sont accessibles via l'interface web NoSketch-Engine.

## Maintenance et mises à jour

### Ajout de nouveaux textes
1. Générer les nouveaux fichiers `.vertical.txt` via MODULE 6
2. Ajouter au dossier source
3. Refusionner avec `Fusion_txt_NoSketch.py`
4. Vérifier sur instance test
5. Exporter vers production
6. Recompiler le corpus

### Correction d'erreurs
1. Identifier le fichier source problématique
2. Corriger dans le workflow MODULE 6
3. Régénérer le fichier `.vertical.txt`
4. Refusionner
5. Tester et réexporter

### Mise à jour de lemmatisation
1. Retraiter les textes sources via MODULE 6 avec TreeTagger mis à jour
2. Régénérer tous les fichiers `.vertical.txt`
3. Refusionner le corpus complet
4. Tester et réexporter

## 📚 Fichiers et ressources

**Schémas** :
- `flowchart-module7-nosketch.mmd` : Schéma du pipeline NoSketch-Engine

**Scripts** :
- `PAGEtopage/fusion_vertical.py` : Fusion des fichiers verticaux

**Documentation** :
- Documentation NoSketch-Engine : https://www.sketchengine.eu/

---

## Conclusion

Le module NoSketch-Engine finalise le pipeline CiSaMe en rendant les corpus enrichis accessibles et interrogeables. La vérification sur instance de test est cruciale pour garantir la qualité du corpus en production.

Le script de fusion `PAGEtopage/fusion_vertical.py` a été déplacé dans le dossier PAGEtopage pour une meilleure organisation logique : PAGEtopage génère les fichiers `.vertical.txt`, puis le script de fusion les prépare pour NoSketch-Engine.

La boucle de retour en cas de corpus non viable permet une correction à la source, maintenant ainsi l'intégrité de l'ensemble du pipeline.
