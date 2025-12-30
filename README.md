# Agent Bibliographique pour Humanités Digitales

<!-- AUTO-GENERATED STATS - DO NOT EDIT -->
**Stats du projet** : 886 lignes | 23 fonctions | 2 classes
<!-- END AUTO-GENERATED -->

## Description

Outil d'enrichissement automatique de références bibliographiques pour la recherche en histoire et humanités digitales.

### Problématique

Lors de la prise de notes de lecture dans Obsidian (format Markdown), les références bibliographiques sont :
- Taggées de manière informelle avec highlights et commentaires
- Écrites dans des formats hétérogènes selon les auteurs
- Souvent fragmentaires ou avec des erreurs OCR (conversion PDF → MD)
- Dispersées entre mentions rapides, notes de bas de page et bibliographies

La recherche manuelle de DOI/ISBN pour chaque référence et leur intégration dans Zotero est chronophage (50-100 références/semaine).

### Solution proposée

Un agent IA local basé sur LLM qui automatise trois workflows distincts :

#### **Workflow 1 : Enrichissement bibliographique** (prioritaire)
1. Détection des tags et citations dans les fichiers `.md`
2. Extraction du contexte et recherche de références complètes dans le corpus local
3. Utilisation d'un LLM local (Ollama) pour comprendre et structurer les références malgré les erreurs
4. Interrogation d'APIs bibliographiques (OpenAlex, CrossRef, WorldCat)
5. Validation et import automatique dans Zotero

#### **Workflow 2 : Insertion des clés BibTeX** (futur)
- Remplacement des tags par les clés BibTeX Zotero (`@auteur2023`)
- Préparation des documents pour export académique (Pandoc/LaTeX)

#### **Workflow 3 : Cartographie conceptuelle** (futur)
- Analyse sémantique du corpus annoté
- Construction d'un graphe de connaissances dans Neo4j
- Visualisation des relations entre auteurs, concepts et arguments

## Stack technique

- **Python 3.10+** : orchestration et scripts
- **Ollama + Llama 3.1** : LLM local pour compréhension contextuelle
- **LangChain** : framework pour la gestion d'agents et tools
- **APIs** : OpenAlex, CrossRef, WorldCat, Zotero
- **Obsidian** : interface de travail (notes en Markdown)
- **Neo4j** : base de données graphe (Workflow 3)

## Objectifs pédagogiques

Ce projet sert également d'apprentissage pratique pour :
- Développement d'agents IA avec LangChain
- Intégration d'APIs REST
- Manipulation de graphes de connaissances (Neo4j)
- Automatisation de workflows de recherche académique

## Installation rapide

### Prérequis

- Python 3.10+
- Ollama installé et lancé (`ollama serve`)
- Modèle Llama 3.1 téléchargé (`ollama pull llama3.1:8b`)

### Installation

```bash
# Cloner le repository
git clone https://github.com/gbottazzoli/assistant_enrichissement_refLitterature.git
cd assistant_enrichissement_refLitterature

# Installer les dépendances
pip install -r requirements.txt

# Copier et configurer
cp config.example.py config.py
# Éditer config.py avec vos chemins et préférences
```

### Utilisation

```bash
# Enrichir un fichier de notes
python3 agent.py "votre_fichier.md"

# Les résultats sont dans results/
```

Voir **QUICKSTART.md** pour un guide détaillé.

## Documentation

- **QUICKSTART.md** : Guide de démarrage rapide
- **TODO.md** : Roadmap complète des 3 workflows
- **PROJECT_STATE.md** : État actuel du projet (auto-généré)
- **AGENTS.md** : Description des 3 agents automatiques
- **GIT_SETUP.md** : Configuration Git/GitHub

## Statut

🚧 **En développement** - Workflow 1 en cours d'implémentation

**Version actuelle** : 0.1.0

### Fonctionnalités implémentées (Workflow 1)

- ✅ Scanner de fichiers Markdown avec détection tags `#reflitterature`
- ✅ Extraction citations entre `== ==`
- ✅ Recherche dans bibliographie locale
- ✅ Enrichissement via LLM local (Ollama)
- ✅ APIs OpenAlex et CrossRef (gratuites, sans clé)
- ✅ Génération rapports JSON + Markdown
- ✅ Calcul scores de confiance

### Prochaines étapes

- [ ] Intégration Zotero (pyzotero)
- [ ] Mode interactif avec validation
- [ ] Gestion des doublons
- [ ] Tests unitaires

Voir **TODO.md** pour la roadmap complète.

## Structure du projet

```
biblio-enricher/
├── agent.py              # Agent principal d'enrichissement
├── config.example.py     # Template de configuration
├── requirements.txt      # Dépendances Python
├── project_state.py      # Agent de maintenance documentation
├── git_publish.py        # Agent Git automatique
└── results/              # Résultats générés (ignoré par Git)
```

## Agents automatiques

Le projet utilise 3 agents spécialisés :

1. **Agent principal** (`agent.py`) : Enrichissement bibliographique
2. **Agent documentation** (`project_state.py`) : Maintenance de la doc projet
3. **Agent Git** (`git_publish.py`) : Publication sécurisée sur GitHub

Voir **AGENTS.md** pour plus de détails.

## Auteur

Étudiant en histoire et humanités digitales

## Licence

À définir
