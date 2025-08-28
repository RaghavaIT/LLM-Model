import re
from typing import Dict

BOT_HINTS = ["PayrollBot", "InvoiceBot", "OrderBot"]

def _guess_priority(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["outage", "down", "failed", "production", "p1", "urgent", "critical"]):
        return "P1"
    if any(k in t for k in ["rerun", "reschedule", "schedule", "p3", "low"]):
        return "P3"
    return "P2"

def _extract_time(text: str) -> str:
    m = re.search(r"\b(\d{1,2}(:\d{2})?\s?(am|pm)?)\b", text, re.I)
    return m.group(1) if m else ""

def _extract_bot(text: str) -> str:
    for name in BOT_HINTS:
        if name.lower() in text.lower():
            return name
    m = re.search(r"\b(payroll|invoice|order)\b", text, re.I)
    return f"{m.group(1).title()}Bot" if m else ""

async def extract_ticket_from_text(text: str) -> Dict:
    return {
        "priority": _guess_priority(text),
        "bot_name": _extract_bot(text),
        "exec_time": _extract_time(text),
        "details": text.strip(),
        "params": "",
    }

async def clarify_if_ambiguous(data: Dict) -> str | None:
    if not data.get("bot_name"):
        return "Which bot are you referring to – PayrollBot or InvoiceBot?"
    return None
