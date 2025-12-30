# 📚 Enrichisseur Bibliographique pour Obsidian


<!-- AUTO-GENERATED STATS - DO NOT EDIT -->
**Stats du projet** : 886 lignes | 23 fonctions | 2 classes
<!-- END AUTO-GENERATED -->

Agent Python pour enrichir automatiquement vos notes bibliographiques avec DOI et métadonnées.

## 🎯 Fonctionnalités (Étape 1)

- ✅ Scanne les fichiers Markdown pour tags `#reflitterature`
- ✅ Extrait le contexte autour des références
- ✅ Cherche des références complètes dans votre fichier bibliographie
- ✅ Utilise un LLM local (Ollama) pour nettoyer les erreurs OCR
- ✅ Interroge les APIs gratuites (OpenAlex prioritaire, CrossRef en backup)
- ✅ Génère un rapport avec scores de confiance (JSON + Markdown)

## 📋 Prérequis

1. **Python 3.8+** (vérifier : `python3 --version`)
2. **Ollama** installé et lancé localement
3. **Git** (optionnel, pour cloner)

## 🚀 Installation

### 1. Copier les fichiers dans votre vault Obsidian

Copiez le dossier `biblio-enricher/` à la racine de votre vault :

```
MonVault/
├── biblio-enricher/     ← Coller ici
│   ├── agent.py
│   ├── config.py
│   └── requirements.txt
├── 1.2 The impact...md
├── 4.4 Bibliographic references.md
└── ...
```

### 2. Installer les dépendances Python

Ouvrez un terminal dans le dossier `biblio-enricher/` :

```bash
cd /chemin/vers/MonVault/biblio-enricher

# Créer un environnement virtuel (recommandé)
python3 -m venv venv

# Activer l'environnement
# Sur Linux/Mac :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Installer et configurer Ollama

**Installation d'Ollama** :
- Linux/Mac : https://ollama.com/download
- Vérifier : `ollama --version`

**Télécharger le modèle** :
```bash
ollama pull llama3.1
```

**Démarrer Ollama** :
```bash
ollama serve
```
(Laissez cette fenêtre de terminal ouverte)

### 4. Configuration (optionnel)

Éditez `config.py` pour ajuster :

```python
# Chemins
VAULT_PATH = "."  # Dossier de votre vault
BIBLIO_FILE = "4.4 Bibliographic references.md"

# Modèle LLM
OLLAMA_MODEL = "llama3.1"  # Ou un autre modèle installé

# APIs (optionnel mais recommandé)
OPENALEX_EMAIL = "votre.email@exemple.com"  # Pour être poli avec l'API
CROSSREF_EMAIL = "votre.email@exemple.com"
```

**Note** : Les APIs OpenAlex et CrossRef sont **gratuites** et **ne nécessitent pas de clé**. Fournir votre email est optionnel mais recommandé (meilleurs quotas).

## 🎮 Utilisation

### Commande de base

```bash
python agent.py "nom_du_fichier.md"
```

### Exemples

```bash
# Traiter un fichier spécifique
python agent.py "1.2 The impact of digitalisation on intellectual life.md"

# Si le nom contient des espaces, utilisez des guillemets !
python agent.py "2.3 The world of open materials.md"

# Sans extension .md (ajoutée automatiquement)
python agent.py "1.2 The impact of digitalisation on intellectual life"
```

### Sortie

Le script génère deux fichiers dans `results/` :

1. **JSON** : `nom_fichier_YYYYMMDD_HHMMSS.json`
   - Format structuré pour traitement ultérieur
   - Contient toutes les métadonnées

2. **Markdown** : `nom_fichier_YYYYMMDD_HHMMSS_report.md`
   - Rapport lisible par humain
   - Visualisable directement dans Obsidian

## 📊 Exemple de sortie

```markdown
## Référence 1

**Ligne 18**: deux références Habermas, sphère publique

**Métadonnées extraites**:
- Auteur: Habermas, Jürgen
- Titre: The Structural Transformation of the Public Sphere
- Année: 1992

**Résultat API (OpenAlex)**:
- DOI: `10.1080/01916599.2024.2365143`
- URL: https://doi.org/10.1080/01916599.2024.2365143
- Score de confiance: 87.5%
```

## 🔧 Dépannage

### "Ollama n'est pas accessible"
```bash
# Vérifier qu'Ollama tourne
ollama list

# Si non, le démarrer
ollama serve
```

### "Le modèle llama3.1 n'est pas installé"
```bash
ollama pull llama3.1
```

### "Fichier non trouvé"
- Vérifiez que vous êtes dans le bon dossier (`cd biblio-enricher`)
- Vérifiez le chemin dans `config.py` → `VAULT_PATH`
- Utilisez des guillemets autour du nom de fichier

### "Aucune référence trouvée"
- Vérifiez que vos tags sont au format : `%% #reflitterature description %%`
- Pas d'espace manquant avant/après `%%`

## 📁 Structure des fichiers

```
biblio-enricher/
├── agent.py              # Script principal (lancez celui-ci)
├── config.py             # Configuration (modifiez selon vos besoins)
├── requirements.txt      # Dépendances Python
├── README.md            # Ce fichier
└── results/             # Dossier de sortie (créé automatiquement)
    ├── fichier_20250101_120000.json
    └── fichier_20250101_120000_report.md
```

## 🚚 Portabilité entre vaults

Pour copier ce système vers un autre vault :

1. **Copier le dossier** `biblio-enricher/` complet
2. **Ajuster** `config.py` si nécessaire (notamment `BIBLIO_FILE`)
3. **Réactiver** l'environnement virtuel :
   ```bash
   cd biblio-enricher
   source venv/bin/activate  # ou venv\Scripts\activate sur Windows
   ```

C'est tout ! Les dépendances sont déjà installées dans `venv/`.

## 🔮 Évolutions futures (Étapes 2-7)

- [ ] Interface interactive pour valider/corriger les résultats
- [ ] Ajout automatique à Zotero via API
- [ ] Support d'ISBN pour les livres
- [ ] Traitement par lot de plusieurs fichiers
- [ ] Cache local pour éviter requêtes API redondantes
- [ ] Export vers BibTeX/CSL-JSON

## 📝 Notes

- **Confidentialité** : Toutes les APIs utilisées sont publiques et gratuites
- **LLM local** : Vos notes ne quittent jamais votre machine (Ollama est local)
- **Pas de modification** : Le script ne modifie JAMAIS vos fichiers .md originaux
- **Format des tags** : Seuls les tags `%% #reflitterature ... %%` sont traités

## 📞 Support

Pour toute question ou problème :
1. Vérifiez la section "Dépannage" ci-dessus
2. Vérifiez que tous les prérequis sont installés
3. Consultez les logs d'erreur dans le terminal

## 📜 Licence

Libre d'utilisation pour vos travaux académiques en humanités digitales.