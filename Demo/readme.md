HELPCPT-ENDOR-BOT/
├── requirements.txt
├── socket_app.py                 # ← run this (Socket Mode, no public URL)
└── src/
    ├── block_kits/
    │   └── block_kit.py          # ← Slack modal + summary blocks
    ├── LLM_connect/
    │   └── qa_module.py          # ← mock “LLM” field extraction + clarify
    └── Helpcentral_Tickets/
        └── ticket_creation.py    # ← mock ServiceNow: returns INC ids


How to run (local, Socket Mode)

Create Slack App → enable Socket Mode, generate App-Level Token (xapp-…).
Add bot scopes: commands, chat:write, im:write. Create slash command /rpa-support.

Install app to workspace → get Bot Token (xoxb-…).

Run:
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export SLACK_BOT_TOKEN=xoxb-***
export SLACK_APP_TOKEN=xapp-***

python socket_app.py

In Slack:

/rpa-support My payroll bot failed last night at 10PM, please check


→ Modal opens (prefilled) → Submit:

P1/P3 → you get a DM with mock INC and summary blocks.

P2 → DM confirming a “forwarded” message (mock).


