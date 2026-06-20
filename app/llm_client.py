import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:14b"

def warmup_model():
    """Préchauffe le modèle au démarrage — évite le cold start"""
    try:
        print("Chargement de Qwen2.5-Coder en mémoire...")
        requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": "bonjour", "stream": False},
            timeout=300
        )
        print("Modèle prêt.")
    except Exception as e:
        print(f"Warmup ignoré : {e}")

def get_llm_analysis(prompt: str) -> str:
    """Envoie le prompt à Qwen2.5-Coder via Ollama"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=300
        )
        if response.status_code == 200:
            return response.json().get("response", "Aucune réponse reçue.")
        else:
            return f"Erreur Ollama : {response.status_code}"
    except requests.exceptions.Timeout:
        return "Erreur : le modèle a mis trop de temps à répondre."
    except Exception as e:
        return f"Erreur de connexion à Ollama : {str(e)}"
