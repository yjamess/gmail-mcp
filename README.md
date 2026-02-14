# Gmail Assistant MCP Server

An MCP server built with Python and `uv` that allows Claude Desktop to read unread emails and create threaded draft replies.

## Features
- `get_unread_emails`: Fetches the latest unread emails (sender, subject, body/snippet).
- `create_draft_reply`: Creates a correctly threaded draft reply in Gmail.
- (Optional) `get_email_style_guide`: Provides custom writing style context.

## Prerequisites
- [uv](https://docs.astral.sh/uv/) installed.
- A Google Cloud Project with the Gmail API enabled.
- `credentials.json` downloaded from Google Cloud Console.

## Setup

**Clone and install:**
```bash
git clone https://github.com/yjamess/gmail-mcp.git
cd gmail-mcp
uv sync
```

**Authentication:** Place `credentials.json` in the repo root, then run:
```bash
uv run setup_gmail.py
```
**Claude Desktop:** Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "gmail-manager": {
      "command": "/PATH/TO/uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/gmail-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

Example Prompts
"Summarise my last emails"
<img width="937" height="555" alt="Screenshot 2026-02-14 at 15 15 51" src="https://github.com/user-attachments/assets/145599f1-7236-4bb1-8efa-66f0368b0477" />

"Draft a reply to the email to the email from Theo"
<img width="797" height="356" alt="Screenshot 2026-02-14 at 15 17 25" src="https://github.com/user-attachments/assets/f597231b-0a79-4e43-814e-bb7a81ce0177" />
<img width="1094" height="265" alt="Screenshot 2026-02-14 at 15 17 44" src="https://github.com/user-attachments/assets/f586ab9a-647f-4cd3-a294-19c20bb4faa8" />

