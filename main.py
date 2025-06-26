from fastapi import FastAPI
from pydantic import BaseModel
from agent import flow

app = FastAPI()

conversation_state = {}

class Message(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat(msg: Message):
    user_id = msg.user_id
    user_message = msg.message

    if user_id not in conversation_state:
        conversation_state[user_id] = {"message": user_message, "last_start_end": None}
    else:
        conversation_state[user_id]["message"] = user_message

    last_message = "Sorry, I couldn't process that."

    events = flow.stream(conversation_state[user_id])
    for event in events:
        state = next(iter(event.values()))
        if "message" in state:
            last_message = state["message"]
        conversation_state[user_id] = state

    return {"response": last_message}
