# 📋 ROADMAP - Enrichisseur Bibliographique

**Projet** : Outil Python pour enrichir les notes bibliographiques en humanités digitales
**Version actuelle** : 0.1.0 (Workflow 1 - MVP)
**Dernière mise à jour** : 2025-12-30

---

## ✅ WORKFLOW 1 - Enrichissement bibliographique (ACTUEL)

### Fonctionnalités implémentées

- [x] **Scanner de fichiers Markdown**
  - Détection des tags `%% #reflitterature description %%`
  - Extraction des citations entre `== ==` avant le tag
  - Parsing intelligent : `(Auteur Année)` ou `(Auteur et Auteur Année)`
  - Extraction du contexte (N lignes autour de la référence)
  - Gestion des noms de fichiers avec espaces

- [x] **Recherche dans bibliographie locale**
  - Scan du fichier bibliographie.md
  - Matching par auteur(s) + année(s)
  - Récupération de la référence complète
  - Score de matching (minimum 2 correspondances)

- [x] **Extraction de métadonnées avec LLM local**
  - Intégration Ollama (llama3.1:8b)
  - Extraction : auteur, titre, année
  - Gestion des erreurs OCR
  - Fallback gracieux en cas d'erreur

- [x] **Recherche DOI via APIs publiques**
  - OpenAlex (prioritaire) - API gratuite
  - CrossRef (backup) - API gratuite
  - Calcul de score de confiance (similarité titre + match année)
  - Pas de clé API requise

- [x] **Génération de rapports**
  - Export JSON (données structurées)
  - Export Markdown (rapport lisible)
  - Timestamps et métadonnées de traitement
  - Statistiques de réussite

- [x] **Configuration flexible**
  - Fichier config.py séparé
  - Chemins configurables
  - Modèle LLM configurable
  - Paramètres de recherche ajustables

- [x] **Portabilité**
  - Architecture mince (3 fichiers principaux)
  - Copiable entre vaults Obsidian
  - Dépendances minimales
  - Pas de base de données externe

---

## 🚧 WORKFLOW 1 - À compléter

### Intégration Zotero

- [ ] **Installation de pyzotero**
  - Ajouter `pyzotero` à requirements.txt
  - Documentation installation et configuration

- [ ] **Configuration Zotero dans config.py**
  - `ZOTERO_LIBRARY_ID` (ID utilisateur ou groupe)
  - `ZOTERO_API_KEY` (clé privée depuis zotero.org/settings/keys)
  - `ZOTERO_LIBRARY_TYPE` ('user' ou 'group')

- [ ] **Fonction de connexion à Zotero**
  - Test de connexion au démarrage
  - Validation des credentials
  - Gestion des erreurs d'authentification

- [ ] **Création d'entrées Zotero**
  - Mapping métadonnées → format Zotero
  - Support types : article, livre, chapitre, rapport
  - Ajout du DOI et URL
  - Préservation des métadonnées existantes

- [ ] **Gestion des doublons**
  - Requête pour vérifier si DOI existe déjà
  - Vérification par auteur + année + titre
  - Option : mettre à jour vs ignorer vs créer nouveau

- [ ] **Validation utilisateur**
  - Mode interactif : afficher métadonnées avant import
  - Demander confirmation pour chaque référence
  - Permettre édition manuelle des champs
  - Option --auto pour import sans confirmation

- [ ] **Gestion des collections Zotero**
  - Créer collection "Enrichissement auto" si n'existe pas
  - Option pour spécifier collection cible
  - Tags automatiques (ex: "auto-enriched", "needs-review")

### Amélioration de la robustesse

- [ ] **Gestion d'erreurs API**
  - Retry automatique avec backoff exponentiel
  - Timeout configurable par API
  - Fallback si API indisponible
  - Logs détaillés des erreurs

- [ ] **Support de formats variés**
  - Détection de citations sans parenthèses
  - Support format "Auteur (Année)"
  - Support notes de bas de page
  - Citations multiples sur plusieurs lignes

- [ ] **Tests unitaires**
  - Tests pour extraction de citations
  - Tests pour matching bibliographie
  - Tests pour parsing métadonnées
  - Mocks des APIs externes

- [ ] **Validation des données**
  - Vérifier format DOI
  - Valider années (1900-2030)
  - Détecter métadonnées incohérentes
  - Warnings pour confiance < 30%

### Interface utilisateur

- [ ] **Mode interactif**
  - Afficher chaque référence trouvée
  - Proposer corrections pour métadonnées
  - Confirmer DOI avant ajout Zotero
  - Navigation : skip, retry, quit

- [ ] **Barre de progression améliorée**
  - Afficher référence en cours
  - Temps estimé restant
  - Statistiques live (DOI trouvés/total)

- [ ] **Logs verbeux**
  - Flag --debug pour logs détaillés
  - --quiet pour mode silencieux
  - Sauvegarde logs dans fichier
  - Niveaux : INFO, WARNING, ERROR, DEBUG

- [ ] **Rapport d'erreurs**
  - Section dédiée dans rapport .md
  - Liste des références non résolues
  - Suggestions de correction
  - Export CSV des erreurs

---

## 📋 WORKFLOW 2 - Insertion clés BibTeX (FUTUR)

### Objectif
Remplacer automatiquement les tags `#reflitterature` par des clés BibTeX Zotero (ex: `@habermas2021`) dans les notes Markdown.

### Fonctionnalités à développer

- [ ] **Récupération des clés Zotero**
  - Lister toutes les entrées de la bibliothèque Zotero
  - Extraire citation keys (format BetterBibTeX ou standard)
  - Créer mapping DOI → citation key
  - Cache local pour éviter requêtes répétées

- [ ] **Analyse des modifications à faire**
  - Scanner le fichier source
  - Identifier références déjà enrichies (avec DOI connu)
  - Proposer remplacement tag → citation key
  - Générer diff des modifications

- [ ] **Remplacement automatique**
  - Backup automatique du fichier (.bak)
  - Remplacement `%% #reflitterature ... %%` → `[@citationkey]`
  - Préservation du commentaire original (en commentaire caché)
  - Option de garder le surlignage `== ==`

- [ ] **Mode dry-run**
  - Preview des changements sans modifier fichier
  - Export diff coloré (terminal ou HTML)
  - Validation manuelle avant application
  - Rollback si erreur

- [ ] **Génération de bibliographie**
  - Collecter toutes les citations du fichier
  - Générer section "## Références" en fin de fichier
  - Format Markdown standard
  - Mise à jour automatique si section existe déjà

- [ ] **Gestion des citations multiples**
  - Support `[@habermas2021; @habermas1992]`
  - Ordre chronologique ou alphabétique
  - Préfixes et suffixes (ex: `[voir @habermas2021, p. 42]`)

---

## 🧠 WORKFLOW 3 - Analyse conceptuelle + Neo4j (FUTUR)

### Objectif
Utiliser un agent LangChain intelligent pour extraire arguments, concepts et relations sémantiques, puis les stocker dans Neo4j pour analyse de réseau de connaissances.

### Pourquoi LangChain ici et pas pour Workflow 1 ?

**Workflow 1 = Pipeline linéaire simple**
- Séquence fixe : scan → extraction → API → rapport
- Pas de décision complexe à prendre
- Chaque étape est déterministe
- Overhead de LangChain inutile
- Code plus simple = plus maintenable

**Workflow 3 = Orchestration intelligente nécessaire**
- Décisions contextuelles (quel concept extraire ? quelle relation créer ?)
- Stratégies multiples selon le type de texte
- Itérations possibles (approfondir une analyse)
- Besoin de tools complexes (Neo4j queries, analyse sémantique)
- Mémoire de conversation pour contexte
- LangChain apporte : agents, tools, chains, mémoire

### Architecture LangChain proposée

- [ ] **Migration vers LangChain**
  - Installer `langchain`, `langchain-community`, `langchain-ollama`
  - Créer agent avec modèle Ollama
  - Définir system prompt pour analyse conceptuelle

- [ ] **Définition des Tools**

  **Tools Neo4j :**
  - `create_author_node(name, bio)` : Créer nœud Auteur
  - `create_work_node(title, year, type)` : Créer nœud Œuvre
  - `create_concept_node(name, definition)` : Créer nœud Concept
  - `create_argument_node(text, type)` : Créer nœud Argument
  - `create_relation(from, to, type, properties)` : Créer relation
  - `query_graph(cypher_query)` : Requête Cypher libre
  - `find_related(node_id, depth)` : Trouver nœuds liés

  **Tools d'analyse :**
  - `extract_arguments(context)` : Extraire arguments du texte
  - `identify_concepts(text)` : Identifier concepts clés
  - `find_semantic_relations(arg1, arg2)` : Détecter type de relation
  - `summarize_position(author, topic)` : Résumer position d'un auteur

- [ ] **Agent orchestrateur**
  - Décider quelle stratégie d'analyse selon contexte
  - Choisir tools appropriés dynamiquement
  - Itérer si information incomplète
  - Générer plan d'analyse automatique

### Intégration Neo4j

- [ ] **Configuration Neo4j**
  - Installation Neo4j Desktop ou Docker
  - Configuration dans config.py (URI, user, password)
  - Test de connexion
  - Driver Python neo4j

- [ ] **Modèle de données (nodes)**
  - **Auteur** : name, birth_year, affiliation, bio
  - **Œuvre** : title, year, type (article/livre/chapitre), DOI, abstract
  - **Concept** : name, definition, domain (philosophie/sociologie/etc.)
  - **Argument** : text, type (thèse/antithèse/synthèse), strength_score
  - **Note** : file_path, line_number, context, comment

- [ ] **Modèle de données (relations)**
  - **AUTHORED** : Auteur → Œuvre
  - **CITES** : Œuvre → Œuvre (properties: page, context)
  - **DISCUSSES** : Œuvre → Concept
  - **CONTAINS** : Œuvre → Argument
  - **SUPPORTS** : Argument → Argument
  - **OPPOSES** : Argument → Argument
  - **SYNTHESIZES** : Argument → [Argument, Argument]
  - **ANNOTATED_IN** : Œuvre → Note

- [ ] **Requêtes Cypher utiles**
  - Trouver tous les auteurs qui discutent d'un concept
  - Chaînes d'argumentation (A soutient B qui oppose C)
  - Auteurs les plus cités dans mes notes
  - Concepts récurrents dans un domaine
  - Graphe de co-citation

### Analyse sémantique avancée

- [ ] **Extraction d'arguments**
  - Parser le contexte autour de la citation
  - Identifier : thèse principale, prémisses, conclusions
  - Détecter modalités (certitude, doute, hypothèse)
  - Extraire nuances du commentaire `%% ... %%`

- [ ] **Identification de relations**
  - **CITE** : simple mention
  - **CRITIQUE** : désaccord, réfutation
  - **SOUTIENT** : accord, confirmation
  - **OPPOSE** : contradiction directe
  - **NUANCE** : apporte précision/limite
  - **SYNTHÉTISE** : combine plusieurs positions

- [ ] **Détection de concepts**
  - NER (Named Entity Recognition) pour concepts académiques
  - Clustering de termes similaires
  - Hiérarchie conceptuelle (concept → sous-concept)
  - Évolution temporelle des concepts

- [ ] **Chaînes d'argumentation**
  - Reconstruire la logique : A → B → C
  - Détecter contradictions dans mes notes
  - Identifier arguments circulaires
  - Force de la chaîne (score cumulatif)

### Visualisation et exploration

- [ ] **Export pour Neo4j Browser**
  - Scripts Cypher pour importer données
  - Vues prédéfinies
  - Style visuel (couleurs par type de nœud)

- [ ] **Graphes interactifs**
  - Intégration vis.js ou d3.js
  - Export HTML standalone
  - Filtres par type, auteur, période
  - Zoom sur sous-graphes

- [ ] **Tableaux de bord**
  - Statistiques : nb concepts, auteurs, relations
  - Timeline des lectures
  - Heatmap des domaines étudiés
  - Top concepts/auteurs

- [ ] **Requêtes prédéfinies utiles**
  - "Qui critique qui ?"
  - "Quels auteurs parlent de X ?"
  - "Chaîne argumentative pour concept Y"
  - "Évolution de mon intérêt (par date notes)"
  - "Trous dans mes lectures (concepts non explorés)"

---

## 🔧 AMÉLIORATIONS TECHNIQUES

### Tests et qualité

- [ ] **Tests unitaires**
  - pytest pour tous les modules
  - Coverage > 80%
  - Fixtures pour APIs (mocking)
  - Tests d'intégration

- [ ] **Tests d'intégration**
  - Test complet end-to-end
  - Environnement de test (vault factice)
  - CI/CD avec GitHub Actions

- [ ] **Linting et formatage**
  - black (formatage code)
  - pylint (qualité code)
  - mypy (type checking)
  - pre-commit hooks

### Packaging et distribution

- [ ] **Structure de package Python**
  - setup.py ou pyproject.toml
  - Versioning sémantique
  - Changelog automatique

- [ ] **Installation via pip**
  - Publication sur PyPI
  - `pip install biblio-enricher`
  - Gestion des dépendances automatique

- [ ] **CLI professionnel**
  - Utiliser `click` ou `typer`
  - Sous-commandes : `enrich`, `insert-keys`, `analyze`
  - Autocomplétion bash/zsh
  - Help contextuel

- [ ] **Configuration flexible**
  - Support .env pour secrets
  - Config YAML pour préférences
  - Priorité : CLI args > .env > config.py > defaults

### Performance

- [ ] **Cache intelligent**
  - Cache local pour résultats API (éviter requêtes répétées)
  - TTL configurable
  - Invalidation sélective

- [ ] **Parallélisation**
  - Traitement concurrent de multiples références
  - asyncio pour requêtes API
  - Pool de workers pour LLM

- [ ] **Optimisations**
  - Batch API requests quand possible
  - Lazy loading des modèles LLM
  - Streaming pour gros fichiers

---

## 📚 DOCUMENTATION

### Documentation utilisateur

- [ ] **Guide d'installation complet**
  - Prerequisites détaillés (OS, Python version)
  - Installation pas-à-pas (Ollama, Neo4j, etc.)
  - Troubleshooting pour chaque OS
  - FAQ

- [ ] **Tutoriel interactif**
  - Exemple de vault Obsidian inclus
  - Walkthrough complet des 3 workflows
  - Vidéo de démonstration
  - Jupyter notebook pour tests

- [ ] **Documentation des APIs**
  - OpenAlex : limites, formats, exemples
  - CrossRef : idem
  - Zotero : authentification, types, champs
  - Neo4j : requêtes utiles, bonnes pratiques

- [ ] **Guide de troubleshooting**
  - Erreurs courantes et solutions
  - Diagnostic automatique (script --check)
  - Logs d'erreur : où les trouver, comment les lire
  - Contact / issues GitHub

### Documentation développeur

- [ ] **Architecture du code**
  - Diagrammes de classes
  - Flow charts des workflows
  - Explication des choix techniques

- [ ] **Guide de contribution**
  - Comment contribuer (PR, issues)
  - Standards de code
  - Comment ajouter un nouveau workflow
  - Comment ajouter un nouveau tool LangChain

- [ ] **API Reference**
  - Docstrings complètes (Google style)
  - Génération automatique avec Sphinx
  - Exemples pour chaque fonction
  - Types hints complets

- [ ] **Roadmap publique**
  - Priorisation des features
  - Milestones et deadlines
  - Demandes communauté

---

## 📊 MÉTRIQUES DE SUCCÈS

### Workflow 1
- [ ] Taux de succès > 80% pour DOI
- [ ] Temps traitement < 5s par référence
- [ ] Zéro modification des fichiers source (read-only)

### Workflow 2
- [ ] 100% backup avant modification
- [ ] Rollback fonctionnel
- [ ] Compatibilité Pandoc pour export

### Workflow 3
- [ ] Extraction concepts : precision > 70%
- [ ] Relations sémantiques : recall > 60%
- [ ] Temps d'analyse < 30s par note

---

## 🗓️ PLANNING INDICATIF

**Phase 1** (actuelle) : Workflow 1 MVP ✅
**Phase 2** (1-2 mois) : Workflow 1 complet + Zotero
**Phase 3** (2-3 mois) : Workflow 2 + BibTeX
**Phase 4** (3-6 mois) : Workflow 3 + Neo4j + LangChain
**Phase 5** (ongoing) : Améliorations, tests, docs

---

**Note** : Ce document est un plan évolutif. Les priorités peuvent changer selon les retours utilisateurs et les besoins du projet.
