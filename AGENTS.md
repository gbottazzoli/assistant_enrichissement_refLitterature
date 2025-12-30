# 🤖 Agents Automatiques du Projet

Ce projet utilise 3 agents automatiques pour différentes tâches.

---

## 1️⃣ Agent Principal : Enrichissement Bibliographique

**Fichier** : `agent.py`

**Fonction** : Enrichir les références bibliographiques dans vos notes Markdown

**Commande** :
```bash
python3 agent.py "votre_fichier.md"
```

**Ce qu'il fait** :
- Scanne le fichier pour tags `%% #reflitterature ... %%`
- Extrait les citations (format `Auteur Année`)
- Cherche dans bibliographie locale
- Appelle LLM (Ollama) pour nettoyer OCR
- Interroge APIs (OpenAlex + CrossRef) pour trouver DOI
- Génère rapports JSON + Markdown

**Résultats** : `results/fichier_TIMESTAMP_report.md`

---

## 2️⃣ Agent de Maintenance : Documentation Projet

**Fichier** : `project_state.py`

**Fonction** : Générer l'état complet du projet pour développement futur

**Commande** :
```bash
python3 project_state.py
```

**Ce qu'il fait** :
- Scanne tous les fichiers Python
- Extrait fonctions, classes, imports
- Parse la configuration
- Calcule les statistiques
- Génère rapport complet (`PROJECT_STATE.md`)
- Met à jour `README.md` avec stats actuelles
- Exporte JSON structuré (`project_state.json`)

**Quand l'utiliser** :
- Avant tout nouveau développement
- Après ajout de fonctionnalités majeures
- Pour partager l'état du projet avec Claude Code

**Pour Claude Code** :
> Avant de développer, lisez `PROJECT_STATE.md`

---

## 3️⃣ Agent Git : Publication Automatique

**Fichier** : `git_publish.py`

**Fonction** : Publier le projet sur GitHub avec vérifications de sécurité

**Commande** :
```bash
python3 git_publish.py
```

**Ce qu'il fait** :
- Vérifie que Git est installé et configuré
- Initialise le repo si nécessaire
- Configure le remote GitHub
- Stage les fichiers (selon `.gitignore`)
- **Scanne les secrets** (clés API, passwords)
- Demande confirmation
- Crée commit (message auto ou custom)
- Push vers `https://github.com/gbottazzoli/assistant_enrichissement_refLitterature`

**Sécurité** :
- Ignore `config.py` (secrets)
- Ignore `results/` (données perso)
- Ignore `../*.md` (vos notes)
- Détecte patterns suspects dans les fichiers

**Première utilisation** :
Voir `GIT_SETUP.md` pour configuration initiale

---

## 🔄 Workflow Recommandé

### Développement quotidien

```bash
# 1. Utiliser l'agent principal
python3 agent.py "ma_note.md"

# 2. Consulter les résultats
cat results/ma_note_*_report.md
```

### Avant de développer de nouvelles fonctionnalités

```bash
# 1. Mettre à jour la doc projet
python3 project_state.py

# 2. Lire l'état du projet
cat PROJECT_STATE.md
```

### Publication sur GitHub

```bash
# 1. S'assurer que doc est à jour
python3 project_state.py

# 2. Publier
python3 git_publish.py
```

---

## 📋 Fichiers de Configuration

| Fichier | Usage | Versionné ? |
|---------|-------|-------------|
| `config.py` | **Votre config locale** (secrets, chemins) | ❌ Non (ignoré) |
| `config.example.py` | Template de configuration | ✅ Oui |
| `.gitignore` | Fichiers à ignorer pour Git | ✅ Oui |

**Important** : Ne modifiez que `config.py` (vos valeurs perso)

---

## 🎯 Résumé des Commandes

```bash
# Enrichissement bibliographique
python3 agent.py "fichier.md"

# Mise à jour documentation
python3 project_state.py

# Publication GitHub
python3 git_publish.py
```

---

## 🛠️ Fichiers Générés Automatiquement

| Fichier | Générateur | Description |
|---------|-----------|-------------|
| `results/*.json` | `agent.py` | Résultats enrichissement (JSON) |
| `results/*_report.md` | `agent.py` | Rapports lisibles |
| `PROJECT_STATE.md` | `project_state.py` | État complet du projet |
| `project_state.json` | `project_state.py` | Données structurées |
| `README.md` (stats) | `project_state.py` | Stats auto-mises à jour |

---

## 📚 Documentation

- **README.md** : Installation et utilisation générale
- **TODO.md** : Roadmap du projet (3 workflows)
- **PROJECT_STATE.md** : État actuel (auto-généré)
- **GIT_SETUP.md** : Configuration Git/GitHub
- **AGENTS.md** : Ce fichier (résumé des agents)
- **QUICKSTART.md** : Démarrage rapide
- **AIDE-MEMOIRE.md** : Référence rapide commandes

---

## 🔮 Évolutions Futures des Agents

### Agent Principal (agent.py)
- [ ] Mode interactif (validation DOI)
- [ ] Intégration Zotero
- [ ] Support ISBN (livres)

### Agent Documentation (project_state.py)
- [ ] Génération diagrammes (classes, flow)
- [ ] Détection code mort
- [ ] Analyse complexité

### Agent Git (git_publish.py)
- [ ] Génération CHANGELOG automatique
- [ ] Détection breaking changes
- [ ] Publication releases GitHub

---

**Note** : Tous les agents sont autonomes et peuvent être lancés indépendamment.
