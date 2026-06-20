import subprocess
import json
import os

def run_pylint(filepath):
    """Lance Pylint sur le fichier et retourne les résultats"""
    try:
        result = subprocess.run(
            ["pylint", filepath, "--output-format=json", "--score=no"],
            capture_output=True, text=True
        )
        issues = json.loads(result.stdout) if result.stdout.strip() else []
        return [
            {
                "tool": "pylint",
                "line": i.get("line"),
                "message": i.get("message"),
                "symbol": i.get("symbol"),
                "type": i.get("type")
            }
            for i in issues
        ]
    except Exception as e:
        return [{"tool": "pylint", "error": str(e)}]


def run_bandit(filepath):
    """Lance Bandit sur le fichier et retourne les résultats"""
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", "-q", filepath],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout) if result.stdout.strip() else {}
        issues = data.get("results", [])
        return [
            {
                "tool": "bandit",
                "line": i.get("line_number"),
                "message": i.get("issue_text"),
                "severity": i.get("issue_severity"),
                "confidence": i.get("issue_confidence")
            }
            for i in issues
        ]
    except Exception as e:
        return [{"tool": "bandit", "error": str(e)}]


def run_semgrep(filepath):
    """Lance Semgrep sur le fichier et retourne les résultats"""
    try:
        result = subprocess.run(
            ["semgrep", "--config=auto", "--json", filepath],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout) if result.stdout.strip() else {}
        issues = data.get("results", [])
        return [
            {
                "tool": "semgrep",
                "line": i.get("start", {}).get("line"),
                "message": i.get("extra", {}).get("message"),
                "severity": i.get("extra", {}).get("severity")
            }
            for i in issues
        ]
    except Exception as e:
        return [{"tool": "semgrep", "error": str(e)}]


def analyze(filepath):
    """Lance les 3 outils SAST et retourne les résultats agrégés"""
    if not os.path.exists(filepath):
        return {"error": f"Fichier introuvable : {filepath}"}

    pylint_results = run_pylint(filepath)
    bandit_results = run_bandit(filepath)
    semgrep_results = run_semgrep(filepath)

    all_issues = pylint_results + bandit_results + semgrep_results

    return {
        "file": filepath,
        "total_issues": len(all_issues),
        "pylint": pylint_results,
        "bandit": bandit_results,
        "semgrep": semgrep_results,
        "summary": {
            "pylint_count": len(pylint_results),
            "bandit_count": len(bandit_results),
            "semgrep_count": len(semgrep_results)
        }
    }
