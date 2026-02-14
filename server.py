import os
import base64
from email.message import EmailMessage
from typing import Any

from mcp.server.fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose"
]

# Initialize FastMCP
mcp = FastMCP("Gmail Manager")

def get_gmail_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

@mcp.tool()
def get_unread_emails(max_results: int = 5) -> list[dict[str, Any]]:
    """Fetch unread emails from the inbox."""
    service = get_gmail_service()
    try:
        results = service.users().messages().list(userId='me', q='is:unread', maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for msg in messages:
            full_msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            headers = full_msg['payload']['headers']
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
            snippet = full_msg.get('snippet', '')
            
            email_data.append({
                "id": msg['id'],
                "threadId": msg['threadId'],
                "sender": sender,
                "subject": subject,
                "snippet": snippet
            })
        return email_data
    except HttpError as error:
        return [{"error": str(error)}]

@mcp.tool()
def create_draft_reply(thread_id: str, reply_body: str) -> dict:
    """Create a draft reply for a specific email thread."""
    service = get_gmail_service()
    try:
        # Get the original message to extract headers for proper threading
        thread = service.users().threads().get(userId='me', id=thread_id).execute()
        original_msg = thread['messages'][-1]
        headers = original_msg['payload']['headers']
        
        # Setup headers for threading
        to_address = next((h['value'] for h in headers if h['name'] == 'From'), "")
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "")
        if not subject.startswith("Re:"):
            subject = f"Re: {subject}"

        message = EmailMessage()
        message.set_content(reply_body)
        message['To'] = to_address
        message['Subject'] = subject
        message['In-Reply-To'] = next((h['value'] for h in headers if h['name'] == 'Message-ID'), "")
        message['References'] = next((h['value'] for h in headers if h['name'] == 'Message-ID'), "")

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        draft_body = {
            'message': {
                'threadId': thread_id,
                'raw': encoded_message
            }
        }
        
        draft = service.users().drafts().create(userId='me', body=draft_body).execute()
        return {"status": "success", "draft_id": draft['id']}
    except HttpError as error:
        return {"error": str(error)}

@mcp.tool()
def get_email_style_guide() -> str:
    """Read the email style guide context."""
    with open("style.md", "r") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()