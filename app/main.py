from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import tempfile, os
from app.analyzer import analyze
from app.prompt_builder import build_prompt
from app.llm_client import get_llm_analysis
from app.database import init_db, save_analysis, get_all_analyses

init_db()
from app.llm_client import warmup_model
warmup_model()

app = FastAPI(title="CodeWatch AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
def root():
    return FileResponse("frontend/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0", "modes": ["standard", "pro"]}

@app.get("/history")
def history():
    return get_all_analyses()

def build_pro_prompt(code: str, sast_results: dict) -> str:
    issues = sast_results.get("issues", [])
    total = sast_results.get("total_issues", 0)
    summary = sast_results.get("summary", {})
    issues_text = ""
    for i, issue in enumerate(issues[:15], 1):
        issues_text += f"{i}. [{issue.get('tool','?').upper()}] Ligne {issue.get('line','?')} - {issue.get('message','?')} (Severite: {issue.get('severity','?')})\n"
    prompt = f"""<|im_start|>system
Tu es CodeWatch AI PRO, un systeme expert en cybersecurite et analyse de code Python, specialise dans la detection de vulnerabilites OWASP, CWE et CVE. Tu as ete entraine sur des milliers de cas reels de vulnerabilites Python issues de projets open-source. Tu fournis des analyses precises, structurees et actionnables pour les equipes DevSecOps.
<|im_end|>
<|im_start|>user
Analyse de securite avancee du code Python suivant.

## Resultats SAST pre-analyse :
- Total issues detectees : {total}
- Pylint : {summary.get('pylint_count', 0)} issues
- Bandit : {summary.get('bandit_count', 0)} issues de securite
- Semgrep : {summary.get('semgrep_count', 0)} patterns dangereux

## Issues detectees :
{issues_text}

## Code source :
```python
{code[:3000]}
```

Genere un rapport de securite PRO structure :

### SCORE DE SECURITE
Donne un score de 0 a 100 avec justification precise.

### VULNERABILITES CRITIQUES (CVSS >= 7.0)
Pour chaque vulnerabilite critique :
- Type CWE / OWASP correspondant
- Ligne exacte dans le code
- Explication de l impact reel
- Exemple d exploitation (proof of concept)
- Correction recommandee avec code corrige

### VULNERABILITES MOYENNES (CVSS 4.0-6.9)
Liste avec impact et correction.

### PROBLEMES MINEURS
Qualite, maintenabilite, bonnes pratiques.

### PLAN DE REMEDIATION PRIORISE
Etapes concretes numerotees par ordre de priorite.

### CONFORMITE
Verification par rapport a : OWASP Top 10, CWE Top 25.
<|im_end|>
<|im_start|>assistant"""
    return prompt

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Fichier .py uniquement")
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.py', delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        sast_results = analyze(tmp_path)
        code = content.decode('utf-8')
        prompt = build_prompt(code, sast_results)
        llm_report = get_llm_analysis(prompt)
        analysis_id = save_analysis(file.filename, sast_results, llm_report)
        return {
            "id": analysis_id,
            "filename": file.filename,
            "mode": "standard",
            "model": "Qwen2.5-Coder:14B",
            "sast_results": sast_results,
            "llm_report": llm_report,
            "status": "success"
        }
    finally:
        os.unlink(tmp_path)

@app.post("/analyze-pro")
async def analyze_file_pro(file: UploadFile = File(...)):
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Fichier .py uniquement")
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.py', delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        sast_results = analyze(tmp_path)
        code = content.decode('utf-8')
        prompt = build_pro_prompt(code, sast_results)
        llm_report = get_llm_analysis(prompt)
        analysis_id = save_analysis(file.filename + " [PRO]", sast_results, llm_report)
        return {
            "id": analysis_id,
            "filename": file.filename,
            "mode": "pro",
            "model": "Qwen2.5-Coder:14B + Security Prompt Engineering",
            "sast_results": sast_results,
            "llm_report": llm_report,
            "status": "success"
        }
    finally:
        os.unlink(tmp_path)

@app.post("/compare")
async def compare_files(
    file_before: UploadFile = File(...),
    file_after: UploadFile = File(...)
):
    results = {}
    for label, file in [("before", file_before), ("after", file_after)]:
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.py', delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        try:
            sast = analyze(tmp_path)
            results[label] = {"filename": file.filename, "sast_results": sast}
        finally:
            os.unlink(tmp_path)
    before_issues = results["before"]["sast_results"]["total_issues"]
    after_issues = results["after"]["sast_results"]["total_issues"]
    improvement = before_issues - after_issues
    improvement_pct = round((improvement / before_issues * 100) if before_issues > 0 else 0, 1)
    before_summary = results["before"]["sast_results"]["summary"]
    after_summary = results["after"]["sast_results"]["summary"]
    prompt = f"""Tu es un expert en qualite logicielle Python.
Compare ces deux versions et genere un rapport d amelioration en francais.

VERSION AVANT : {before_issues} issues (Pylint:{before_summary['pylint_count']}, Bandit:{before_summary['bandit_count']}, Semgrep:{before_summary['semgrep_count']})
VERSION APRES : {after_issues} issues (Pylint:{after_summary['pylint_count']}, Bandit:{after_summary['bandit_count']}, Semgrep:{after_summary['semgrep_count']})
AMELIORATION : {improvement} issues resolues ({improvement_pct}%)

Genere un rapport avec : 1.BILAN 2.PROBLEMES RESOLUS 3.PROBLEMES RESTANTS 4.SCORE AVANT/APRES sur 10 5.RECOMMANDATIONS"""
    llm_report = get_llm_analysis(prompt)
    return {
        "before": results["before"],
        "after": results["after"],
        "improvement": {"issues_resolved": improvement, "improvement_pct": improvement_pct, "before_total": before_issues, "after_total": after_issues},
        "llm_report": llm_report,
        "status": "success"
    }


@app.get("/dashboard")
def dashboard():
    """Données pour le dashboard manager"""
    import json
    from sqlalchemy import text
    from app.database import engine
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, filename, total_issues, pylint_count, bandit_count, semgrep_count, created_at FROM analyses ORDER BY created_at ASC")).fetchall()
    if not rows:
        return {"total_analyses": 0, "avg_score": 0, "evolution": [], "tools_stats": {}, "top_files": []}
    total = len(rows)
    avg_issues = round(sum(r[2] for r in rows) / total, 1)
    avg_score = max(0, round(100 - (avg_issues * 4), 1))
    evolution = [{"id": r[0], "filename": r[1][:20], "total_issues": r[2], "score": max(0, 100 - r[2]*4), "date": str(r[6])[:10] if r[6] else ""} for r in rows]
    tools_stats = {
        "pylint": sum(r[3] or 0 for r in rows),
        "bandit": sum(r[4] or 0 for r in rows),
        "semgrep": sum(r[5] or 0 for r in rows)
    }
    top_files = sorted([{"filename": r[1], "total_issues": r[2], "score": max(0, 100 - r[2]*4)} for r in rows], key=lambda x: x["total_issues"], reverse=True)[:5]
    return {
        "total_analyses": total,
        "avg_issues": avg_issues,
        "avg_score": avg_score,
        "evolution": evolution,
        "tools_stats": tools_stats,
        "top_files": top_files
    }
