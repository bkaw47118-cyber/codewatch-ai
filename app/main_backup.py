from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import tempfile, os
from app.analyzer import analyze
from app.prompt_builder import build_prompt
from app.llm_client import get_llm_analysis
from app.database import init_db, save_analysis, get_all_analyses

# Initialiser la base de données au démarrage


init_db()
from app.llm_client import warmup_model
warmup_model()
app = FastAPI(title="CodeWatch AI", version="1.0.0")

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
    return {"status": "ok"}

@app.get("/history")
def history():
    """Retourne l'historique de toutes les analyses"""
    return get_all_analyses()
@app.post("/compare")
async def compare_files(
    file_before: UploadFile = File(...),
    file_after: UploadFile = File(...)
):
    """Compare deux versions d'un fichier Python et mesure l'amélioration"""

    results = {}

    for label, file in [("before", file_before), ("after", file_after)]:
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.py', delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            sast = analyze(tmp_path)
            results[label] = {
                "filename": file.filename,
                "sast_results": sast
            }
        finally:
            os.unlink(tmp_path)

    # Calculer l'amélioration
    before_issues = results["before"]["sast_results"]["total_issues"]
    after_issues = results["after"]["sast_results"]["total_issues"]
    improvement = before_issues - after_issues
    improvement_pct = round((improvement / before_issues * 100) if before_issues > 0 else 0, 1)

    # Prompt comparatif pour le LLM
    before_summary = results["before"]["sast_results"]["summary"]
    after_summary = results["after"]["sast_results"]["summary"]

    prompt = f"""Tu es un expert en qualité logicielle Python.
Compare ces deux versions d'un fichier Python et génère un rapport d'amélioration en français.

=== VERSION AVANT (originale) ===
Total issues : {before_issues}
- Pylint : {before_summary['pylint_count']}
- Bandit : {before_summary['bandit_count']}
- Semgrep : {before_summary['semgrep_count']}

=== VERSION APRÈS (corrigée) ===
Total issues : {after_issues}
- Pylint : {after_summary['pylint_count']}
- Bandit : {after_summary['bandit_count']}
- Semgrep : {after_summary['semgrep_count']}

=== AMÉLIORATION ===
Issues résolues : {improvement} ({improvement_pct}%)

Génère un rapport structuré avec :
1. BILAN DE L'AMÉLIORATION : résumé de ce qui a été corrigé
2. PROBLÈMES RÉSOLUS : liste des vulnérabilités éliminées
3. PROBLÈMES RESTANTS : ce qui n'a pas encore été corrigé
4. SCORE AVANT / APRÈS : note sur 10 pour chaque version
5. RECOMMANDATIONS : prochaines étapes pour améliorer davantage
"""

    llm_report = get_llm_analysis(prompt)

    return {
        "before": results["before"],
        "after": results["after"],
        "improvement": {
            "issues_resolved": improvement,
            "improvement_pct": improvement_pct,
            "before_total": before_issues,
            "after_total": after_issues
        },
        "llm_report": llm_report,
        "status": "success"
    }


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

        # Sauvegarder dans la base de données
        analysis_id = save_analysis(file.filename, sast_results, llm_report)

        return {
            "id": analysis_id,
            "filename": file.filename,
            "sast_results": sast_results,
            "llm_report": llm_report,
            "status": "success"
        }
    finally:
        os.unlink(tmp_path)
