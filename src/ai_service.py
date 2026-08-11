import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict


def generate_answer_with_memory(user_text: str, history: List[Dict]) -> str:
    """
    history: list of {"role": "user"|"assistant", "content": "..."}
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")

    client = OpenAI(api_key=api_key)

    system = (
        "You are a helpful assistant.\n"
        "Maintain conversation continuity using the provided history.\n"
        "If the user asks for something ambiguous, ask one clarifying question.\n"
        "Be concise and correct.\n"
    )

    messages = [{"role": "system", "content": system}]

    # Replay recent history (short-term memory)
    for msg in history:
        if msg.get("role") in {"user", "assistant"} and isinstance(msg.get("content"), str):
            messages.append({"role": msg["role"], "content": msg["content"]})

    # Add the new user message
    messages.append({"role": "user", "content": user_text})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=300,
    )



    return resp.choices[0].message.content.strip()