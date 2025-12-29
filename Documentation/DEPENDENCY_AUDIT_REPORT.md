# Audit des Dépendances - Projet CiSaMe
**Date:** 2025-12-29
**Auditeur:** Claude Code
**Portée:** Analyse complète des dépendances Python

---

## 📊 Résumé Exécutif

✅ **Sécurité:** Aucune vulnérabilité connue détectée
✅ **Versions:** Toutes les dépendances listées sont à jour
⚠️ **Documentation:** Dépendances incomplètes dans requirements.txt
✅ **Bloat:** Aucun bloat détecté (80M de data = dictionnaire légitime)

---

## 🔍 Analyse Détaillée

### 1. État Actuel des Dépendances

#### Fichier: `latin_analyzer/requirements.txt`

| Package | Version Actuelle | Dernière Version | Statut | Vulnérabilités |
|---------|-----------------|------------------|--------|----------------|
| python-docx | 1.2.0 | 1.2.0 | ✅ À jour | Aucune |
| lxml | 6.0.2 | 6.0.2 | ✅ À jour | Aucune |
| unidecode | 1.4.0 | 1.4.0 | ✅ À jour | Aucune |

**Sécurité:** Audit réalisé avec `pip-audit` - Aucune vulnérabilité CVE détectée.

---

### 2. ⚠️ Dépendances Manquantes dans requirements.txt

Le projet utilise plusieurs packages qui **NE SONT PAS** documentés dans les fichiers de dépendances:

#### Module PAGEtopage
| Package | Usage | Dernière Version | Priorité |
|---------|-------|------------------|----------|
| **pyyaml** | Configuration (config.yaml) | 6.0.3 | 🔴 CRITIQUE |
| **treetaggerwrapper** | Lemmatisation TreeTagger | 2.3 | 🔴 CRITIQUE |

**Fichiers affectés:**
- `PAGEtopage/config.py:10` → `import yaml`
- `PAGEtopage/README.md:51` → Installation manuelle requise

#### Tests
| Package | Usage | Dernière Version | Priorité |
|---------|-------|------------------|----------|
| **pytest** | Framework de tests | 9.0.2 | 🟡 DÉVELOPPEMENT |

**Fichiers affectés:**
- `PAGEtopage/tests/test_*.py`
- `latin_analyzer/tests/test_*.py`

---

### 3. 📦 Analyse de Taille et Bloat

```
Taille totale du projet:
- latin_analyzer/data:     80M  (dictionnaire Du Cange - 99,917 mots)
- latin_analyzer/src:      53K  (code source)
- PAGEtopage:             494K  (module enrichissement)
- Modules_projet:          ~variée (scripts utilitaires)
```

**Verdict:** ✅ Aucun bloat détecté
- Les 80M de `latin_analyzer/data` sont du contenu légitime (dictionnaire médiéval)
- Pas de `__pycache__` détecté (bon nettoyage)
- Tailles de code raisonnables

---

### 4. 🔄 Dépendances Externes Non-pip

| Package | Installation | Statut | Notes |
|---------|--------------|--------|-------|
| **PyCollatinus** | GitHub clone | ⚠️ Non-pip | Package PyPI cassé (voir requirements.txt) |
| **TreeTagger** | Auto-download | ✅ Automatique | Installation automatique lors du 1er lancement |

**Référence:** `latin_analyzer/requirements.txt:13-14`

---

## 🎯 Recommandations

### Priorité 🔴 CRITIQUE

#### 1. Créer un requirements.txt racine complet

**Problème:** Actuellement, seul `latin_analyzer/requirements.txt` existe, mais PAGEtopage a ses propres dépendances non documentées.

**Solution:** Créer `/CiSaMe/requirements.txt` avec toutes les dépendances:

```txt
# Dépendances principales
python-docx==1.2.0
lxml==6.0.2
unidecode==1.4.0
pyyaml==6.0.3
treetaggerwrapper==2.3

# Note: PyCollatinus doit être installé manuellement depuis GitHub
# Voir: https://github.com/PonteIneptique/collatinus-python
```

#### 2. Créer requirements-dev.txt pour le développement

```txt
# Dépendances de développement
pytest==9.0.2
pytest-cov==6.0.0  # Couverture de tests
black==25.1.0      # Formatage code
flake8==8.0.0      # Linting
mypy==1.15.0       # Type checking
```

---

### Priorité 🟡 RECOMMANDÉE

#### 3. Adopter pyproject.toml (PEP 517/518)

**Avantages:**
- Standard moderne Python
- Gestion unifiée des dépendances
- Meilleure compatibilité avec pip/Poetry/uv
- Métadonnées de projet centralisées

**Exemple de structure:**

```toml
[project]
name = "cisame"
version = "1.0.0"
description = "Suite d'outils numériques pour manuscrits juridiques médiévaux"
requires-python = ">=3.10"
dependencies = [
    "python-docx==1.2.0",
    "lxml==6.0.2",
    "unidecode==1.4.0",
    "pyyaml==6.0.3",
    "treetaggerwrapper==2.3",
]

[project.optional-dependencies]
dev = [
    "pytest>=9.0.0",
    "pytest-cov>=6.0.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_backend"
```

#### 4. Ajouter pip-audit au CI/CD

**Commande à intégrer:**
```bash
pip install pip-audit
pip-audit -r requirements.txt
```

**Bénéfices:** Détection automatique de nouvelles CVE

---

### Priorité 🟢 AMÉLIORATIONS

#### 5. Versionner avec contraintes flexibles

**Actuellement:** Versions exactes (`==`)
**Problème:** Bloque les patches de sécurité
**Recommandation:** Utiliser versions compatibles (`~=`)

```txt
# Avant
python-docx==1.2.0

# Après (permet 1.2.x mais pas 1.3)
python-docx~=1.2.0
```

#### 6. Documenter les dépendances système

Créer `DEPENDENCIES.md`:

```markdown
## Dépendances Système

- Python 3.10+ (requis)
- Git (pour PyCollatinus)

## Dépendances Non-pip

- PyCollatinus: `git clone https://github.com/PonteIneptique/collatinus-python`
- TreeTagger: Téléchargement automatique au premier lancement
```

#### 7. Créer .gitignore pour cache Python

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
```

---

## 📝 Plan d'Action Recommandé

### Phase 1: Immédiat (1-2 heures)
1. ✅ Créer `requirements.txt` racine avec pyyaml et treetaggerwrapper
2. ✅ Créer `requirements-dev.txt` avec pytest
3. ✅ Ajouter/mettre à jour `.gitignore`
4. ✅ Créer `DEPENDENCIES.md` documentant PyCollatinus

### Phase 2: Court terme (1 semaine)
1. 🔄 Migrer vers `pyproject.toml`
2. 🔄 Intégrer pip-audit dans CI/CD (si applicable)
3. 🔄 Ajouter tests de dépendances manquantes

### Phase 3: Long terme (optionnel)
1. 💡 Évaluer migration vers Poetry/uv pour gestion dépendances
2. 💡 Créer requirements.lock pour reproductibilité exacte
3. 💡 Ajouter Dependabot/Renovate pour mises à jour auto

---

## 🔐 Notes de Sécurité

### Versions Sécurisées Vérifiées (2025-12-29)

Toutes les dépendances listées sont exemptes de CVE connues selon:
- `pip-audit 2.10.0`
- Base de données OSV (Open Source Vulnerabilities)
- PyPI Advisory Database

### Mises à Jour Futures

**Fréquence recommandée:** Audit trimestriel (ou immédiat si CVE critique)

**Commande de vérification:**
```bash
pip-audit -r requirements.txt --format json > audit_$(date +%Y%m%d).json
```

---

## 📚 Références

- **pip-audit:** https://pypi.org/project/pip-audit/
- **PEP 517/518:** https://peps.python.org/pep-0517/
- **Semantic Versioning:** https://semver.org/
- **Python Packaging Guide:** https://packaging.python.org/

---

## ✅ Checklist d'Implémentation

```
[ ] Créer requirements.txt racine
[ ] Créer requirements-dev.txt
[ ] Tester installation complète: pip install -r requirements.txt
[ ] Mettre à jour README.md avec instructions installation
[ ] Ajouter .gitignore si absent
[ ] Créer DEPENDENCIES.md
[ ] (Optionnel) Migrer vers pyproject.toml
[ ] (Optionnel) Configurer CI/CD avec pip-audit
```

---

**Fin du rapport**
Pour toute question: voir documentation ou créer une issue GitHub
