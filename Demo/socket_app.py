import os
import asyncio
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web.async_client import AsyncWebClient

from src.LLM_connect.qa_module import extract_ticket_from_text, clarify_if_ambiguous
from src.block_kits.block_kit import build_ticket_modal, summary_blocks
from src.Helpcentral_Tickets.ticket_creation import create_incident, summarize_confirmation

app = App(token=os.environ["SLACK_BOT_TOKEN"])

def async_client() -> AsyncWebClient:
    return AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])

PRIORITY_TO_URGENCY = {"P1": "1", "P2": "2", "P3": "3"}

@app.command("/rpa-support")
def handle_slash_command(ack, body, client, logger):
    # ACK fast (within 3s)
    ack()
    text = (body.get("text") or "").strip()
    trigger_id = body["trigger_id"]

    async def work():
        prefill = await extract_ticket_from_text(text)
        _ = await clarify_if_ambiguous(prefill)  # (optional) ask clarifying DM; we keep it simple here
        modal = build_ticket_modal(prefill=prefill, bot_options=["PayrollBot", "InvoiceBot", "OrderBot"])
        await async_client().views_open(trigger_id=trigger_id, view=modal)

    asyncio.get_event_loop().create_task(work())

@app.view("create_sn_ticket")
def handle_modal_submission(ack, body, view, client, logger):
    # close the modal quickly
    ack()

    v = view["state"]["values"]
    # priority is static_select
    priority = v["priority"]["priority_select"]["selected_option"]["value"]

    # bot name can be from select OR text input (we prefer select if present)
    bot_name = ""
    if "bot_name_select" in v["bot_name"]:
        bot_name = v["bot_name"]["bot_name_select"]["selected_option"]["value"]
    elif "bot_name_in" in v["bot_name"]:
        bot_name = v["bot_name"]["bot_name_in"]["value"]

    exec_time = v["exec_time"].get("exec_time_in", {}).get("value", "")
    details   = v["details"]["details_in"]["value"]
    params    = v.get("params", {}).get("params_in", {}).get("value", "")
    user_id   = body["user"]["id"]

    async def work():
        if priority in ("P1", "P3"):
            short = f"[{priority}] {bot_name} issue"
            desc  = f"Bot: {bot_name}\nWhen: {exec_time or 'N/A'}\nDetails: {details}\nParams: {params or 'N/A'}"
            inc, _sys_id = await create_incident(short, desc, urgency=PRIORITY_TO_URGENCY[priority])

            blocks = summary_blocks(priority, bot_name, exec_time, details, inc=inc)
            human  = await summarize_confirmation(inc, bot_name, exec_time, details)

            im = await async_client().conversations_open(users=user_id)
            await async_client().chat_postMessage(channel=im["channel"]["id"], text=human, blocks=blocks)

        else:
            # P2 → just DM a nice “forwarded” styled block (mock)
            blocks = summary_blocks(priority, bot_name, exec_time, details, inc=None)
            im = await async_client().conversations_open(users=user_id)
            await async_client().chat_postMessage(
                channel=im["channel"]["id"],
                text="Your request has been forwarded to the RPA support channel.",
                blocks=blocks
            )

    asyncio.get_event_loop().create_task(work())

if __name__ == "__main__":
    # Requires:
    #   SLACK_BOT_TOKEN = xoxb-***
    #   SLACK_APP_TOKEN = xapp-***  (App-level token; Socket Mode enabled)
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
