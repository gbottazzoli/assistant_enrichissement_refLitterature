#!/bin/bash
# Script de reprise du projet pour nouvelle session Claude Code
# À lancer en début de conversation pour mettre à jour la documentation

echo "=========================================="
echo "🔄 REPRISE DU PROJET - Documentation"
echo "=========================================="
echo

# 1. Mettre à jour l'état du projet
echo "📊 Mise à jour de l'état du projet..."
python3 project_state.py

echo
echo "=========================================="
echo "✅ PROJET PRÊT"
echo "=========================================="
echo
echo "📄 Fichiers mis à jour pour Claude Code :"
echo "   - PROJECT_STATE.md (état complet du projet)"
echo "   - project_state.json (données structurées)"
echo "   - README.md (stats actualisées)"
echo
echo "💡 Instructions pour Claude Code :"
echo "   1. Lis PROJECT_STATE.md"
echo "   2. Lis TODO.md pour la roadmap"
echo "   3. Tu es prêt à développer"
echo
