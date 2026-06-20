def build_prompt(code: str, sast_results: dict) -> str:
    """Construit le prompt structuré pour Qwen2.5-Coder"""

    pylint_issues = sast_results.get("pylint", [])
    bandit_issues = sast_results.get("bandit", [])
    semgrep_issues = sast_results.get("semgrep", [])

    # Formater les résultats Pylint
    pylint_text = ""
    for i in pylint_issues:
        if "error" not in i:
            pylint_text += f"  - Ligne {i.get('line')}: [{i.get('type')}] {i.get('message')} ({i.get('symbol')})\n"

    # Formater les résultats Bandit
    bandit_text = ""
    for i in bandit_issues:
        if "error" not in i:
            bandit_text += f"  - Ligne {i.get('line')}: {i.get('message')} [Sévérité: {i.get('severity')}, Confiance: {i.get('confidence')}]\n"

    # Formater les résultats Semgrep
    semgrep_text = ""
    for i in semgrep_issues:
        if "error" not in i:
            semgrep_text += f"  - Ligne {i.get('line')}: {i.get('message')} [Sévérité: {i.get('severity')}]\n"

    prompt = f"""Tu es un expert en sécurité et qualité logicielle Python. 
Analyse le code suivant et les résultats des outils d'analyse statique, puis génère un rapport détaillé en français.

=== CODE SOURCE ===
{code}

=== RÉSULTATS PYLINT (Qualité du code) ===
{pylint_text if pylint_text else "Aucun problème détecté."}

=== RÉSULTATS BANDIT (Sécurité) ===
{bandit_text if bandit_text else "Aucun problème détecté."}

=== RÉSULTATS SEMGREP (Patterns dangereux) ===
{semgrep_text if semgrep_text else "Aucun problème détecté."}

=== INSTRUCTIONS ===
Génère un rapport structuré avec :
1. RÉSUMÉ EXÉCUTIF : synthèse globale en 3-4 phrases
2. VULNÉRABILITÉS CRITIQUES : liste des problèmes de sécurité prioritaires avec explication claire
3. PROBLÈMES DE QUALITÉ : problèmes de style et maintenabilité
4. RECOMMANDATIONS : corrections concrètes pour chaque problème critique
5. SCORE DE SÉCURITÉ : note sur 10 avec justification

Sois précis, pédagogique et donne des exemples de code corrigé pour les vulnérabilités critiques.
"""
    return prompt
