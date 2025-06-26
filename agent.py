from langgraph.graph import StateGraph, END
from calendar_utils import check_availability, book_meeting
import datetime
import dateparser
import re
from typing import TypedDict, Optional, Tuple
from zoneinfo import ZoneInfo  # Use zoneinfo for timezone handling (Python 3.9+)

# Set your local timezone here
LOCAL_TZ = ZoneInfo("Asia/Kolkata")  # Adjust based on your location

# State structure
class AgentState(TypedDict):
    message: str
    last_start_end: Optional[Tuple[datetime.datetime, datetime.datetime]]

# Date extraction with timezone awareness
def parse_booking_intent(message: str):
    pattern = r"(tomorrow|next\s+\w+|\d{1,2}(st|nd|rd|th)?\s+\w+\s*\d{0,4}|\d{4}-\d{1,2}-\d{1,2}\s*\d{0,2}[:.]?\d{0,2}\s*(am|pm)?|\d{1,2}[:.]\d{2}\s*(am|pm)?)"
    matches = re.findall(pattern, message, re.IGNORECASE)

    for match in matches:
        candidate = match[0]
        parsed_datetime = dateparser.parse(candidate, settings={"PREFER_DATES_FROM": "future"})

        if parsed_datetime:
            # Ensure timezone awareness
            if parsed_datetime.tzinfo is None:
                parsed_datetime = parsed_datetime.replace(tzinfo=LOCAL_TZ)

            start_time = parsed_datetime
            end_time = start_time + datetime.timedelta(minutes=30)
            return start_time, end_time

    return None

# Unified root node handling all logic
def root_node(state: AgentState):
    message = state["message"].lower()
    last_start_end = state.get("last_start_end")

    if "yes" in message and last_start_end:
        meeting_link = book_meeting(*last_start_end)
        return {
            "message": f"Meeting booked! Link: {meeting_link}",
            "last_start_end": None,
            "next": END
        }

    if "no" in message:
        return {
            "message": "Okay, booking cancelled.",
            "last_start_end": None,
            "next": END
        }

    parsed = parse_booking_intent(message)
    if not parsed:
        return {
            "message": "I couldn't understand the date and time. Can you rephrase?",
            "last_start_end": None,
            "next": END
        }

    start_time, end_time = parsed
    if check_availability(start_time, end_time):
        return {
            "message": f"You are free at {start_time.strftime('%Y-%m-%d %H:%M')} ({LOCAL_TZ}) . Would you like me to book it?",
            "last_start_end": (start_time, end_time),
            "next": END
        }
    else:
        return {
            "message": "You're busy at that time. Please suggest another slot.",
            "last_start_end": None,
            "next": END
        }

# Build graph
graph = StateGraph(AgentState)
graph.add_node("root", root_node)
graph.set_entry_point("root")
flow = graph.compile()
