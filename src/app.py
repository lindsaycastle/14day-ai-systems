from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from scripts.rate_limiter import limit
from src.ai_service import generate_answer

app = FastAPI(title="Day 7 AI Web App")

# Serve static frontend
app.mount("/web", StaticFiles(directory="web"), name="web")

class AskRequest(BaseModel):
    prompt: str

def global_key_func():
    # All functions share this key to enforce a single global limit
    return "global_api_calls"


@app.get("/")
def home():
    return FileResponse("web/index.html")


@app.post("/api/ask")
def ask(req: AskRequest):

    prompt = req.prompt.strip()
    if not prompt:
        return {"ok": False, "error": "Prompt cannot be empty."}

    if limit() == False:
        return {"ok": False, "error": "Rate limit exceeded. Please try again later."}

    if len(prompt) > 1000:
        return {"ok": False, "error": "Prompt is too long. Maximum length is 1000 characters."}

    try:
        answer = generate_answer(prompt)
        return {"ok": True, "answer": answer}
    except Exception as e:
        return {"ok": False, "error": str(e)}