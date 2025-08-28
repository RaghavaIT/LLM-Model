from typing import Iterable, Optional

def _opt(text: str) -> dict:
    return {"text": {"type": "plain_text", "text": text}, "value": text}

def build_ticket_modal(prefill: Optional[dict] = None, bot_options: Optional[Iterable[str]] = None) -> dict:
    pre = prefill or {}
    blocks = [
        {"type":"input","block_id":"priority",
         "label":{"type":"plain_text","text":"Priority"},
         "element":{"type":"static_select","action_id":"priority_select",
                    "initial_option": _opt(pre.get("priority","P2")),
                    "options":[_opt("P1"),_opt("P2"),_opt("P3")]}}
    ]

    if bot_options:
        el = {"type":"static_select","action_id":"bot_name_select","options":[_opt(x) for x in bot_options]}
        if pre.get("bot_name") in bot_options:
            el["initial_option"] = _opt(pre["bot_name"])
        blocks.append({"type":"input","block_id":"bot_name","label":{"type":"plain_text","text":"Bot name"},"element": el})
    else:
        blocks.append({"type":"input","block_id":"bot_name","label":{"type":"plain_text","text":"Bot name"},
                       "element":{"type":"plain_text_input","action_id":"bot_name_in","initial_value": pre.get("bot_name","")}})

    blocks += [
        {"type":"input","block_id":"exec_time","optional":True,
         "label":{"type":"plain_text","text":"Execution time/date"},
         "element":{"type":"plain_text_input","action_id":"exec_time_in","initial_value": pre.get("exec_time","")}},
        {"type":"input","block_id":"details",
         "label":{"type":"plain_text","text":"Issue details"},
         "element":{"type":"plain_text_input","action_id":"details_in","multiline":True,"initial_value": pre.get("details","")}},
        {"type":"input","block_id":"params","optional":True,
         "label":{"type":"plain_text","text":"Input file / parameters (optional)"},
         "element":{"type":"plain_text_input","action_id":"params_in","initial_value": pre.get("params","")}},
    ]

    return {
        "type":"modal","callback_id":"create_sn_ticket",
        "title":{"type":"plain_text","text":"RPA Support"},
        "submit":{"type":"plain_text","text":"Create"},
        "close":{"type":"plain_text","text":"Cancel"},
        "blocks": blocks
    }

def summary_blocks(priority: str, bot_name: str, exec_time: str | None, details: str, inc: str | None) -> list[dict]:
    header = f"{'✅' if inc else '🛈'} RPA Support"
    if inc:
        header += f" — Ticket {inc}"
    return [
        {"type":"header","text":{"type":"plain_text","text":header}},
        {"type":"section","fields":[
            {"type":"mrkdwn","text":f"*Priority:*\n{priority}"},
            {"type":"mrkdwn","text":f"*Bot:*\n{bot_name}"},
            {"type":"mrkdwn","text":f"*When:*\n{exec_time or 'N/A'}"},
        ]},
        {"type":"section","text":{"type":"mrkdwn","text":f"*Details:*\n{details}"}}
    ]
