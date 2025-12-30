# 🚀 Configuration Git et Publication

## ⚠️ Avant la première publication

### 1. Créer le repository sur GitHub

1. Allez sur https://github.com/gbottazzoli
2. Cliquez sur "New repository"
3. Nom: `assistant_enrichissement_refLitterature`
4. Description: "Agent Python pour enrichir notes bibliographiques avec DOI et métadonnées (Ollama + OpenAlex + CrossRef)"
5. **Public** ou **Private** selon votre choix
6. **Ne cochez pas** "Initialize with README" (on a déjà les fichiers)
7. Cliquez "Create repository"

### 2. Configurer vos credentials Git (si pas déjà fait)

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@exemple.com"
```

### 3. Configurer l'authentification GitHub

**Option A : Token personnel (recommandé)**

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Cochez `repo` (accès complet aux repos)
4. Générer et copier le token
5. À la première publication, utilisez le token comme mot de passe

**Option B : SSH (plus sécurisé)**

```bash
ssh-keygen -t ed25519 -C "votre.email@exemple.com"
cat ~/.ssh/id_ed25519.pub  # Copier cette clé
```

Puis ajoutez la clé publique dans GitHub → Settings → SSH keys

Si SSH, modifiez l'URL dans `git_publish.py` ligne 16:
```python
self.repo_url = "git@github.com:gbottazzoli/assistant_enrichissement_refLitterature.git"
```

## 📦 Publication automatique

### Commande simple

```bash
python3 git_publish.py
```

### Ce que fait le script

1. ✅ Vérifie que Git est installé
2. ✅ Vérifie que `.gitignore` existe
3. ✅ Initialise le repo si nécessaire
4. ✅ Configure le remote GitHub
5. ✅ Affiche le statut des fichiers
6. ✅ Stage les fichiers (selon `.gitignore`)
7. ✅ **Scanne les secrets potentiels** (clés API, passwords)
8. ✅ Demande confirmation
9. ✅ Crée le commit
10. ✅ Push vers GitHub

### Fichiers ignorés (ne seront PAS publiés)

- ❌ `config.py` (contient vos chemins/emails)
- ❌ `results/` (vos résultats d'analyse)
- ❌ `../*.md` (les fichiers de votre vault)
- ❌ `*.json` sauf `project_state.json`
- ❌ `__pycache__/`, `.env`, etc.

### Fichiers publiés (seront sur GitHub)

- ✅ `agent.py` (code principal)
- ✅ `config.example.py` (template de config)
- ✅ `requirements.txt`
- ✅ `README.md`, `TODO.md`, `PROJECT_STATE.md`
- ✅ Tous les fichiers `.md` de documentation
- ✅ `project_state.py`, `git_publish.py`
- ✅ `project_state.json` (état du projet)

## 🔒 Sécurité

### Le script détecte automatiquement

- Patterns `password = "..."`
- Patterns `api_key = "..."`
- Patterns `secret = "..."`
- Chaînes longues suspectes (possibles tokens)

Si détecté → Demande confirmation avant de continuer

### Vérification manuelle

Avant publication, vérifiez manuellement :

```bash
# Voir ce qui sera commité
git diff --cached

# Voir les fichiers stagés
git diff --cached --name-only
```

## 📝 Workflow de publication

### Première fois

```bash
# 1. Créer le repo sur GitHub (voir ci-dessus)

# 2. Copier config.py depuis example
cp config.example.py config.py
# Éditer config.py avec vos valeurs

# 3. Publier
python3 git_publish.py
```

### Mises à jour régulières

```bash
# 1. Mettre à jour la doc projet
python3 project_state.py

# 2. Publier
python3 git_publish.py
```

## 🛠️ Commandes Git manuelles (si besoin)

```bash
# Initialiser
git init
git remote add origin https://github.com/gbottazzoli/assistant_enrichissement_refLitterature

# Vérifier statut
git status

# Voir ce qui est ignoré
git status --ignored

# Commit manuel
git add .
git commit -m "Votre message"
git push -u origin main

# Voir l'historique
git log --oneline

# Annuler un commit (avant push)
git reset --soft HEAD~1
```

## ⚠️ Problèmes courants

### "Permission denied"
→ Vérifiez vos credentials (token ou SSH)

### "Repository not found"
→ Vérifiez que le repo existe sur GitHub et que l'URL est correcte

### "Nothing to commit"
→ Aucun changement détecté, normal si vous venez de publier

### "Divergent branches"
→ Quelqu'un a modifié le repo depuis votre dernier pull
```bash
git pull --rebase origin main
```

### Secrets détectés à tort
→ C'est un faux positif, confirmez quand le script demande

## 📚 Ressources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---

**Important** : Ne commitez JAMAIS `config.py` avec vos vraies valeurs !
