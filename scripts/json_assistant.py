import os
from dotenv import load_dotenv

from openai import OpenAI
import json
import template_prompt_validator

def build_messages(user_text: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": (
                "You are a RPG referee"
                "Be concise, correct, and do not invent facts. "
                "If unsure, say you are unsure."
                "Your response must follow this JSON schema: summary: { 'summary': string }, category { 'category': only yes, no or uncertain as a string] }, confidence: { 'confidence': float between 0 and 1 }"
                "If your response isn't a clean yes or no, return uncertain"
                "Do not include any fields, details or comments outside of the schema provided."
                "Use Vampire the Masquerade 5th edition ruleset to answer questions about the game."
            ),
        },
        {"role": "user", "content": user_text},
    ]

def call_llm(client: OpenAI, user_text: str) -> str:
    messages = build_messages(user_text)
    
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=300,
    )

    return resp.choices[0].message.content.strip()

def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY. Put it in a .env file.")

    client = OpenAI(api_key=api_key)

    print("V5 AI Assistant (type 'exit' to quit)")
    while True:
        user_text = input("\nYou: ").strip()
        if user_text.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if not user_text:
            print("Please enter a question.")
            continue

        try:
            answer = call_llm(client, user_text)
            template_prompt_validator.validate_json(json.loads(answer), json.load(open("tests/response_schema.json")))
            print("\nJson Assistant:", answer)
        except Exception as e:
            print("\nError calling the LLM API:", str(e))

if __name__ == "__main__":
    main()