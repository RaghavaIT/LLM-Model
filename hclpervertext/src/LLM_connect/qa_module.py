# src/LLM_connect/qa_module.py
import os, json, httpx
from typing import Dict

# Endor LLM config (env-injected)
ENDOR_API_URL = os.getenv("ENDOR_API_URL")  # e.g., https://endor.company.ai/v1/chat/completions
ENDOR_API_KEY = os.getenv("ENDOR_API_KEY")  # Bearer token or similar
ENDOR_MODEL   = os.getenv("ENDOR_MODEL", "endor-text-mixtral")

SYSTEM = (
    "You extract ticket fields for an RPA support flow. "
    "Return strict JSON with keys: priority (P1/P2/P3), bot_name, exec_time, details, params. "
    "Priority rules: P1=critical outage/production; P2=question/support; P3=low/scheduled/rerun."
)

async def extract_ticket_from_text(text: str) -> Dict:
    """
    Call Endor 'endor-text-mixtral' and return a dict with:
      priority, bot_name, exec_time, details, params
    """
    if not text:
        return {}

    headers = {
        "Authorization": f"Bearer {ENDOR_API_KEY}",
        "Content-Type": "application/json",
    }

    # Adjust payload fields to match Endor’s API (example shown)
    payload = {
        "model": ENDOR_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"User message:\n{text}\nReturn ONLY JSON."},
        ],
        # ask for JSON so parsing is robust
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(ENDOR_API_URL, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()

    # Normalize to a dict
    try:
        # Typical “chat.completions” shape
        content = data["choices"][0]["message"]["content"]
        obj = json.loads(content)
    except Exception:
        obj = {"details": text}

    # Safe defaults
    return {
        "priority": obj.get("priority", "P2"),
        "bot_name": obj.get("bot_name", ""),
        "exec_time": obj.get("exec_time", ""),
        "details": obj.get("details", text),
        "params": obj.get("params", ""),
    }
