#!/usr/bin/env python3
"""
Agent de maintenance de documentation projet
Génère un état complet du projet pour développement futur
"""

import os
import re
import json
import ast
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import subprocess


class ProjectStateGenerator:
    """Génère l'état complet du projet"""

    def __init__(self, project_root: str = "."):
        self.root = Path(project_root).resolve()
        self.state = {
            'timestamp': datetime.now().isoformat(),
            'project_name': 'biblio-enricher',
            'version': '0.1.0',
            'files': {},
            'functions': {},
            'classes': {},
            'dependencies': {},
            'config': {},
            'stats': {}
        }

    def scan_project(self):
        """Scan complet du projet"""
        print("🔍 Scanning project structure...")
        self._scan_python_files()
        self._scan_config()
        self._scan_dependencies()
        self._scan_documentation()
        self._calculate_stats()
        print("✓ Scan complete")

    def _scan_python_files(self):
        """Scanne tous les fichiers Python"""
        for py_file in self.root.glob("*.py"):
            if py_file.name == 'project_state.py':
                continue

            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)

            file_info = {
                'path': str(py_file),
                'lines': len(content.splitlines()),
                'functions': [],
                'classes': [],
                'imports': []
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node)
                    }
                    file_info['functions'].append(func_info)
                    self.state['functions'][f"{py_file.stem}.{node.name}"] = func_info

                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        'docstring': ast.get_docstring(node)
                    }
                    file_info['classes'].append(class_info)
                    self.state['classes'][f"{py_file.stem}.{node.name}"] = class_info

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        file_info['imports'].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        file_info['imports'].append(node.module)

            self.state['files'][py_file.name] = file_info

    def _scan_config(self):
        """Extrait la configuration"""
        config_file = self.root / 'config.py'
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extraire les variables de config
            for line in content.splitlines():
                if '=' in line and not line.strip().startswith('#'):
                    match = re.match(r'^([A-Z_]+)\s*=\s*(.+)', line)
                    if match:
                        key, value = match.groups()
                        self.state['config'][key] = value.strip()

    def _scan_dependencies(self):
        """Liste les dépendances"""
        req_file = self.root / 'requirements.txt'
        if req_file.exists():
            with open(req_file, 'r', encoding='utf-8') as f:
                deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            self.state['dependencies'] = {
                'requirements': deps,
                'count': len(deps)
            }

    def _scan_documentation(self):
        """Scanne la documentation existante"""
        docs = {}
        for doc_file in self.root.glob("*.md"):
            docs[doc_file.name] = {
                'path': str(doc_file),
                'size': doc_file.stat().st_size,
                'lines': len(doc_file.read_text(encoding='utf-8').splitlines())
            }

        for doc_file in self.root.glob("*.txt"):
            docs[doc_file.name] = {
                'path': str(doc_file),
                'size': doc_file.stat().st_size,
                'lines': len(doc_file.read_text(encoding='utf-8').splitlines())
            }

        self.state['documentation'] = docs

    def _calculate_stats(self):
        """Calcule les statistiques du projet"""
        total_lines = sum(f['lines'] for f in self.state['files'].values())
        total_functions = len(self.state['functions'])
        total_classes = len(self.state['classes'])

        self.state['stats'] = {
            'total_python_files': len(self.state['files']),
            'total_lines_of_code': total_lines,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_dependencies': self.state['dependencies'].get('count', 0),
            'documentation_files': len(self.state.get('documentation', {}))
        }

    def generate_markdown_report(self) -> str:
        """Génère le rapport Markdown"""
        md = f"""# 📊 ÉTAT DU PROJET - {self.state['project_name']}

**Généré le** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version** : {self.state['version']}

---

## 📈 Statistiques globales

| Métrique | Valeur |
|----------|--------|
| Fichiers Python | {self.state['stats']['total_python_files']} |
| Lignes de code | {self.state['stats']['total_lines_of_code']} |
| Fonctions | {self.state['stats']['total_functions']} |
| Classes | {self.state['stats']['total_classes']} |
| Dépendances | {self.state['stats']['total_dependencies']} |
| Fichiers de documentation | {self.state['stats']['documentation_files']} |

---

## 🗂️ Structure des fichiers Python

"""
        for filename, info in sorted(self.state['files'].items()):
            md += f"\n### {filename}\n\n"
            md += f"**Lignes** : {info['lines']}\n\n"

            if info['classes']:
                md += "**Classes** :\n"
                for cls in info['classes']:
                    md += f"- `{cls['name']}` (ligne {cls['line']})\n"
                    md += f"  - Méthodes : {', '.join(cls['methods'])}\n"
                md += "\n"

            if info['functions']:
                md += "**Fonctions** :\n"
                for func in info['functions']:
                    args = ', '.join(func['args']) if func['args'] else ''
                    md += f"- `{func['name']}({args})` (ligne {func['line']})\n"
                md += "\n"

            if info['imports']:
                md += f"**Imports** : {', '.join(set(info['imports']))}\n\n"

        md += "\n---\n\n## ⚙️ Configuration actuelle\n\n"
        md += "```python\n"
        for key, value in sorted(self.state['config'].items()):
            md += f"{key} = {value}\n"
        md += "```\n\n"

        md += "---\n\n## 📦 Dépendances\n\n"
        if self.state['dependencies']:
            for dep in self.state['dependencies']['requirements']:
                md += f"- {dep}\n"
        md += "\n"

        md += "---\n\n## 📚 Documentation disponible\n\n"
        for doc_name, doc_info in sorted(self.state.get('documentation', {}).items()):
            md += f"- **{doc_name}** ({doc_info['lines']} lignes)\n"
        md += "\n"

        md += """---

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
"""
        return md

    def save_state(self):
        """Sauvegarde l'état du projet"""
        # Rapport Markdown
        md_report = self.generate_markdown_report()
        state_md = self.root / 'PROJECT_STATE.md'
        with open(state_md, 'w', encoding='utf-8') as f:
            f.write(md_report)
        print(f"✓ État sauvegardé : {state_md}")

        # État JSON (pour traitement automatique)
        state_json = self.root / 'project_state.json'
        with open(state_json, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
        print(f"✓ JSON sauvegardé : {state_json}")

    def update_readme(self):
        """Met à jour le README avec les stats actuelles"""
        readme = self.root / 'README.md'
        if not readme.exists():
            return

        content = readme.read_text(encoding='utf-8')

        # Créer badge de stats
        stats_badge = f"""
<!-- AUTO-GENERATED STATS - DO NOT EDIT -->
**Stats du projet** : {self.state['stats']['total_lines_of_code']} lignes | {self.state['stats']['total_functions']} fonctions | {self.state['stats']['total_classes']} classes
<!-- END AUTO-GENERATED -->
"""

        # Remplacer section auto-générée si existe
        if '<!-- AUTO-GENERATED STATS' in content:
            content = re.sub(
                r'<!-- AUTO-GENERATED STATS.*?END AUTO-GENERATED -->',
                stats_badge.strip(),
                content,
                flags=re.DOTALL
            )
        else:
            # Ajouter après le titre principal
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    lines.insert(i + 2, stats_badge)
                    break
            content = '\n'.join(lines)

        readme.write_text(content, encoding='utf-8')
        print(f"✓ README mis à jour")


def main():
    """Point d'entrée"""
    print("=" * 60)
    print("🤖 AGENT DE MAINTENANCE - DOCUMENTATION PROJET")
    print("=" * 60)
    print()

    generator = ProjectStateGenerator()
    generator.scan_project()
    generator.save_state()
    generator.update_readme()

    print()
    print("=" * 60)
    print("✅ DOCUMENTATION MISE À JOUR")
    print("=" * 60)
    print()
    print("📄 Fichiers générés :")
    print("   - PROJECT_STATE.md (rapport lisible)")
    print("   - project_state.json (données structurées)")
    print()
    print("💡 Pour Claude Code :")
    print("   Lisez PROJECT_STATE.md avant tout nouveau développement")
    print()


if __name__ == "__main__":
    main()
