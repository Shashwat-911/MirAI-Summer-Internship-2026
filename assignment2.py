import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Page Config
st.set_page_config(page_title="AI Multiverse", page_icon="🤖")

st.title("🌍 AI Multiverse")
st.write("Talk with different AI Personalities!")

# Sidebar
st.sidebar.title("Choose Personality")

personality = st.sidebar.selectbox(
    "Select",
    [
        "Common Indian Man",
        "Crazy Salman Khan Fan",
        "Little Boy",
        "Motivational Coach",
        "Software Engineer",
        "College Professor",
        "Stand-up Comedian",
        "Entrepreneur",
        "Friendly Teacher",
        "AI Assistant"
    ]
)

# Clear Chat
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    instruction = f"""
You are acting as {personality}.
Always stay in character.
Reply according to that personality.
Keep your answers interesting and natural.
"""

    with st.spinner("Thinking..."):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{instruction}\n\nUser: {prompt}"
            )

            answer = response.text

        except Exception as e:
            answer = f"Error: {e}"

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer) 
