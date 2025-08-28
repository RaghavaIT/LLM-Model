import itertools
from typing import Tuple

_inc_seq = itertools.count(12345)

async def create_incident(short_description: str, description: str, urgency: str = "2") -> Tuple[str, str]:
    """
    Mock ServiceNow create. Returns (INC number, sys_id).
    Replace with real REST call later.
    """
    inc = f"INC{next(_inc_seq)}"
    sys_id = f"demo-{inc.lower()}"
    return inc, sys_id

async def summarize_confirmation(inc: str, bot_name: str, exec_time: str, details: str) -> str:
    when = exec_time or "N/A"
    return f"Thanks, I’ve created ticket *{inc}* for *{bot_name}* (failure at {when}). Our RPA team has been notified."
