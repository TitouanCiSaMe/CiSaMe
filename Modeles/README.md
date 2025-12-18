# Modèles Kraken (.mlmodel)

Bibliothèque de modèles pré-entraînés pour la segmentation et transcription automatique (MODULE 4 - eScriptorium).

## Structure

```
Modeles/
├── MODELES_SEGMENTATION/
│   ├── SEGMENTATION_EDITION/      # Détection lignes/régions éditions imprimées
│   └── SEGMENTATION_MANUSCRIT/    # Détection lignes/régions manuscrits
└── MODELES_TRANSCRIPTION/
    ├── TRANSCRIPTION_EDITION/     # HTR/OCR éditions imprimées
    └── TRANSCRIPTION_MANUSCRIT/   # HTR manuscrits médiévaux
```

## Utilisation

### Import dans eScriptorium
- Importer le modèle correspondant au type de document
- Appliquer automatiquement sur les pages

## Types de documents

### Éditions (imprimées)
- Texte régulier, meilleurs résultats (CER < 2%)
- Modèles : EXPOSANT, EDITION_GENERALE, CATMUS_PRINT_FONDUE_LARGE

### Manuscrits (médiévaux)
- Écriture manuscrite variable (CER 4-8%)
- Modèles spécifiques : ADMONT_7, ALCUINUS, AVRANCHE, BAMBERG_126/127, PARIS_18108, SUMMA_SICARDI, TRIDIS_V2

## Formats de mise en page

| Modèle | Layout |
|--------|--------|
| `MANUSCRIT_UNE_COLLONE.mlmodel` | 1 colonne |
| `MANUSCRIT_DEUX_COLLONE.mlmodel` | 2 colonnes |
| `ADMONT_7_DOUBLE_COLONNE.mlmodel` | 2 colonnes (Admont 7) |

## Ressources

- **Kraken** : https://kraken.re/
- **eScriptorium** : https://escriptorium.readthedocs.io/
- **HTR-United** : https://htr-united.github.io/ (modèles publics)
- **Documentation MODULE 4** : `Modules_projet/Module_4/MODULE4_DOCUMENTATION.md`
