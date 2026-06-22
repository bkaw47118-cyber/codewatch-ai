# CodeWatch AI

<!-- CODEWATCH-BADGES-START -->
![Security Score](https://img.shields.io/badge/security%20score-85%2F100-brightgreen?style=flat-square&logo=shield) ![Issues](https://img.shields.io/badge/issues-39-red?style=flat-square) ![Tools](https://img.shields.io/badge/tools-Pylint%20%7C%20Bandit%20%7C%20Semgrep-blue?style=flat-square) ![Model](https://img.shields.io/badge/LLM-Qwen2.5--Coder%2014B-purple?style=flat-square)
<!-- CODEWATCH-BADGES-END -->

![CI](https://github.com/bkaw47118-cyber/codewatch-ai/actions/workflows/codewatch.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square&logo=fastapi)
![License](https://img.shields.io/badge/license-MIT-grey?style=flat-square)

> **Plateforme intelligente de revue automatique de code Python** intégrant analyse statique, IA et DevSecOps.
> 
> 📄 [Rapport de sécurité en direct](https://bkaw47118-cyber.github.io/codewatch-ai/) · 🚀 [Interface web](http://5.78.97.46:8000)

---

## Architecture

```
CodeWatch AI
├── Analyse statique (SAST)     ← Pylint + Bandit + Semgrep
├── Analyse IA                  ← Qwen2.5-Coder 14B (Ollama)
│   ├── Mode Standard           ← Rapport qualité général
│   └── Mode PRO                ← CVSS · OWASP/CWE · Proof of Concept
├── Dashboard Manager           ← KPIs · évolution · top fichiers
├── Comparaison de versions     ← avant/après correction
└── CI/CD GitHub Actions        ← bot PR · badges · GitHub Pages
```

## Stack technique

| Composant | Technologie |
|---|---|
| Backend API | FastAPI + Python 3.12 |
| Analyse statique | Pylint 4.0.6 · Bandit 1.9.4 · Semgrep 1.167.0 |
| LLM | Qwen2.5-Coder 14B via Ollama |
| Base de données | SQLite / SQLAlchemy |
| Frontend | HTML/CSS/JS vanilla + Chart.js |
| CI/CD | GitHub Actions |
| Serveur | Ubuntu 24.04 · Hetzner · 48 cores · 184GB RAM |

## Fonctionnalités

- ✅ **Mode Standard** — analyse complète Pylint + Bandit + Semgrep + rapport IA
- ✅ **Mode PRO** — score CVSS, mapping OWASP/CWE, proof of concept, plan de remédiation priorisé
- ✅ **Dashboard Manager** — KPIs, évolution du score, répartition des outils, top fichiers vulnérables
- ✅ **Comparaison de versions** — mesure l'amélioration avant/après correction
- ✅ **Bot GitHub Actions** — commente automatiquement les Pull Requests avec les résultats
- ✅ **Badges dynamiques** — score de sécurité mis à jour à chaque push
- ✅ **Rapport GitHub Pages** — rapport HTML généré automatiquement

## Lancement rapide

```bash
# Cloner le repo
git clone https://github.com/bkaw47118-cyber/codewatch-ai.git
cd codewatch-ai

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Accéder à l'interface
open http://localhost:8000
```

## API Endpoints

| Endpoint | Méthode | Description |
|---|---|---|
| `/` | GET | Interface web |
| `/health` | GET | Statut API |
| `/analyze` | POST | Analyse Standard |
| `/analyze-pro` | POST | Analyse PRO |
| `/compare` | POST | Comparaison de versions |
| `/history` | GET | Historique des analyses |
| `/dashboard` | GET | Données Dashboard Manager |

---

**Mémoire de fin d'études — ENPO-MA 2026**  
Kawther BOUZEROUAT.
*Ingénierie du Management et des Systèmes d'Information*
