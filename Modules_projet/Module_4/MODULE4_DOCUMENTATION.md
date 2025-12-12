# MODULE 4 - Traitement eScriptorium

**Documentation du workflow de segmentation et transcription HTR/OCR**

---

## Vue d'ensemble

Le MODULE 4 gère le traitement des images de manuscrits et éditions via **eScriptorium** pour produire des transcriptions au format XML PAGE.

**Entrée** : Images depuis Seafile (MODULE 1-3)
**Sortie** : Fichiers XML PAGE avec transcriptions
**Outils** : eScriptorium, Kraken, HPC Unistra

---

## Tutoriels eScriptorium

### Documentation officielle

**En anglais** : https://escriptorium.readthedocs.io/en/latest/

**En français** : https://lectaurep.hypotheses.org/documentation/prendre-en-main-escriptorium

Ces tutoriels couvrent :
- Création de projet
- Import d'images
- Segmentation manuelle et automatique
- Transcription manuelle et automatique
- Export des données

### Installation / Accès

**Option 1 : Installation locale via Docker**
- Suivre le guide officiel : https://gitlab.com/scripta/escriptorium
- Nécessite Docker installé sur la machine

**Option 2 : Instance en ligne**
- Demander un compte sur une instance existante
- Instances disponibles :
  - INRIA
  - Universités partenaires
  - Instances de recherche

---

## Workflow général

```
Images (Seafile)
      ↓
Import dans eScriptorium
      ↓
┌─────────────────────────────┐
│     SEGMENTATION            │
├─────────────────────────────┤
│ 1. Segmentation manuelle    │
│    (50-100 pages)           │
│         ↓                   │
│ 2. Entraînement modèle      │
│    (HPC si besoin)          │
│         ↓                   │
│ 3. Application automatique  │
│         ↓                   │
│ 4. Validation/corrections   │
└─────────────────────────────┘
      ↓
┌─────────────────────────────┐
│     TRANSCRIPTION           │
├─────────────────────────────┤
│ 1. Transcription manuelle   │
│    (100-200 lignes)         │
│         ↓                   │
│ 2. Entraînement modèle      │
│    (HPC)                    │
│         ↓                   │
│ 3. Application automatique  │
│         ↓                   │
│ 4. Validation/corrections   │
└─────────────────────────────┘
      ↓
Export XML PAGE
      ↓
Vers MODULE 5 (Nettoyage)
```

---

## Types de documents

### Éditions imprimées

**Caractéristiques** :
- Texte régulier et imprimé
- Plus facile à traiter
- Meilleurs résultats

**CER cible** : 0.1-2% (Character Error Rate)

### Manuscrits

**Caractéristiques** :
- Écriture manuscrite variable
- Plus complexe à traiter
- Nécessite plus de données d'entraînement

**CER cible** : 4-8%

---

## Entraînement sur HPC

### Prérequis

- Compte HPC Unistra
- Données de vérité de terrain (Ground Truth)
- Modèle de base pour fine-tuning

### Connexion au HPC

```bash
ssh votre_login@hpc-login.u-strasbg.fr
# ou
ssh votre_login@hpc-glogin.u-strasbg.fr
```

### Structure des répertoires sur le HPC

```
~/
├── Ground_Truth/           # Vérité de terrain par projet
│   └── Projet_A/
│       ├── page001.xml
│       └── page001.png
├── GT_compile/             # Datasets compilés (.arrow)
├── Model_de_base/          # Modèles pré-entraînés
├── Scripts/                # Scripts d'entraînement
└── Repertoire_model_finetune/  # Modèles fine-tunés
```

### Création de l'arborescence

```bash
mkdir -p Ground_Truth
mkdir -p GT_compile
mkdir -p Model_de_base
mkdir -p Scripts
mkdir -p Repertoire_model_finetune
```

### Transfert des données (depuis Mac/Linux)

**Vérité de terrain** :
```bash
scp -r ~/chemin/local/Projet_A votre_login@hpc-login.u-strasbg.fr:~/Ground_Truth/
```

**Modèles de base** :
```bash
scp modele.mlmodel votre_login@hpc-login.u-strasbg.fr:~/Model_de_base/
```

**Scripts** :
```bash
scp *.sh votre_login@hpc-login.u-strasbg.fr:~/Scripts/
```

---

## Scripts de Fine-tuning

### Fine-tuning de Transcription

**Fichier** : `Fine_tuning_transcription.sh` (voir Documentation/)

```bash
#! /bin/sh

#SBATCH -p publicgpu          # Partition GPU publique
#SBATCH -N 1                  # 1 noeud
#SBATCH -t 4:00:00            # Temps maximum : 4 heures
#SBATCH --gres=gpu:1          # 1 GPU
#SBATCH --constraint=gputc    # GPU tensor core
#SBATCH --mail-type=END       # Email à la fin
#SBATCH --mail-user=votre.email@unistra.fr

module load kraken

# Compilation + Entraînement
ketos compile --random-split 0.8 0.1 0.1 --workers 64 -f xml \
  -o GT_compile/NOM.arrow Ground_Truth/NOM_PROJET/*.xml

ketos -v train --optimizer Adam --augment --workers 64 -d cuda:0 \
  --min-epochs 20 -w 0 --quit dumb --pad 24 \
  -o Repertoire_model_finetune/NOM_PROJET/NOM_PROJET \
  -s '[1,128,0,1 Cr4,16,32 Do0.1,2 Mp2,2 Cr4,16,32 Do0.1,2 Mp2,2 Cr3,8,64 Do0.1,2 Mp2,2 Cr3,8,64 Do0.1,2 S1(1x0)1,3 Lbx256 Do0.3,2 Lbx256 Do0.3,2 Lbx256 Do0.3]' \
  -f binary -r 0.0001 --resize new \
  -i Model_de_base/NOM_MODELE_BASE.mlmodel \
  GT_compile/NOM.arrow
```

**Paramètres importants** :
- `--random-split 0.8 0.1 0.1` : 80% train, 10% validation, 10% test
- `--min-epochs 20` : Minimum 20 époques
- `-r 0.0001` : Learning rate
- `-i` : Modèle de base pour fine-tuning

### Fine-tuning de Segmentation

**Fichier** : `Fine_tuning_segmentation.sh` (voir Documentation/)

```bash
#! /bin/sh

#SBATCH -p publicgpu
#SBATCH -N 1
#SBATCH -t 4:00:00
#SBATCH --gres=gpu:1
#SBATCH --constraint=gputc
#SBATCH --mail-type=END
#SBATCH --mail-user=votre.email@unistra.fr

module load kraken

ketos segtrain --optimizer Adam --augment --workers 64 -d cuda:0 \
  -f page --min-epochs 60 -w 0 --quit dumb 20 -N 2000 --resize new \
  -i Model_de_base/NOM_MODELE_BASE.mlmodel \
  -o Repertoire_model_finetune/NOM_PROJET/NOM_PROJET \
  -s '[1,1200,0,3 Cr7,7,64,2,2 Gn32 Cr3,3,128,2,2 Gn32 Cr3,3,128 Gn32 Cr3,3,256 Gn32]' \
  -r 0.0001 Ground_Truth/NOM_PROJET/*.xml
```

**Note** : La segmentation n'a PAS besoin de compilation (.arrow), elle utilise directement les XML.

---

## Soumission et suivi des jobs

### Soumettre un job

```bash
cd ~/Scripts
sbatch finetune_transcription.sh
# Réponse : Submitted batch job 123456
```

### Suivre les jobs

```bash
# État de vos jobs
squeue -u votre_login

# Détails d'un job
scontrol show job 123456

# Logs en temps réel
tail -f slurm-123456.out

# Historique
sacct -u votre_login
```

### Annuler un job

```bash
scancel 123456
# ou tous vos jobs
scancel -u votre_login
```

---

## Récupération des modèles

### Localiser le modèle

```bash
ssh votre_login@hpc-login.u-strasbg.fr
cd ~/Repertoire_model_finetune/NOM_PROJET
ls -lh
# Chercher : model_best.mlmodel
```

### Télécharger (depuis Mac/Linux)

```bash
scp votre_login@hpc-login.u-strasbg.fr:~/Repertoire_model_finetune/NOM_PROJET/model_best.mlmodel ~/local/
```

### Nettoyage HPC

Après récupération des modèles :
```bash
# Supprimer les fichiers compilés
rm ~/GT_compile/*.arrow

# Supprimer les logs
rm ~/slurm-*.out

# Vérifier quota
diskquota
```

---

## Réutilisation des modèles

### Principe

Si un manuscrit similaire a déjà été traité, le modèle existant peut être réutilisé directement ou servir de base pour un nouveau fine-tuning.

**Avantages** :
- Gain de temps considérable
- Pas besoin de refaire la vérité de terrain
- Résultats souvent meilleurs

### Modèles de base recommandés

Les modèles de base pour fine-tuning sont stockés dans `Model_de_base/` sur le HPC.

Sources de modèles pré-entraînés :
- Zenodo (https://zenodo.org)
- HTR-United (https://htr-united.github.io/)
- Partage entre projets

---

## Export depuis eScriptorium

### Format XML PAGE

**Sortie standard** : Fichiers XML PAGE contenant :
- Coordonnées des régions
- Coordonnées des lignes
- Texte transcrit
- Métadonnées

### Procédure d'export

1. Dans eScriptorium, sélectionner le document
2. Aller dans "Export"
3. Choisir le format "PAGE XML"
4. Télécharger l'archive
5. Extraire et uploader sur Seafile

---

## Métriques de qualité

### CER (Character Error Rate)

| Type | CER acceptable | CER bon | CER excellent |
|------|----------------|---------|---------------|
| Éditions | < 5% | < 2% | < 1% |
| Manuscrits | < 10% | < 8% | < 5% |

### Interprétation

- **< 2%** : Excellent, peu de corrections nécessaires
- **2-5%** : Bon, corrections mineures
- **5-10%** : Acceptable, corrections modérées
- **> 10%** : Nécessite retraitement ou plus de données

---

## Lien avec les autres modules

**En amont** :
- MODULE 1-2 : Images de manuscrits
- MODULE 3 : Images d'éditions

**En aval** :
- MODULE 5 : Nettoyage post-eScriptorium

---

## Fichiers associés

```
/
├── Documentation/
│   ├── Fine_tuning_segmentation.sh    # Script HPC segmentation
│   ├── Fine_tuning_transcription.sh   # Script HPC transcription
│   └── Guide_Kraken_HTR_Mac.txt       # Guide complet HPC
└── Modules_projet/
    └── Module_4/
        ├── flowchart-module4.mmd       # Schéma du workflow
        └── MODULE4_DOCUMENTATION.md    # Cette documentation
```

---

## Ressources

- **Documentation Kraken** : https://kraken.re/main/index.html
- **eScriptorium (EN)** : https://escriptorium.readthedocs.io/en/latest/
- **eScriptorium (FR)** : https://lectaurep.hypotheses.org/documentation/prendre-en-main-escriptorium
- **Guide HPC complet** : `Documentation/Guide_Kraken_HTR_Mac.txt`

---

## Statut

**MODULE 4** : Opérationnel

- Workflow eScriptorium : Documenté
- Scripts HPC : Disponibles
- Guide complet : Disponible

---

*Dernière mise à jour : Décembre 2025*
