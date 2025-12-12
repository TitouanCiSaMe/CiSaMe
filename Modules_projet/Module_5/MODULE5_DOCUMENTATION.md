# MODULE 5 - Nettoyage Post-eScriptorium

**Documentation du nettoyage des fichiers XML PAGE avec Oxygène**

---

## Vue d'ensemble

Le MODULE 5 assure le nettoyage et la correction des fichiers XML PAGE produits par eScriptorium avant leur enrichissement linguistique.

**Entrée** : Fichiers XML PAGE depuis eScriptorium (MODULE 4)
**Sortie** : Fichiers XML PAGE nettoyés, prêts pour PAGEtopage
**Outil principal** : Oxygène XML Editor

---

## Oxygène XML Editor

### Installation

**Site officiel** : https://www.oxygenxml.com/

**Licence d'essai (30 jours)** : https://www.oxygenxml.com/xml_editor/register.html?p=editor

**Tutoriels** : Disponibles sur le site d'Oxygène et sur YouTube

### Pourquoi Oxygène ?

- Recherche XPath puissante
- Support des expressions régulières
- Remplacement dans plusieurs fichiers
- Validation XML intégrée
- Interface intuitive

---

## Workflow de nettoyage

### Étapes générales

```
1. Import XML PAGE depuis Seafile
       ↓
2. Ouvrir avec Oxygène
       ↓
3. Identifier le type de layout (1, 2 ou 4 régions)
       ↓
4. Appliquer XPath + Regex selon le layout
       ↓
5. Vérification (pagination, erreurs OCR)
       ↓
6. Corrections manuelles si nécessaire
       ↓
7. Export vers Seafile
       ↓
8. Vers MODULE 6 (PAGEtopage)
```

### Types de layouts

| Layout | Description | XPath |
|--------|-------------|-------|
| **Simple** | 1 région Main par page | `//TextRegion[contains(@custom, 'type:MainZone')]` |
| **Deux colonnes** | 2 régions Main par page | `column#1` et `column#2` |
| **Quatre colonnes** | 4 régions Main par page | `column#1` à `column#4` |

---

## Procédure détaillée avec Oxygène

### Étape 1 : Ouvrir le fichier

1. Lancer Oxygène XML Editor
2. Fichier → Ouvrir → Sélectionner le fichier XML PAGE
3. Le fichier s'affiche en mode texte/grille

### Étape 2 : Accéder à la recherche

1. Menu **Rechercher** → **Rechercher/Remplacer** (ou Ctrl+H)
2. Ou utiliser l'onglet **Rechercher** dans le panneau inférieur

### Étape 3 : Configurer la recherche

**Paramètres importants** :

1. **Cocher "Expression régulière"** : Active le mode regex
2. **Cocher "Chemin indiqué"** : Limite la recherche au XPath spécifié
3. **Renseigner le XPath** selon le layout du document

### Étape 4 : Appliquer les regex

Exécuter les regex une par une :
1. Saisir la regex dans "Texte à rechercher"
2. Saisir le remplacement dans "Remplacer par"
3. Cliquer sur "Remplacer tout"
4. Vérifier le nombre de remplacements

---

## XPath par type de layout

### Layout simple (1 région Main)

```xpath
//TextRegion[contains(@custom, 'type:MainZone')]//TextLine//Unicode/text()
```

### Layout 2 colonnes

**Colonne 1** :
```xpath
//TextRegion[contains(@custom, 'type:MainZone:column#1')]//TextLine//Unicode/text()
```

**Colonne 2** :
```xpath
//TextRegion[contains(@custom, 'type:MainZone:column#2')]//TextLine//Unicode/text()
```

### Layout 4 colonnes

Appliquer séquentiellement pour `column#1`, `column#2`, `column#3`, `column#4`.

---

## Expressions régulières courantes

### Nettoyage des espaces

| Description | Rechercher | Remplacer |
|-------------|------------|-----------|
| Doubles espaces | `  +` (2 espaces+) | ` ` (1 espace) |
| Espaces en début de ligne | `^\s+` | `` (vide) |
| Espaces en fin de ligne | `\s+$` | `` (vide) |

### Nettoyage de la ponctuation

| Description | Rechercher | Remplacer |
|-------------|------------|-----------|
| Espace avant ponctuation | ` ([.,;:!?])` | `$1` |
| Pas d'espace après ponctuation | `([.,;:!?])([A-Za-z])` | `$1 $2` |

### Caractères spéciaux

| Description | Rechercher | Remplacer |
|-------------|------------|-----------|
| Caractères indésirables | `[!?''` `` `–—…\[\]{}«»/\\&*@#§¶†‡°^~¨]` | `` (vide) |
| Chiffres isolés | `^\d+$` | `` (vide) |

### Références de folios

| Description | Rechercher | Remplacer |
|-------------|------------|-----------|
| Références folio type 1 | `f[°'] [A-Z\d{1,2}][a-z]{2}` | `` (vide) |
| Références folio type 2 | `f[°'] [A-Z0-9][a-z]{2}` | `` (vide) |

### Suppressions spécifiques

| Description | Rechercher | Remplacer |
|-------------|------------|-----------|
| Contenu entre \| et ] | `\|[^\]]*\]` | `` (vide) |

---

## Validation des regex

### Outils en ligne recommandés

- **Regex101** : https://regex101.com/ (recommandé, avec explications)
- **RegExr** : https://regexr.com/
- **Debuggex** : https://www.debuggex.com/ (visualisation)

### Bonnes pratiques

1. **Tester avant d'appliquer** : Utiliser "Rechercher" avant "Remplacer tout"
2. **Sauvegarder une copie** : Avant d'appliquer des regex massives
3. **Procéder par étapes** : Une regex à la fois
4. **Vérifier les résultats** : Après chaque remplacement

---

## Vérification post-nettoyage

### Points à contrôler

1. **Pagination** : Vérifier que toutes les pages sont présentes
2. **Lignes vides** : Détecter les pages sans texte (souvent fins de chapitre)
3. **Erreurs OCR résiduelles** : Caractères mal reconnus
4. **Cohérence** : Structure globale du document

### Cas problématiques courants

| Problème | Cause | Solution |
|----------|-------|----------|
| Pages sans lignes MainZone | Fin de chapitre, page de titre | Normal, ignorer |
| Texte mal segmenté | Mauvaise segmentation eScriptorium | Retour MODULE 4 |
| Caractères aberrants | Erreur OCR | Correction manuelle |

---

## Corrections manuelles

### Quand corriger manuellement ?

- Erreurs OCR persistantes
- Pages sans lignes détectées (bugs de segmentation)
- Caractères spéciaux non gérés par regex

### Procédure

1. Identifier les erreurs dans Oxygène
2. Éditer directement le texte dans le fichier XML
3. Sauvegarder
4. Relancer la vérification

---

## Format de sortie

### Nomenclature des fichiers

**Format recommandé** : `NOMEDITION_ID.xml`

**Exemples** :
- `Friedberg_Edi-1.xml`
- `Laspeyres_Edi-7.xml`

### Structure du fichier XML PAGE

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15">
  <Page imageFilename="page001.jpg" imageWidth="2000" imageHeight="3000">
    <TextRegion custom="type:MainZone">
      <TextLine>
        <Coords points="..."/>
        <TextEquiv>
          <Unicode>Texte transcrit nettoyé</Unicode>
        </TextEquiv>
      </TextLine>
    </TextRegion>
  </Page>
</PcGts>
```

---

## Temps de traitement

**Estimation** : ~20 minutes par oeuvre

**Détail** :
- Configuration XPath : 2-3 min
- Application des regex : 5-10 min
- Vérification : 5-10 min
- Corrections manuelles : Variable

---

## Lien avec les autres modules

**En amont** : MODULE 4 (eScriptorium)
- Fichiers XML PAGE bruts

**En aval** : MODULE 6 (PAGEtopage)
- Fichiers XML PAGE nettoyés, prêts pour l'enrichissement linguistique

---

## Fichiers associés

```
Modules_projet/
└── Module_5/
    ├── flowchart-module5.mmd          # Schéma du workflow
    └── MODULE5_DOCUMENTATION.md       # Cette documentation
```

---

## Ressources

- **Oxygène XML Editor** : https://www.oxygenxml.com/
- **Licence d'essai** : https://www.oxygenxml.com/xml_editor/register.html?p=editor
- **Regex101** : https://regex101.com/
- **Documentation XPath** : https://www.w3schools.com/xml/xpath_intro.asp

---

## Statut

**MODULE 5** : Opérationnel

- Workflow défini
- Regex documentées
- Procédure Oxygène décrite

---

*Dernière mise à jour : Décembre 2025*
