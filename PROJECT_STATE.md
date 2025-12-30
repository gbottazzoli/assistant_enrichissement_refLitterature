# 📊 ÉTAT DU PROJET - biblio-enricher

**Généré le** : 2025-12-30 09:40:11
**Version** : 0.1.0

---

## 📈 Statistiques globales

| Métrique | Valeur |
|----------|--------|
| Fichiers Python | 4 |
| Lignes de code | 886 |
| Fonctions | 23 |
| Classes | 2 |
| Dépendances | 5 |
| Fichiers de documentation | 9 |

---

## 🗂️ Structure des fichiers Python


### agent.py

**Lignes** : 542

**Classes** :
- `BiblioEnricher` (ligne 27)
  - Méthodes : __init__, _check_ollama, scan_file, search_in_bibliography, extract_metadata_with_llm, search_openalex, search_crossref, _similarity_score, process_references, save_results

**Fonctions** :
- `main()` (ligne 498)
- `__init__(self, vault_path)` (ligne 30)
- `_check_ollama(self)` (ligne 45)
- `scan_file(self, filename)` (ligne 61)
- `search_in_bibliography(self, ref_text)` (ligne 137)
- `extract_metadata_with_llm(self, ref_text, full_ref)` (ligne 189)
- `search_openalex(self, author, title, year)` (ligne 252)
- `search_crossref(self, author, title, year)` (ligne 313)
- `_similarity_score(self, str1, str2)` (ligne 372)
- `process_references(self, references)` (ligne 391)
- `save_results(self, results, source_file)` (ligne 443)

**Imports** : re, requests, os, pathlib, typing, tqdm, json, config, sys, datetime, ollama


### config.example.py

**Lignes** : 43


### config.py

**Lignes** : 42


### git_publish.py

**Lignes** : 259

**Classes** :
- `GitPublisher` (ligne 14)
  - Méthodes : __init__, run_cmd, check_git_installed, init_repo_if_needed, ensure_gitignore, check_for_secrets, get_status, stage_files, create_commit, push_to_remote, show_summary

**Fonctions** :
- `main()` (ligne 204)
- `__init__(self)` (ligne 17)
- `run_cmd(self, cmd, check)` (ligne 28)
- `check_git_installed(self)` (ligne 46)
- `init_repo_if_needed(self)` (ligne 53)
- `ensure_gitignore(self)` (ligne 76)
- `check_for_secrets(self)` (ligne 84)
- `get_status(self)` (ligne 127)
- `stage_files(self)` (ligne 132)
- `create_commit(self, message)` (ligne 153)
- `push_to_remote(self, branch)` (ligne 164)
- `show_summary(self)` (ligne 191)

**Imports** : re, pathlib, subprocess, sys, datetime


---

## ⚙️ Configuration actuelle

```python
BIBLIO_FILE = "4.4 Bibliographic references.md"
CONTEXT_LINES = 3
CROSSREF_EMAIL = None  # Optionnel
MIN_CONFIDENCE_SCORE = 0.5
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_URL = "http://localhost:11434"
OPENALEX_EMAIL = None  # Optionnel : votre email pour être poli avec l'API
OUTPUT_DIR = "results"
OUTPUT_FORMAT = "both"
VAULT_PATH = ".."  # Dossier parent (le vault Obsidian)
```

---

## 📦 Dépendances

- requests>=2.31.0
- markdown-it-py>=3.0.0
- ollama>=0.1.0
- regex>=2023.0.0
- tqdm>=4.66.0

---

## 📚 Documentation disponible

- **AGENTS.md** (196 lignes)
- **EXAMPLE_TEST.md** (33 lignes)
- **GIT_SETUP.md** (186 lignes)
- **LISTE_FICHIERS.txt** (78 lignes)
- **PROJECT_STATE.md** (155 lignes)
- **QUICKSTART.md** (142 lignes)
- **README.md** (226 lignes)
- **TODO.md** (481 lignes)
- **requirements.txt** (16 lignes)

---

## 🎯 Fonctionnalités implémentées

### Scanner de fichiers
- ✅ Détection tags `#reflitterature`
- ✅ Extraction citations entre `== ==`
- ✅ Parsing auteur/année
- ✅ Extraction contexte

### Recherche bibliographique
- ✅ Matching dans fichier bibliographie local
- ✅ Score de matching (auteur + année)

### Enrichissement métadonnées
- ✅ LLM local (Ollama)
- ✅ Extraction : auteur, titre, année
- ✅ Gestion erreurs OCR

### APIs externes
- ✅ OpenAlex (prioritaire)
- ✅ CrossRef (backup)
- ✅ Calcul score de confiance

### Sortie
- ✅ Rapport JSON
- ✅ Rapport Markdown
- ✅ Statistiques de réussite

---

## 🚧 Prochaines étapes (voir TODO.md)

1. **Intégration Zotero** avec pyzotero
2. **Mode interactif** pour validation
3. **Gestion doublons** Zotero
4. **Tests unitaires**
5. **Workflow 2** : Insertion clés BibTeX
6. **Workflow 3** : LangChain + Neo4j

---

## 🔧 Points d'attention pour développement futur

### Architecture actuelle
- Pipeline linéaire simple (scan → extract → API → report)
- Pas de base de données externe
- Configuration via config.py
- Portable entre vaults Obsidian

### Bonnes pratiques à maintenir
- Read-only sur fichiers source (pas de modification)
- Fallback gracieux en cas d'erreur
- Configuration séparée du code
- Rapports horodatés

### Améliorations nécessaires
- Gestion d'erreurs API plus robuste (retry, timeout)
- Tests unitaires manquants
- Mode interactif à implémenter
- Logs plus verbeux (--debug)

---

**Fichier généré automatiquement par `project_state.py`**
