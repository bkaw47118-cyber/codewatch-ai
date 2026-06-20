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
