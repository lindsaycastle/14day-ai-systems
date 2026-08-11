from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

#from scripts.rate_limiter import limit
from src.ai_service import generate_answer_with_memory
from scripts.rag_assistant import generate__rag_answer
from src.session_store import (
    load_sessions_from_disk,
    save_sessions_to_disk,
    get_recent_messages,
    append_message,
    cleanup_sessions
)

app = FastAPI(title="Day 7 AI Web App")
# Server static frontend
app.mount("/web", StaticFiles(directory="web"), name="web")

class AskRequest(BaseModel):
    prompt: str

class ChatRequest(BaseModel):
    session_id: str
    prompt: str

@app.on_event("startup")
def on_startup():
    load_sessions_from_disk()
    cleanup_sessions()
    save_sessions_to_disk()

@app.get("/")
def home():
    return FileResponse("web/index.html")

@app.post("/api/chat")
def chat(req: ChatRequest):
    session_id = (req.session_id or "").strip()
    prompt = (req.prompt or "").strip()

    if not session_id:
        return {"ok": False, "error": "Missing session_id."}
    if not prompt:
        return {"ok": False, "error": "Prompt cannot be empty."}

    # Load recent memory (short-term)
    history = get_recent_messages(session_id, limit=10)

    # Add the user message to memory
    append_message(session_id, "user", prompt)

    try:
        answer = generate_answer_with_memory(prompt, history)
        append_message(session_id, "assistant", answer)
        save_sessions_to_disk()
        return {"ok": True, "answer": answer}
    except Exception as e:
        save_sessions_to_disk()
        return {"ok": False, "error": str(e)}

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
        answer = generate__rag_answer(prompt)
        return {"ok": True, "answer": answer}
    except Exception as e:
        return {"ok": False, "error": str(e)}