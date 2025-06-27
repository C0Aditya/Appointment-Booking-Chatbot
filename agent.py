from langgraph.graph import StateGraph, END
from calendar_utils import check_availability, book_meeting
import datetime
import dateparser
import re
from typing import TypedDict, Optional, Tuple

class AgentState(TypedDict):
    message: str
    last_start_end: Optional[Tuple[datetime.datetime, datetime.datetime]]

def parse_booking_intent(message: str):
    # Extract phrases like “tomorrow”, “next Monday”, “29th June 1pm”
    pattern = (
        r"(tomorrow|next\s+\w+|"
        r"\d{1,2}(st|nd|rd|th)?\s+\w+\s*\d{0,4}|"
        r"\d{4}-\d{1,2}-\d{1,2}\s*\d{1,2}[:.]\d{2}\s*(am|pm)?|"
        r"\d{1,2}[:.]\d{2}\s*(am|pm)?)"
    )
    matches = re.findall(pattern, message, re.IGNORECASE)
    for m in matches:
        phrase = m[0]
        dt = dateparser.parse(phrase, settings={"PREFER_DATES_FROM": "future"})
        if dt:
            start = dt
            end = start + datetime.timedelta(minutes=30)
            return start, end
    return None

def root_node(state: AgentState):
    msg = state["message"].lower()
    slot = state.get("last_start_end")

    # Confirmation flow
    if "yes" in msg and slot:
        link = book_meeting(*slot)
        return {"message": f"Meeting booked! Link: {link}",
                "last_start_end": None, "next": END}
    if "no" in msg:
        return {"message": "Okay, booking cancelled.",
                "last_start_end": None, "next": END}

    # Parse a new booking intent
    parsed = parse_booking_intent(msg)
    if not parsed:
        return {"message": "I couldn't understand the date and time. Can you rephrase?",
                "last_start_end": None, "next": END}

    start, end = parsed
    if check_availability(start, end):
        return {"message": f"You are free at {start.strftime('%Y-%m-%d %H:%M')}. Would you like me to book it?",
                "last_start_end": (start, end), "next": END}
    else:
        return {"message": "You're busy at that time. Please suggest another slot.",
                "last_start_end": None, "next": END}

# Build and compile the graph
graph = StateGraph(AgentState)
graph.add_node("root", root_node)
graph.set_entry_point("root")
flow = graph.compile()
