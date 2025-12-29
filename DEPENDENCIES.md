# Documentation des Dépendances - CiSaMe

Ce document détaille toutes les dépendances du projet CiSaMe (Circulation des Savoirs Médiévaux).

---

## 🐍 Prérequis Système

### Python
- **Version minimale:** Python 3.10
- **Version recommandée:** Python 3.11+
- **Vérification:** `python3 --version`

### Git
- **Requis pour:** Installation de PyCollatinus
- **Vérification:** `git --version`

---

## 📦 Installation Standard

### 1. Dépendances principales

```bash
pip install -r requirements.txt
```

**Packages installés:**
- `python-docx==1.2.0` - Génération de documents Word
- `lxml==6.0.2` - Parsing XML (dépendance de python-docx)
- `unidecode==1.4.0` - Translittération et nettoyage de texte
- `pyyaml==6.0.3` - Lecture fichiers de configuration YAML
- `treetaggerwrapper==2.3` - Interface Python pour TreeTagger

### 2. Dépendances de développement (optionnel)

```bash
pip install -r requirements-dev.txt
```

**Packages installés:**
- `pytest==9.0.2` - Framework de tests
- `pytest-cov==6.0.0` - Couverture de code
- `black==25.1.0` - Formatage automatique
- `flake8==8.0.0` - Linting et détection d'erreurs
- `mypy==1.15.0` - Vérification de types statiques
- `pip-audit==2.10.0` - Audit de sécurité des dépendances

---

## 🔧 Dépendances Externes (Non-pip)

### PyCollatinus - Lemmatisation Latin Classique

**Pourquoi non-pip?** Le package PyPI `collatinus` est cassé/obsolète.

**Installation manuelle:**

```bash
# 1. Cloner le dépôt GitHub
cd /chemin/vers/votre/workspace
git clone https://github.com/PonteIneptique/collatinus-python.git

# 2. Installer le package en mode développement
cd collatinus-python
pip install -e .

# 3. Vérifier l'installation
python3 -c "from pycollatinus import Lemmatiseur; print('PyCollatinus OK')"
```

**Utilisation dans le projet:**
- Analyseur latin: `latin_analyzer/src/latin_analyzer_v2.py:34`
- Capacités: ~500,000 formes latines classiques

**Alternative si problème:**
Voir `latin_analyzer/INSTALL.md` pour instructions détaillées.

---

### TreeTagger - Lemmatisation Automatique

**Installation:** ✅ **AUTOMATIQUE**

TreeTagger est téléchargé et configuré automatiquement lors du premier lancement de PAGEtopage grâce à `treetaggerwrapper`.

**Processus automatique:**
1. Téléchargement binaires TreeTagger (CIS München)
2. Installation paramètres de langue (Latin)
3. Configuration dans `~/.treetagger/`

**Emplacement:** `~/.treetagger/` ou `/opt/treetagger/`

**Vérification:**
```bash
python3 -c "import treetaggerwrapper; print('TreeTagger OK')"
```

**Configuration manuelle (si nécessaire):**
Voir `PAGEtopage/step2_enrich/treetagger_installer.py`

---

## 🎯 Utilisation par Module

### Module: latin_analyzer

**Dépendances requises:**
```txt
python-docx==1.2.0
lxml==6.0.2
unidecode==1.4.0
PyCollatinus (manuel)
```

**Installation:**
```bash
pip install python-docx==1.2.0 lxml==6.0.2 unidecode==1.4.0
# + PyCollatinus (voir ci-dessus)
```

---

### Module: PAGEtopage

**Dépendances requises:**
```txt
pyyaml==6.0.3
treetaggerwrapper==2.3
```

**Installation:**
```bash
pip install pyyaml==6.0.3 treetaggerwrapper==2.3
```

**Note:** TreeTagger s'installe automatiquement au premier lancement.

---

### Module: Tests

**Dépendances requises:**
```txt
pytest==9.0.2
pytest-cov==6.0.0 (optionnel, couverture)
```

**Installation:**
```bash
pip install pytest==9.0.2
```

**Lancement tests:**
```bash
pytest PAGEtopage/tests/
pytest latin_analyzer/tests/
```

---

## 🔒 Sécurité et Audits

### Vérification des vulnérabilités

```bash
# Installer pip-audit
pip install pip-audit

# Auditer les dépendances
pip-audit -r requirements.txt

# Format JSON pour intégration CI/CD
pip-audit -r requirements.txt --format json
```

**Dernière vérification:** 2025-12-29
**Résultat:** ✅ Aucune vulnérabilité CVE détectée

---

## 🌍 Environnements Virtuels (Recommandé)

### Création d'un environnement virtuel

```bash
# Création
python3 -m venv venv

# Activation
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installation dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt  # optionnel

# Désactivation
deactivate
```

**Avantages:**
- Isolation des dépendances
- Pas de conflit avec packages système
- Reproductibilité garantie

---

## 📊 Taille des Dépendances

### Espace disque requis (approximatif)

| Composant | Taille | Description |
|-----------|--------|-------------|
| **Packages pip** | ~50 MB | python-docx, lxml, pyyaml, etc. |
| **PyCollatinus** | ~10 MB | Données morphologiques latin |
| **TreeTagger** | ~30 MB | Binaires + paramètres langue |
| **Dictionnaire Du Cange** | 80 MB | latin_analyzer/data (déjà inclus) |
| **Total** | ~170 MB | Installation complète |

---

## 🔄 Mise à Jour des Dépendances

### Vérifier les versions disponibles

```bash
pip index versions python-docx
pip index versions pyyaml
```

### Mettre à jour toutes les dépendances

```bash
pip install --upgrade -r requirements.txt
```

**⚠️ Attention:** Tester après mise à jour!

### Figer les versions exactes

```bash
pip freeze > requirements.lock
```

---

## 🐛 Résolution de Problèmes

### Problème: "ModuleNotFoundError: No module named 'yaml'"

**Solution:**
```bash
pip install pyyaml==6.0.3
```

### Problème: "ModuleNotFoundError: No module named 'pycollatinus'"

**Solution:** PyCollatinus nécessite installation manuelle (voir section PyCollatinus ci-dessus)

### Problème: "lxml installation failed"

**Solution (Linux):**
```bash
sudo apt-get install libxml2-dev libxslt1-dev
pip install lxml==6.0.2
```

**Solution (Mac):**
```bash
brew install libxml2 libxslt
pip install lxml==6.0.2
```

### Problème: TreeTagger ne se télécharge pas

**Solution:**
```bash
python3 PAGEtopage/step2_enrich/treetagger_installer.py
```

---

## 📚 Ressources

### Documentations officielles

- **python-docx:** https://python-docx.readthedocs.io/
- **lxml:** https://lxml.de/
- **PyYAML:** https://pyyaml.org/
- **TreeTagger:** https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/
- **PyCollatinus:** https://github.com/PonteIneptique/collatinus-python

### Commandes utiles

```bash
# Lister packages installés
pip list

# Afficher info package
pip show python-docx

# Vérifier compatibilité
pip check

# Audit sécurité
pip-audit
```

---

## 📝 Notes de Version

### Version 1.0 (2025-12-29)
- Documentation initiale des dépendances
- Ajout requirements.txt racine
- Ajout requirements-dev.txt
- Instructions PyCollatinus détaillées

---

**Pour toute question:** Consulter `DEPENDENCY_AUDIT_REPORT.md` ou créer une issue GitHub.
