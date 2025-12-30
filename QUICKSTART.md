# 🚀 Démarrage rapide

## 📦 Installation (5 minutes)

### 1. Installer Ollama

**Linux** :
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Mac** :
Téléchargez depuis https://ollama.com/download

**Vérifier** :
```bash
ollama --version
```

### 2. Télécharger le modèle LLM

```bash
ollama pull llama3.1
```
(Cela prend quelques minutes, ~4 GB)

### 3. Démarrer Ollama

```bash
ollama serve
```
Laissez cette fenêtre de terminal ouverte en arrière-plan.

### 4. Installer les dépendances Python

Dans un **nouveau terminal** :

```bash
cd /chemin/vers/votre/vault/biblio-enricher

# Installer les dépendances
pip install -r requirements.txt
```

## ▶️ Première utilisation

### Test rapide

```bash
python agent.py "1.2 The impact of digitalisation on intellectual life.md"
```

Vous devriez voir :
```
============================================================
📚 ENRICHISSEUR BIBLIOGRAPHIQUE POUR OBSIDIAN
============================================================
📖 Scan du fichier: 1.2 The impact...md
   ✓ 4 référence(s) #reflitterature trouvée(s)

🔍 Traitement de 4 référence(s)...
...
✅ TRAITEMENT TERMINÉ
```

### Consulter les résultats

Ouvrez le fichier généré dans `results/` :
- `*_report.md` → Lisible dans Obsidian
- `*.json` → Pour traitement automatisé

## 📧 Configuration des APIs (optionnel)

Les APIs OpenAlex et CrossRef sont **gratuites et sans clé**.

Pour améliorer les quotas, ajoutez votre email dans `config.py` :

```python
OPENALEX_EMAIL = "votre.email@exemple.com"
CROSSREF_EMAIL = "votre.email@exemple.com"
```

**Aucune inscription requise !** Les APIs sont totalement ouvertes.

## 🎯 Utilisation quotidienne

1. **Démarrer Ollama** (si pas déjà lancé) :
   ```bash
   ollama serve
   ```

2. **Lancer l'enrichissement** :
   ```bash
   python agent.py "votre_fichier.md"
   ```

3. **Consulter** `results/` dans Obsidian

## 🔄 Copier vers un autre vault

1. Copiez le dossier `biblio-enricher/` complet
2. Ajustez `config.py` → `BIBLIO_FILE` si nécessaire
3. C'est tout ! (les dépendances sont déjà installées)

## ❓ Problèmes courants

### "Ollama not found"
→ Assurez-vous qu'Ollama tourne : `ollama serve`

### "Model not found"
→ Téléchargez le modèle : `ollama pull llama3.1`

### "No module named 'requests'"
→ Installez les dépendances : `pip install -r requirements.txt`

### Aucune référence trouvée
→ Vérifiez le format : `%% #reflitterature description %%`

## 📚 Exemple de workflow

```bash
# 1. Démarrer Ollama (une fois au début de votre session)
ollama serve &

# 2. Traiter plusieurs fichiers
python agent.py "1.2 The impact of digitalisation.md"
python agent.py "2.3 The world of open materials.md"

# 3. Consulter tous les rapports dans results/
ls results/*.md
```

## 🎓 Prochaines étapes

Une fois familiarisé avec l'Étape 1 :
- Étape 2 : Validation interactive des résultats
- Étape 3 : Intégration avec Zotero
- Étape 4 : Traitement par lots

---

**Besoin d'aide ?** Consultez le README.md complet pour plus de détails.
