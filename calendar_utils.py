import os
import datetime
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CRED_PATH = os.getenv("CREDENTIALS_PATH", "credentials.json")
TOKEN_PATH = os.getenv("TOKEN_PATH", "token.json")
CALENDAR_ID = os.getenv("CALENDAR_ID", "primary")

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def check_availability(start_time: datetime.datetime, end_time: datetime.datetime) -> bool:
    service = get_calendar_service()
    # Convert to RFC3339 format with timezone
    time_min = start_time.isoformat()
    time_max = end_time.isoformat()
    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute().get('items', [])
    return len(events) == 0

def book_meeting(start_time: datetime.datetime, end_time: datetime.datetime, summary="TailorTalk Booking") -> str:
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': start_time.tzinfo.zone if start_time.tzinfo else 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': end_time.tzinfo.zone if end_time.tzinfo else 'UTC',
        },
        # Optional: add conferencing
        'conferenceData': {
            'createRequest': {
                'requestId': f"tt-{int(start_time.timestamp())}"
            }
        }
    }
    created = service.events().insert(
        calendarId=CALENDAR_ID,
        body=event,
        conferenceDataVersion=1
    ).execute()
    return created.get('htmlLink', created.get('hangoutLink', ''))
