#!/usr/bin/env python3
"""
Agent Git automatique pour publication du projet
Ignore les sources .md, secrets et clés API
"""

import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime


class GitPublisher:
    """Automatise la publication Git avec vérifications de sécurité"""

    def __init__(self):
        self.root = Path(__file__).parent
        self.repo_url = "https://github.com/gbottazzoli/assistant_enrichissement_refLitterature"
        self.sensitive_patterns = [
            r'password\s*=\s*["\'].+["\']',
            r'api[_-]?key\s*=\s*["\'].+["\']',
            r'secret\s*=\s*["\'].+["\']',
            r'token\s*=\s*["\'].+["\']',
            r'[a-zA-Z0-9]{32,}',  # Chaînes longues (possibles clés)
        ]

    def run_cmd(self, cmd: list, check=True) -> subprocess.CompletedProcess:
        """Execute commande shell"""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.root,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur commande: {' '.join(cmd)}")
            print(f"   {e.stderr}")
            if check:
                sys.exit(1)
            return e

    def check_git_installed(self):
        """Vérifie que Git est installé"""
        result = self.run_cmd(['git', '--version'], check=False)
        if result.returncode != 0:
            print("❌ Git n'est pas installé")
            sys.exit(1)

    def init_repo_if_needed(self):
        """Initialise le repo si nécessaire"""
        git_dir = self.root / '.git'
        if not git_dir.exists():
            print("📦 Initialisation du repository Git...")
            self.run_cmd(['git', 'init'])
            self.run_cmd(['git', 'remote', 'add', 'origin', self.repo_url])
            print(f"✓ Repository initialisé avec remote: {self.repo_url}")
        else:
            # Vérifier que l'URL remote est correcte
            result = self.run_cmd(['git', 'remote', 'get-url', 'origin'], check=False)
            if result.returncode == 0:
                current_url = result.stdout.strip()
                if current_url != self.repo_url:
                    print(f"⚠️  URL remote différente: {current_url}")
                    response = input(f"Mettre à jour vers {self.repo_url} ? (y/n): ")
                    if response.lower() == 'y':
                        self.run_cmd(['git', 'remote', 'set-url', 'origin', self.repo_url])
                        print("✓ URL remote mise à jour")
            else:
                # Pas de remote, l'ajouter
                self.run_cmd(['git', 'remote', 'add', 'origin', self.repo_url])

    def ensure_gitignore(self):
        """Vérifie que .gitignore existe"""
        gitignore = self.root / '.gitignore'
        if not gitignore.exists():
            print("❌ .gitignore manquant!")
            sys.exit(1)
        print("✓ .gitignore présent")

    def check_for_secrets(self):
        """Vérifie qu'aucun secret n'est dans les fichiers stagés"""
        # Liste des fichiers à committer
        result = self.run_cmd(['git', 'diff', '--cached', '--name-only'])
        files = result.stdout.strip().split('\n')

        if not files or files == ['']:
            return True

        print("🔍 Vérification des secrets...")
        secrets_found = False

        for file in files:
            filepath = self.root / file
            if not filepath.exists() or not filepath.is_file():
                continue

            # Ignorer les binaires et non-texte
            if filepath.suffix in ['.pyc', '.so', '.png', '.jpg', '.pdf']:
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                for pattern in self.sensitive_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        print(f"⚠️  Secret potentiel détecté dans: {file}")
                        print(f"   Pattern: {pattern}")
                        secrets_found = True
            except:
                # Fichier non lisible, ignorer
                pass

        if secrets_found:
            response = input("\n⚠️  Des secrets potentiels ont été détectés. Continuer quand même ? (y/n): ")
            if response.lower() != 'y':
                print("❌ Publication annulée")
                sys.exit(1)

        print("✓ Aucun secret détecté")
        return True

    def get_status(self) -> str:
        """Récupère le statut Git"""
        result = self.run_cmd(['git', 'status', '--short'])
        return result.stdout

    def stage_files(self):
        """Stage les fichiers selon .gitignore"""
        print("📝 Staging des fichiers...")

        # Ajouter tous les fichiers (gitignore fait le filtrage)
        self.run_cmd(['git', 'add', '.'])

        # Vérifier ce qui est stagé
        result = self.run_cmd(['git', 'diff', '--cached', '--name-only'])
        staged = result.stdout.strip()

        if not staged:
            print("⚠️  Aucun fichier à committer")
            return False

        print("✓ Fichiers stagés:")
        for file in staged.split('\n'):
            print(f"   + {file}")

        return True

    def create_commit(self, message: str = None):
        """Crée un commit"""
        if message is None:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            message = f"Auto-update: {timestamp}"

        print(f"\n💬 Message de commit: {message}")

        self.run_cmd(['git', 'commit', '-m', message])
        print("✓ Commit créé")

    def push_to_remote(self, branch: str = 'main'):
        """Push vers le remote"""
        print(f"\n🚀 Push vers {self.repo_url}...")

        # Vérifier si la branche existe
        result = self.run_cmd(['git', 'branch', '--show-current'])
        current_branch = result.stdout.strip()

        if not current_branch:
            # Pas de branche, créer main
            self.run_cmd(['git', 'branch', '-M', branch])
            current_branch = branch

        # Premier push peut nécessiter -u
        result = self.run_cmd(['git', 'push', '-u', 'origin', current_branch], check=False)

        if result.returncode != 0:
            print("❌ Erreur lors du push")
            print(f"   {result.stderr}")
            print("\n💡 Vérifiez:")
            print("   1. Que vous avez accès au repo")
            print("   2. Vos credentials Git sont configurés")
            print("   3. Le repo existe sur GitHub")
            sys.exit(1)

        print(f"✓ Push réussi vers {current_branch}")

    def show_summary(self):
        """Affiche un résumé"""
        result = self.run_cmd(['git', 'log', '-1', '--oneline'])
        last_commit = result.stdout.strip()

        print("\n" + "=" * 60)
        print("✅ PUBLICATION RÉUSSIE")
        print("=" * 60)
        print(f"Repository: {self.repo_url}")
        print(f"Dernier commit: {last_commit}")
        print()


def main():
    """Point d'entrée"""
    print("=" * 60)
    print("🤖 AGENT GIT - PUBLICATION AUTOMATIQUE")
    print("=" * 60)
    print()

    publisher = GitPublisher()

    # Vérifications préliminaires
    publisher.check_git_installed()
    publisher.ensure_gitignore()
    publisher.init_repo_if_needed()

    # Afficher le statut
    status = publisher.get_status()
    if status:
        print("📊 Statut actuel:")
        print(status)
    else:
        print("✓ Working directory clean")
        response = input("\nAucun changement détecté. Continuer quand même ? (y/n): ")
        if response.lower() != 'y':
            print("Annulé")
            sys.exit(0)

    # Message de commit personnalisé ?
    print("\n💬 Message de commit:")
    print("   Appuyez sur Entrée pour message auto, ou tapez votre message")
    custom_message = input("> ").strip()

    # Stage des fichiers
    if not publisher.stage_files():
        print("Rien à publier")
        sys.exit(0)

    # Vérification des secrets
    publisher.check_for_secrets()

    # Confirmation finale
    print("\n⚠️  Prêt à publier sur GitHub")
    response = input("Confirmer ? (y/n): ")
    if response.lower() != 'y':
        print("❌ Publication annulée")
        sys.exit(0)

    # Commit et push
    publisher.create_commit(custom_message if custom_message else None)
    publisher.push_to_remote()

    # Résumé
    publisher.show_summary()


if __name__ == "__main__":
    main()
