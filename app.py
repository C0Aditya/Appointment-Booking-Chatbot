import streamlit as st
import uuid
from agent import flow

# Page config
st.set_page_config(page_title="TailorTalk – Booking Assistant", layout="centered")
st.title("🧵 TailorTalk – Booking Assistant")

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = {"message": "", "last_start_end": None}

# Show User ID
st.markdown(f"**Your User ID:** `{st.session_state.user_id}`")

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    send = st.form_submit_button("Send")

if send and user_input.strip():
    # Append user message
    st.session_state.chat_history.append(("You", user_input))
    # Update the LangGraph state
    st.session_state.conversation_state["message"] = user_input

    # Run the flow
    last_bot = "Sorry, I couldn't process that."
    for ev in flow.stream(st.session_state.conversation_state):
        node_state = next(iter(ev.values()))
        if "message" in node_state:
            last_bot = node_state["message"]
        st.session_state.conversation_state = node_state

    # Append bot response
    st.session_state.chat_history.append(("Bot", last_bot))
    # **NO** st.experimental_rerun()

# Render chat history
st.markdown("---")
for who, text in st.session_state.chat_history:
    st.markdown(f"**{who}:** {text}")
