"""
Configuration pour l'enrichisseur bibliographique
COPIEZ CE FICHIER vers config.py et remplissez vos valeurs
"""

# ===== CHEMINS =====
# Chemin vers le dossier contenant vos fichiers .md
VAULT_PATH = ".."  # Dossier parent (le vault Obsidian)

# Nom du fichier contenant la bibliographie complète
BIBLIO_FILE = "4.4 Bibliographic references.md"

# ===== OLLAMA =====
# URL de votre instance Ollama locale
OLLAMA_URL = "http://localhost:11434"

# Modèle LLM à utiliser (assurez-vous de l'avoir téléchargé avec 'ollama pull')
OLLAMA_MODEL = "llama3.1:8b"

# ===== APIS EXTERNES =====
# OpenAlex : API gratuite, pas de clé nécessaire par défaut
# Mais vous pouvez vous inscrire pour des quotas plus élevés
OPENALEX_EMAIL = None  # Optionnel : votre email pour être poli avec l'API
# Exemple : OPENALEX_EMAIL = "votre.email@exemple.com"

# CrossRef : API gratuite en backup
# Pas de clé requise, mais recommandé de fournir un email
CROSSREF_EMAIL = None  # Optionnel
# Exemple : CROSSREF_EMAIL = "votre.email@exemple.com"

# ===== PARAMETRES DE RECHERCHE =====
# Nombre de lignes de contexte autour d'une référence
CONTEXT_LINES = 3

# Score de confiance minimum pour afficher un résultat (0.0 à 1.0)
MIN_CONFIDENCE_SCORE = 0.5

# ===== SORTIE =====
# Dossier pour sauvegarder les résultats
OUTPUT_DIR = "results"

# Format de sortie : 'json', 'markdown', ou 'both'
OUTPUT_FORMAT = "both"
