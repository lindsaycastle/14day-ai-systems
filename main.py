import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI

app = FastAPI(title="Live AI App")

class PromptIn(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ask")
def ask(payload: PromptIn):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Keep responses concise and accurate."},
                {"role": "user", "content": payload.prompt},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        answer = (resp.choices[0].message.content or "").strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))