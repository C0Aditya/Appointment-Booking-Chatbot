import os
import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")
TOKEN_PATH = os.getenv("TOKEN_PATH")

# Set your local timezone (must match your Calendar settings)
LOCAL_TIMEZONE = "Asia/Kolkata"  # Adjust if needed

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service

def check_availability(start_time: datetime.datetime, end_time: datetime.datetime):
    service = get_calendar_service()

    body = {
        "timeMin": start_time.isoformat(),
        "timeMax": end_time.isoformat(),
        "timeZone": LOCAL_TIMEZONE,
        "items": [{"id": "primary"}],
    }

    eventsResult = service.freebusy().query(body=body).execute()
    busy_times = eventsResult["calendars"]["primary"]["busy"]

    return len(busy_times) == 0

def book_meeting(start_time: datetime.datetime, end_time: datetime.datetime):
    service = get_calendar_service()

    event = {
        "summary": "TailorTalk Meeting",
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": LOCAL_TIMEZONE,
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": LOCAL_TIMEZONE,
        },
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event.get("htmlLink", "No meeting link generated.")

