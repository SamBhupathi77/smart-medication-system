from pathlib import Path
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = PROJECT_ROOT / "token.json"
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"


def get_calendar_service():
    creds = None

    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    except Exception:
        creds = None

    if not creds:
        if not CREDENTIALS_FILE.exists():
            raise FileNotFoundError(f"Missing Google credentials file: {CREDENTIALS_FILE}")

        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
        creds = flow.run_local_server(port=0)

        with open(str(TOKEN_FILE), "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_calendar_event(medication_name, reminder_time):
    service = get_calendar_service()

    today = datetime.now().date()
    event_datetime = datetime.strptime(f"{today} {reminder_time}", "%Y-%m-%d %H:%M")

    if event_datetime < datetime.now():
        event_datetime += timedelta(days=1)

    event = {
        "summary": f"Take {medication_name}",
        "description": f"Medication Reminder: {medication_name}",
        "start": {
            "dateTime": event_datetime.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": event_datetime.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": 10}],
        },
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event.get("htmlLink")