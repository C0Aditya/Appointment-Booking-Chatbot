import streamlit as st
import requests
import uuid

st.title("TailorTalk - Booking Assistant")

# Initialize chat history and user ID
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    # Auto-generate a simple unique ID per user session
    st.session_state.user_id = str(uuid.uuid4())[:8]

st.write(f"**Your User ID:** `{st.session_state.user_id}`")

user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    st.session_state.messages.append(("You", user_input))

    try:
        res = requests.post(
            "https://appointment-booking-chatbot-yu7qxdcmhynnddftuzejq9.streamlit.app/",
            json={"user_id": st.session_state.user_id, "message": user_input}
        )

        if res.status_code == 200:
            bot_response = res.json().get("response", "Sorry, no response.")
        else:
            bot_response = f"Server error: {res.status_code}"

    except Exception as e:
        bot_response = f"Error contacting server: {e}"

    st.session_state.messages.append(("Bot", bot_response))

# Display chat history
st.write("---")
for sender, message in st.session_state.messages:
    st.markdown(f"**{sender}:** {message}")
