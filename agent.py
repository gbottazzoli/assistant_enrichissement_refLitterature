#!/usr/bin/env python3
"""
Enrichisseur bibliographique pour notes Obsidian
Scanne les tags #reflitterature et trouve les DOI/métadonnées
"""

import re
import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

try:
    import requests
    import ollama
    from tqdm import tqdm
except ImportError:
    print("❌ Erreur: Certaines dépendances sont manquantes.")
    print("Installez-les avec: pip install -r requirements.txt")
    sys.exit(1)

import config


class BiblioEnricher:
    """Agent pour enrichir les références bibliographiques"""

    def __init__(self, vault_path: str = None):
        """
        Initialise l'enrichisseur

        Args:
            vault_path: Chemin vers le vault Obsidian (par défaut: config.VAULT_PATH)
        """
        self.vault_path = Path(vault_path or config.VAULT_PATH).resolve()
        self.biblio_file = self.vault_path / config.BIBLIO_FILE
        self.output_dir = self.vault_path / config.OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)

        # Vérifier qu'Ollama est accessible
        self._check_ollama()

    def _check_ollama(self):
        """Vérifie que le serveur Ollama est accessible"""
        try:
            response = requests.get(f"{config.OLLAMA_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                if not any(config.OLLAMA_MODEL in name for name in model_names):
                    print(f"⚠️  Warning: Le modèle '{config.OLLAMA_MODEL}' n'est pas installé.")
                    print(f"   Téléchargez-le avec: ollama pull {config.OLLAMA_MODEL}")
            else:
                raise ConnectionError()
        except:
            print(f"⚠️  Warning: Ollama n'est pas accessible à {config.OLLAMA_URL}")
            print("   Assurez-vous qu'Ollama est démarré: ollama serve")

    def scan_file(self, filename: str) -> List[Dict]:
        """
        Scanne un fichier .md pour trouver les tags #reflitterature

        Args:
            filename: Nom du fichier à scanner (avec ou sans .md)

        Returns:
            Liste de dictionnaires contenant les références trouvées
        """
        # Ajouter .md si nécessaire
        if not filename.endswith('.md'):
            filename += '.md'

        filepath = self.vault_path / filename

        if not filepath.exists():
            print(f"❌ Erreur: Le fichier '{filename}' n'existe pas dans {self.vault_path}")
            print(f"\n💡 Astuce: Si le nom contient des espaces, utilisez des guillemets:")
            print(f'   python agent.py "{filename}"')

            # Suggérer des fichiers similaires
            similar = list(self.vault_path.glob(f"*{filename.split()[0]}*.md"))
            if similar:
                print(f"\n📁 Fichiers similaires trouvés:")
                for f in similar[:5]:
                    print(f"   - {f.name}")

            return []

        print(f"📖 Scan du fichier: {filename}")

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        references = []

        # Pattern pour détecter %% #reflitterature description %%
        pattern = r'%%\s*#reflitterature\s+(.+?)\s*%%'

        for line_num, line in enumerate(lines, 1):
            matches = re.finditer(pattern, line)
            for match in matches:
                comment_text = match.group(1).strip()

                # Extraire la citation AVANT le tag (entre == ==)
                # Pattern : ==...citation...== %% #reflitterature
                citation_pattern = r'==(.+?)==\s*%%\s*#reflitterature'
                citation_match = re.search(citation_pattern, line)

                if citation_match:
                    citation_text = citation_match.group(1).strip()
                    # Extraire les citations entre parenthèses (Auteur Année)
                    citation_refs = re.findall(r'\(([^)]+?\d{4}[^)]*)\)', citation_text)
                    ref_text = '; '.join(citation_refs) if citation_refs else citation_text
                else:
                    # Fallback : utiliser le commentaire si pas de citation trouvée
                    ref_text = comment_text

                # Extraire le contexte (lignes autour)
                start_idx = max(0, line_num - 1 - config.CONTEXT_LINES)
                end_idx = min(len(lines), line_num + config.CONTEXT_LINES)
                context = ''.join(lines[start_idx:end_idx])

                references.append({
                    'file': filename,
                    'line': line_num,
                    'raw_text': ref_text,
                    'comment': comment_text,
                    'context': context,
                    'line_text': line.strip()
                })

        print(f"   ✓ {len(references)} référence(s) #reflitterature trouvée(s)")
        return references

    def search_in_bibliography(self, ref_text: str) -> Optional[str]:
        """
        Cherche une référence complète dans le fichier bibliographie

        Args:
            ref_text: Texte de la référence à chercher (format: "Auteur Année" ou "Auteur et Auteur Année")

        Returns:
            La référence complète si trouvée, None sinon
        """
        if not self.biblio_file.exists():
            return None

        with open(self.biblio_file, 'r', encoding='utf-8') as f:
            biblio_content = f.read()

        # Extraire tous les auteurs et années de la citation
        # Format : "Habermas 2021, Habermas 1992" ou "Anderson and Rainie 2017"

        # Extraire les années
        years = re.findall(r'\b(19|20)\d{2}\b', ref_text)

        # Extraire les noms d'auteur (mots commençant par une majuscule)
        authors = re.findall(r'\b([A-Z][a-zà-ÿ]+)', ref_text)
        # Filtrer les mots comme "and", "et"
        authors = [a for a in authors if a.lower() not in ['and', 'et', 'the', 'de', 'du', 'la', 'le']]

        if not (authors and years):
            return None

        # Chercher dans la bibliographie
        lines = biblio_content.split('\n')
        best_match = None
        max_matches = 0

        for i, line in enumerate(lines):
            # Compter les matchs (auteurs + année)
            matches = sum(1 for author in authors if author in line)
            matches += sum(1 for year in years if year in line)

            if matches > max_matches:
                max_matches = matches
                # Retourner cette ligne et éventuellement les suivantes
                full_ref = line
                j = i + 1
                while j < len(lines) and lines[j].strip() and not lines[j].startswith('\n'):
                    full_ref += ' ' + lines[j].strip()
                    j += 1
                best_match = full_ref.strip()

        return best_match if max_matches >= 2 else None

    def extract_metadata_with_llm(self, ref_text: str, full_ref: Optional[str] = None) -> Dict:
        """
        Utilise Ollama pour extraire les métadonnées d'une référence
        Gère les erreurs OCR et formate les données

        Args:
            ref_text: Texte brut de la référence
            full_ref: Référence complète depuis bibliographie (optionnel)

        Returns:
            Dictionnaire avec auteur, titre, année extraits
        """
        # Texte à analyser (priorité à la référence complète)
        text_to_analyze = full_ref if full_ref else ref_text

        prompt = f"""Tu es un assistant bibliographique. Analyse cette référence et extrais les informations suivantes.
Note : la référence peut contenir des erreurs OCR (caractères mal reconnus).

Référence: {text_to_analyze}

Extrais et retourne UNIQUEMENT un objet JSON avec ce format exact:
{{
  "author": "Nom de l'auteur principal (format: Nom, Prénom)",
  "title": "Titre complet de l'ouvrage ou article",
  "year": "Année de publication (nombre à 4 chiffres)",
  "confidence": 0.85
}}

Le champ confidence doit être entre 0 et 1 selon ta certitude (1 = très sûr, 0.5 = incertain).
NE retourne QUE le JSON, sans texte avant ou après."""

        try:
            # Appel à Ollama
            response = ollama.chat(
                model=config.OLLAMA_MODEL,
                messages=[{'role': 'user', 'content': prompt}]
            )

            # Parser la réponse JSON
            response_text = response['message']['content'].strip()

            # Nettoyer la réponse (parfois le LLM ajoute des backticks)
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)

            metadata = json.loads(response_text)

            # Validation basique
            if not all(k in metadata for k in ['author', 'title', 'year']):
                raise ValueError("Champs manquants dans la réponse")

            return metadata

        except Exception as e:
            print(f"   ⚠️  Erreur LLM: {e}")
            # Retour par défaut en cas d'erreur
            return {
                'author': 'Unknown',
                'title': ref_text[:100],
                'year': 'Unknown',
                'confidence': 0.0
            }

    def search_openalex(self, author: str, title: str, year: str) -> Optional[Dict]:
        """
        Recherche dans OpenAlex (API gratuite prioritaire)

        Args:
            author, title, year: Métadonnées extraites

        Returns:
            Informations bibliographiques avec DOI si trouvé
        """
        base_url = "https://api.openalex.org/works"

        # Construire la requête de recherche
        # OpenAlex utilise un format de requête spécifique
        query = f"{title} {author} {year}".strip()

        params = {
            'search': query,
            'per_page': 5  # Limiter à 5 résultats
        }

        # Ajouter email si configuré (pour être poli avec l'API)
        if config.OPENALEX_EMAIL:
            params['mailto'] = config.OPENALEX_EMAIL

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data['results']:
                # Prendre le premier résultat (le plus pertinent)
                work = data['results'][0]

                # Calculer un score de confiance basique
                # (comparaison titre + année)
                title_similarity = self._similarity_score(
                    title.lower(),
                    work.get('title', '').lower()
                )
                year_match = str(year) in str(work.get('publication_year', ''))

                confidence = title_similarity * (1.2 if year_match else 0.8)
                confidence = min(confidence, 1.0)

                return {
                    'source': 'OpenAlex',
                    'doi': work.get('doi', '').replace('https://doi.org/', ''),
                    'title': work.get('title'),
                    'authors': [a.get('author', {}).get('display_name')
                               for a in work.get('authorships', [])],
                    'year': work.get('publication_year'),
                    'url': work.get('doi') or work.get('id'),
                    'confidence': confidence
                }

        except Exception as e:
            print(f"   ⚠️  Erreur OpenAlex: {e}")

        return None

    def search_crossref(self, author: str, title: str, year: str) -> Optional[Dict]:
        """
        Recherche dans CrossRef (API de backup)

        Args:
            author, title, year: Métadonnées extraites

        Returns:
            Informations bibliographiques avec DOI si trouvé
        """
        base_url = "https://api.crossref.org/works"

        query = f"{title} {author} {year}".strip()

        params = {
            'query': query,
            'rows': 5
        }

        headers = {}
        if config.CROSSREF_EMAIL:
            headers['User-Agent'] = f"BiblioEnricher/1.0 (mailto:{config.CROSSREF_EMAIL})"

        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data['message']['items']:
                item = data['message']['items'][0]

                # Score de confiance
                title_similarity = self._similarity_score(
                    title.lower(),
                    ' '.join(item.get('title', [''])).lower()
                )
                year_match = str(year) == str(item.get('published-print', {}).get('date-parts', [[None]])[0][0])

                confidence = title_similarity * (1.2 if year_match else 0.8)
                confidence = min(confidence, 1.0)

                authors = [f"{a.get('family', '')}, {a.get('given', '')}"
                          for a in item.get('author', [])]

                return {
                    'source': 'CrossRef',
                    'doi': item.get('DOI'),
                    'title': ' '.join(item.get('title', [])),
                    'authors': authors,
                    'year': item.get('published-print', {}).get('date-parts', [[None]])[0][0],
                    'url': f"https://doi.org/{item.get('DOI')}",
                    'confidence': confidence
                }

        except Exception as e:
            print(f"   ⚠️  Erreur CrossRef: {e}")

        return None

    def _similarity_score(self, str1: str, str2: str) -> float:
        """
        Calcul de similarité simple entre deux chaînes
        (Ratio de mots communs)
        """
        if not str1 or not str2:
            return 0.0

        words1 = set(str1.lower().split())
        words2 = set(str2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def process_references(self, references: List[Dict]) -> List[Dict]:
        """
        Traite une liste de références et enrichit avec métadonnées

        Args:
            references: Liste de références extraites du fichier

        Returns:
            Liste enrichie avec DOI et métadonnées
        """
        enriched = []

        print(f"\n🔍 Traitement de {len(references)} référence(s)...")

        for ref in tqdm(references, desc="Enrichissement"):
            # 1. Chercher dans bibliographie
            full_ref = self.search_in_bibliography(ref['raw_text'])
            if full_ref:
                print(f"\n   ✓ Référence complète trouvée dans bibliographie")

            # 2. Extraire métadonnées avec LLM
            metadata = self.extract_metadata_with_llm(ref['raw_text'], full_ref)

            # 3. Chercher DOI (OpenAlex prioritaire, puis CrossRef)
            api_result = None
            if metadata['author'] != 'Unknown':
                api_result = self.search_openalex(
                    metadata['author'],
                    metadata['title'],
                    metadata['year']
                )

                if not api_result or api_result['confidence'] < config.MIN_CONFIDENCE_SCORE:
                    api_result = self.search_crossref(
                        metadata['author'],
                        metadata['title'],
                        metadata['year']
                    )

            # 4. Combiner les résultats
            enriched_ref = {
                **ref,
                'extracted_metadata': metadata,
                'full_reference': full_ref,
                'api_result': api_result,
                'final_confidence': api_result['confidence'] if api_result else metadata.get('confidence', 0.0)
            }

            enriched.append(enriched_ref)

        return enriched

    def save_results(self, results: List[Dict], source_file: str):
        """
        Sauvegarde les résultats dans le dossier de sortie

        Args:
            results: Résultats enrichis
            source_file: Nom du fichier source
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(source_file).stem

        # JSON
        if config.OUTPUT_FORMAT in ['json', 'both']:
            json_file = self.output_dir / f"{base_name}_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Résultats JSON: {json_file}")

        # Markdown
        if config.OUTPUT_FORMAT in ['markdown', 'both']:
            md_file = self.output_dir / f"{base_name}_{timestamp}_report.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"# Rapport d'enrichissement bibliographique\n\n")
                f.write(f"**Fichier source**: {source_file}\n")
                f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Références trouvées**: {len(results)}\n\n")
                f.write("---\n\n")

                for i, ref in enumerate(results, 1):
                    f.write(f"## Référence {i}\n\n")
                    f.write(f"**Ligne {ref['line']}**: {ref['raw_text']}\n\n")

                    if ref['full_reference']:
                        f.write(f"**Référence complète**:\n> {ref['full_reference']}\n\n")

                    meta = ref['extracted_metadata']
                    f.write(f"**Métadonnées extraites**:\n")
                    f.write(f"- Auteur: {meta['author']}\n")
                    f.write(f"- Titre: {meta['title']}\n")
                    f.write(f"- Année: {meta['year']}\n\n")

                    if ref['api_result']:
                        api = ref['api_result']
                        f.write(f"**Résultat API ({api['source']})**:\n")
                        f.write(f"- DOI: `{api['doi']}`\n")
                        f.write(f"- URL: {api['url']}\n")
                        f.write(f"- Score de confiance: {api['confidence']:.2%}\n\n")
                    else:
                        f.write(f"⚠️ *Aucun DOI trouvé*\n\n")

                    f.write("---\n\n")

            print(f"📄 Rapport Markdown: {md_file}")


def main():
    """Point d'entrée principal du script"""

    print("=" * 60)
    print("📚 ENRICHISSEUR BIBLIOGRAPHIQUE POUR OBSIDIAN")
    print("=" * 60)

    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("\n❌ Usage: python agent.py <nom_du_fichier.md>")
        print("\nExemple: python agent.py '1.2 The impact of digitalisation on intellectual life.md'")
        print("\n💡 Astuce: Utilisez des guillemets si le nom contient des espaces!")
        sys.exit(1)

    # Joindre tous les arguments (pour gérer les noms avec espaces même sans guillemets)
    target_file = ' '.join(sys.argv[1:])

    # Initialiser l'agent
    enricher = BiblioEnricher()

    # Scanner le fichier
    references = enricher.scan_file(target_file)

    if not references:
        print("\n✓ Aucune référence #reflitterature trouvée dans ce fichier.")
        sys.exit(0)

    # Traiter les références
    enriched = enricher.process_references(references)

    # Sauvegarder les résultats
    enricher.save_results(enriched, target_file)

    # Résumé
    print("\n" + "=" * 60)
    print("✅ TRAITEMENT TERMINÉ")
    print("=" * 60)
    with_doi = sum(1 for r in enriched if r['api_result'])
    print(f"Références traitées: {len(enriched)}")
    print(f"DOI trouvés: {with_doi}/{len(enriched)}")
    print(f"Taux de réussite: {with_doi/len(enriched)*100:.1f}%" if enriched else "N/A")


if __name__ == "__main__":
    main()
