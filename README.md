# Gmail Assistant MCP Server

An MCP server built with Python and `uv` that allows Claude Desktop to read unread emails and create threaded draft replies.

## Features
- `get_unread_emails`: Fetches the latest unread emails (sender, subject, snippet).
- `create_draft_reply`: Creates a correctly threaded draft reply in Gmail.
- (Optional) `get_style_guide`: Provides custom writing style context.

## Prerequisites
- [uv](https://docs.astral.sh/uv/) installed.
- A Google Cloud Project with the Gmail API enabled.
- `credentials.json` downloaded from Google Cloud Console.

## Setup

1. **Clone and Install:**
   ```bash
   git clone <your-repo-link>
   cd mcp-gmail-server
   uv sync

