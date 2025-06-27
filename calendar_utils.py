import os
import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# If you set a different filename, update here
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "service-account.json")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CALENDAR_ID = os.getenv("CALENDAR_ID", "primary")

def get_calendar_service():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=creds)
    return service

def check_availability(start_time: datetime.datetime, end_time: datetime.datetime) -> bool:
    service = get_calendar_service()
    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute().get("items", [])
    return len(events) == 0

def book_meeting(start_time: datetime.datetime, end_time: datetime.datetime, summary="TailorTalk Booking") -> str:
    service = get_calendar_service()
    event = {
        "summary": summary,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end":   {"dateTime": end_time.isoformat(),   "timeZone": "UTC"},
        "conferenceData": {
            "createRequest": {"requestId": f"tt-{int(start_time.timestamp())}"}
        }
    }
    created = service.events().insert(
        calendarId=CALENDAR_ID,
        body=event,
        conferenceDataVersion=1
    ).execute()
    return created.get("htmlLink", "")
