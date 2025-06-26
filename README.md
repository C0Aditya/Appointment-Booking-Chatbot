🧵 TailorTalk — Your Smart Meeting Scheduler with Natural Language
TailorTalk is a conversational AI assistant that helps users schedule meetings using natural language. It leverages FastAPI, LangGraph, and Google Calendar integration to interpret user intent, check availability, and confirm bookings seamlessly.

✨ Built with simplicity in mind — just say things like:

"Schedule a meeting tomorrow at 2 PM"

…and TailorTalk takes care of the rest.

🚀 Features
✅ Natural language date/time parsing (via dateparser)

✅ Intelligent availability checks using your Google Calendar

✅ Seamless meeting booking with a unique Google Meet link

✅ Supports multi-turn conversation with confirmation handling

✅ Streamlit front-end for quick testing

📸 Demo
Coming soon (include screenshot or GIF once available)

🧠 How It Works
LangGraph handles the multi-step conversational logic

The agent uses one unified state node to:

Parse the message

Detect intent

Store and recall proposed times

Book or cancel based on confirmation

FastAPI backend exposes a /chat endpoint to receive messages and respond with the bot’s reply

Streamlit front-end makes it easy to chat with the bot interactively

📁 Project Structure
graphql
Copy
Edit
TailorTalk/
│
├── agent.py               # LangGraph logic (natural language → booking)
├── main.py                # FastAPI backend
├── app.py                 # Streamlit front-end
├── calendar_utils.py      # Google Calendar auth + API helpers
├── credentials.json       # Google API credentials (not included)
├── token.json             # Generated on first Google auth
└── README.md              # This file
⚙️ Requirements
Install the following dependencies inside a virtual environment:

bash
Copy
Edit
pip install -r requirements.txt
requirements.txt:

txt
Copy
Edit
fastapi
uvicorn
streamlit
langgraph
dateparser
google-api-python-client
google-auth
google-auth-oauthlib
requests
🛠️ Setup Instructions
Clone the repo:

bash
Copy
Edit
git clone https://github.com/yourusername/TailorTalk.git
cd TailorTalk
Place your Google Calendar OAuth credentials JSON as credentials.json in the root directory.

Get credentials from: https://console.cloud.google.com/apis/credentials

Run the FastAPI backend:

bash
Copy
Edit
uvicorn main:app --reload
In a new terminal, start the Streamlit app:

bash
Copy
Edit
streamlit run app.py
🔐 Google Calendar Integration
The first time you run TailorTalk, it will prompt a browser-based Google login.

⚠️ Note: If the app is not verified by Google, you will need to click "Advanced" and "Proceed anyway" (or add yourself as a test user in your OAuth consent screen).

💬 Example Conversation
User: schedule a meeting tomorrow at 2pm
Bot: You are free at 2025-06-27 14:00. Would you like me to book it?
User: yes
Bot: Meeting booked! Link: https://meet.google.com/abc-defg-hij

📌 Tips
Dates like “tomorrow” or “next Monday” work great.

If you're unavailable, the bot will ask you to suggest another slot.

Confirmation must include “yes” or “no”.

🧩 Possible Improvements
Email notification integration

Voice assistant support

More flexible rescheduling and cancellations

Persistent memory with a database

🧑‍💻 Author
✉️ theodricknight0@gmail.com
