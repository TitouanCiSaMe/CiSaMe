# 📦 MODULE - Données Textuelles : Gestion de la Diffusion

**Documentation du module de gestion de la diffusion finale des corpus**

---

## 📋 Vue d'ensemble

Ce module gère la **diffusion finale** des données textuelles enrichies, en fonction des droits de diffusion et de la présence ou non des images.

**Objectif** : Décider où publier/stocker les corpus finaux
**Critères** : Droits (libre/restreint) + Présence d'images
**Destinations** : Nakala (plateforme ouverte) ou Seafile (stockage privé)

---

## 🔄 Logique de décision

### **2 branches parallèles**

Le module traite deux cas de figure en parallèle :

1. **Avec images** : Corpus + images des manuscrits/éditions
2. **Sans images** : Corpus textuel uniquement

Pour chaque cas, décision selon les **droits de diffusion** :
- ✅ **Libre de droit** → Export sur **Nakala**
- ❌ **Pas libre de droit** → Reste sur **Seafile**

---

## 📊 Workflow détaillé

```
Données textuelles
    ↓
    ├─→ AVEC IMAGES
    │       ↓
    │   Libre de droit ?
    │       ├─→ OUI → Nakala (via algo Hécate + connecteur)
    │       └─→ NON → Seafile (stockage privé)
    │
    └─→ SANS IMAGES
            ↓
        Libre de droit ?
            ├─→ OUI → Nakala (via algo Hécate + connecteur)
            └─→ NON → Seafile (stockage privé)
```

---

## 📁 Contenu des packages

### **Package "Avec images"**

Contient :
- `Conversion.log` : Log du traitement
- `images_mapping.txt` : Correspondance texte ↔ images
- `pages_index.json` : Index des pages avec métadonnées
- **Chaque page** : Fichiers texte individuels
- `texte_complet.txt` : Fichier unique avec tout le texte
- **Images de chaque page** : Fichiers image (TIF/JPG)

**Taille** : Variable selon corpus (plusieurs GB possibles)

### **Package "Sans images"**

Contient :
- `Conversion.log` : Log du traitement
- `images_mapping.txt` : Correspondance (sans les images réelles)
- `pages_index.json` : Index des pages avec métadonnées
- **Chaque page** : Fichiers texte individuels
- `texte_complet.txt` : Fichier unique avec tout le texte

**Taille** : Beaucoup plus légère (quelques MB)

---

## 🌐 Nakala : Plateforme de diffusion ouverte

### Qu'est-ce que Nakala ?

**Nakala** est un espace de stockage et de diffusion pour la recherche scientifique.

**Caractéristiques** :
- Plateforme institutionnelle française
- Dédiée aux données de recherche
- Accès ouvert (open access)
- Pérenne et référencée
- DOI attribués aux corpus

**Usage dans le projet** :
- Publication des corpus **libres de droit**
- Visibilité internationale
- Respect des principes FAIR (Findable, Accessible, Interoperable, Reusable)
- Citation académique facilitée

### Export vers Nakala

**Outil** : Algo Hécate + connecteur Nakala

**Processus** :
1. Préparation du package (textes + images si applicable)
2. Génération métadonnées Nakala-compatibles
3. **Algo Hécate** : Script d'export automatisé
4. **Connecteur Nakala** : Upload vers la plateforme
5. Attribution d'un DOI
6. Publication en ligne

**Métadonnées exportées** :
- Titre du corpus
- Auteur(s)
- Date
- Type de droit
- Langue
- Description
- Institution (Université de Strasbourg / ARCHE)

---

## 💾 Seafile : Stockage privé

### Qu'est-ce que Seafile ?

**Seafile** est le cloud universitaire de l'Université de Strasbourg.

**Caractéristiques** :
- Stockage sécurisé
- Accès restreint (équipe projet)
- Sauvegarde automatique
- Synchronisation
- Partage contrôlé

**Usage dans le projet** :
- Stockage des corpus **pas libres de droit**
- Accès interne uniquement
- Travail collaboratif de l'équipe
- Conservation avant publication éventuelle

### Stockage sur Seafile

**Organisation** :
```
Seafile/
└── CiSaMe/
    └── Corpus/
        ├── Avec_images/
        │   ├── Pas_libre/
        │   │   ├── [Manuscrit_1]/
        │   │   └── [Manuscrit_2]/
        │   └── Libre/  (avant export Nakala)
        │
        └── Sans_images/
            ├── Pas_libre/
            └── Libre/  (avant export Nakala)
```

---

## ⚖️ Gestion des droits

### Détermination du statut "Libre de droit"

**Critères** :
1. **Manuscrits médiévaux** : Toujours libres (domaine public)
2. **Éditions anciennes** (avant 1900) : Généralement libres
3. **Éditions récentes** (après 1900) :
   - Libre si : +70 ans après décès auteur/éditeur
   - Pas libre si : droits actifs

**Référence** : Module 3 (Récupération d'éditions) documente déjà la catégorisation :
- 15e-début 20e siècle → Libre de droit (~60%)
- Jamais officiellement sorties → Secret (~10%)
- 20e-21e siècle → Très restreint (~30%)

### Cas particuliers

**"Secret"** : Éditions jamais officiellement sorties
- Thèses non publiées
- Travaux inédits
- Pas de diffusion publique autorisée
- → Stockage Seafile uniquement

**"Très restreint"** : Droits d'auteur actifs
- Usage recherche uniquement
- Convention nécessaire
- → Stockage Seafile uniquement

---

## ✅ Critères de décision

### Checklist avant diffusion

**Pour chaque corpus** :

1. ☐ Vérifier statut droits dans Heurist
2. ☐ Confirmer présence/absence images
3. ☐ Vérifier complétude du package
4. ☐ Si libre → Préparer métadonnées Nakala
5. ☐ Lancer export (Hécate ou Seafile)
6. ☐ Vérifier succès de l'opération
7. ☐ Logger dans base de suivi

---

## 📝 Workflow complet

```
1. Corpus finalisé (Module 6 ou Décret)
        ↓
2. Consultation statut droits (Heurist)
        ↓
3. Détermination branche (Avec/Sans images)
        ↓
4. SI Libre de droit :
   a. Préparation package
   b. Génération métadonnées
   c. Algo Hécate → Upload Nakala
   d. Vérification DOI attribué
   e. Publication
        ↓
5. SI Pas libre :
   a. Organisation dossier Seafile
   b. Upload sur cloud privé
   c. Documentation accès restreint
        ↓
6. Logging et archivage
```

---

## 🔒 Sécurité et confidentialité

### Données libres sur Nakala

**Accès** : Public mondial
**Licence** : À définir (Creative Commons recommandé)
**Citation** : Via DOI
**Durabilité** : Garantie par Nakala

### Données restreintes sur Seafile

**Accès** : Équipe CiSaMe uniquement
**Authentification** : Comptes universitaires
**Sauvegarde** : Automatique quotidienne
**Partage** : Contrôlé (liens temporaires possibles)

---

## 📊 Schéma récapitulatif

```
                    Données textuelles
                           ↓
        ┌─────────────────┴─────────────────┐
        ↓                                    ↓
    AVEC IMAGES                         SANS IMAGES
        ↓                                    ↓
    Libre ?                             Libre ?
    ↓     ↓                             ↓     ↓
   OUI   NON                           OUI   NON
    ↓     ↓                             ↓     ↓
  Nakala Seafile                      Nakala Seafile
  (DOI)  (Privé)                      (DOI)  (Privé)
```

---

## 📚 Fichiers et ressources

**Schémas** :
- `Shema_module_projet/module_donnees_textuelles.mermaid`

**Scripts** :
- `algo_hecate.py` : Export vers Nakala
- Connecteur Nakala : API REST

**Documentation Nakala** :
- Site officiel : https://www.nakala.fr/
- API documentation : https://api.nakala.fr/doc

---

## ✅ État actuel

**MODULE Données Textuelles** : ✅ **Opérationnel**

- Logique de décision claire : ✅
- Algo Hécate fonctionnel : ✅
- Connecteur Nakala : ✅
- Organisation Seafile : ✅

**Prêt pour diffusion** des corpus finalisés.

---

## 🎯 Prochaines étapes

1. Finalisation des premiers corpus
2. Tests d'export Nakala
3. Attribution DOI
4. Communication publications
5. Suivi citations académiques
