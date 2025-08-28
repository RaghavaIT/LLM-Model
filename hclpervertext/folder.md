HELPCPT-ENDOR-BOT/
├── kubernetes/
│   ├── deploy.yaml
│   ├── service.yaml
│   └── ingress-internal.yaml
│
├── scripts/
│   ├── dev-deploy.sh
│   └── prod-deploy.sh
│
├── test/
│   └── (unit tests / mocks here)
│
├── src/
│   ├── block_kits/
│   │   └── block_kit.py              # Slack modal definitions
│   │
│   ├── channel_pick/
│   │   ├── auto_ticket_channel.py    # Forward tickets to internal Slack channel
│   │   └── channel_pick.py           # Logic to pick right channel/team
│   │
│   ├── database_manager/             # (optional) store ticket metadata if needed
│   │
│   ├── Helpcentral_Tickets/
│   │   ├── auto_ticket.py            # Logic for auto-ticket creation
│   │   ├── incidents.py              # Ticket utility mappings (P1/P2/P3)
│   │   ├── ticket_creation.py        # Create SN/HCL incident
│   │   └── ticket_update.py          # Update ticket status in Slack
│   │
│   ├── helper_functions/             # Common utils (timestamp, validation, etc.)
│   │
│   ├── LLM_connect/
│   │   ├── LLM_feedback.py           # Generate human-friendly confirmations
│   │   └── qa_module.py              # **Now calls endor-text-mixtral bot**
│   │
│   ├── logger/
│   │   ├── __init__.py
│   │   ├── parent_message_fetch.py   # Fetch parent threads
│   │   └── parent_message_details.py # Summarize threads
│   │
│   ├── postgresql_certificate/
│   │   └── apple_corporate_root_ca.pem
│   │
│   ├── reaction_handle/
│   │   ├── reaction_handler.py       # Handle Slack reactions (escalation, etc.)
│   │   └── reaction_message_check.py # Check message for reaction-based triggers
│   │
│   ├── secret/
│   │   └── __init__.py               # Placeholder for secrets/secret manager client
│   │
│   ├── url_formatter/
│   │   └── slack_url_formatter.py    # Format incident URLs
│   │
│   ├── validators.py                 # Pydantic models for ticket validation
│   └── main.py                       # FastAPI + Slack Bolt app entrypoint
│
├── Dockerfile
├── README.md
├── requirements.txt
└── rio.yaml                          # (optional) Helm/ArgoCD config values
