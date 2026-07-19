import streamlit as st
import os
from google import genai
from dotenv import load_dotenv
import json
import edge_tts
import asyncio
import requests

load_dotenv()

st.title("📖 AI Visual Novel")

# Phase 1: The Director's Cut (UI & Configuration)
# Cache the Gemini client so Streamlit doesn't recreate it on every rerun
@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_ai_client()

# Phase 4.2: Multi-Media Rendering (TTS)
# Generate AI narration using Microsoft Edge TTS
async def generate_audio(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AndrewNeural"
    )

    await communicate.save("story.mp3")


# Phase 1: The Director's Cut (UI & Configuration)
# Configure the story settings from the sidebar
st.sidebar.header("Story Settings")

story_genre = st.sidebar.selectbox(
    "📚 Story Genre",
    [
        "Dark Fantasy",
        "Cyberpunk Thriller",
        "Post-Apocalyptic Survival",
        "Psychological Horror",
        "Space Opera",
        "Mythological Adventure",
        "Detective Mystery",
        "Time Travel"
    ],
    help="Choose the world your AI adventure will take place in."
)

art_style = st.sidebar.selectbox(
    "🎨 Art Style",
    [
        "Anime",
        "Cinematic Realism",
        "Studio Ghibli",
        "Comic Book",
        "Pixel Art",
        "Dark Gothic",
        "Fantasy Concept Art",
        "Oil Painting"
    ],
    help="Choose the artistic style for AI-generated illustrations."
)

start_story = st.sidebar.button("🎮 Start New Story")


# Phase 1: The Director's Cut (UI & Configuration)
# Create a persistent Gemini chat session
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash"
    )


# Phase 2: The Structured JSON Engine
# Generate a new interactive story and parse the AI's JSON response
if start_story:
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash"
    )

    # Phase 5: Graceful Failures
    # Prevent the app from crashing if the Gemini API fails
    try:
        response = st.session_state.gemini_chat.send_message(
            f"""
            Start a {story_genre} interactive visual novel.
            The image_prompt should be a detailed prompt for generating an image in {art_style} style.
            The story_text should be written in a cinematic, immersive narration style suitable for spoken narration.
            Keep paragraphs reasonably short and natural for text-to-speech.
            Respond ONLY with valid JSON.
            The JSON must contain:
            {{
                "story_text": "...",
                "image_prompt": "...",
                "options": [
                    "...",
                    "...",
                    "..."
                ]
            }}

            Do not wrap the response in markdown.
            Do not include explanations.
            Return only valid JSON.
            """
        )

        story = json.loads(response.text)
        st.session_state.story = story

    except Exception:
        st.toast("Couldn't start the story. Please try again.")


# Show instructions before the first story is created
if "story" not in st.session_state:
    st.info(
        "👈 Select a genre and art style from the sidebar, then click **Start New Story** to begin your adventure."
    )


# Display the current story once it exists
if "story" in st.session_state:

    story_text = st.session_state.story["story_text"]
    image_prompt = st.session_state.story["image_prompt"]
    options = st.session_state.story["options"]


    # Phase 4.1: Multi-Media Rendering (Visuals)
    # Generate and display the AI story illustration
    image_url = f"https://image.pollinations.ai/prompt/{image_prompt}"

    # Phase 5: Graceful Failures
    # Continue the story even if image generation fails
    try:
        image = requests.get(image_url)
        image.raise_for_status()

        st.image(
            image.content,
            caption="Story Scene",
            use_container_width=True
        )

    except Exception:
        st.toast("🖼️ Image server is busy, skipping visual...")


    # Phase 3: Dynamic UI Generation
    # Display the current story scene
    st.subheader("Story")
    st.write(story_text)


    # Phase 4.2: Multi-Media Rendering (TTS)
    # Generate and play AI narration
    try:
        asyncio.run(generate_audio(story_text))
        st.audio("story.mp3")

    # Phase 5: Graceful Failures
    # Continue the story even if audio generation fails
    except Exception:
        st.toast("🔊 Audio could not be generated.")


    # Phase 3: Dynamic UI Generation
    # Display interactive choices for the next scene
    st.subheader("Choose your next move")

    for option in options:
        if st.button(option):

            with st.spinner("Generating next scene..."):

                # Phase 5: Graceful Failures
                # Prevent the app from crashing while continuing the story
                try:
                    response = st.session_state.gemini_chat.send_message(
                        f"""
                        The player chose: {option}
                        Continue the {story_genre} story.
                        The image_prompt should describe the current scene in {art_style} style.
                        Write story_text as cinematic narration, as if it is being narrated in an audiobook.
                        Use vivid but concise descriptions and natural sentence flow.
                        Keep paragraphs short so they sound smooth when converted to speech.
                        Respond ONLY with valid JSON.
                        The JSON must contain:

                        {{
                            "story_text": "...",
                            "image_prompt": "...",
                            "options": [
                                "...",
                                "...",
                                "..."
                            ]
                        }}

                        Do not wrap the response in markdown.
                        Do not include explanations.
                        Return only valid JSON.
                        """
                    )

                    story = json.loads(response.text)
                    st.session_state.story = story

                    st.rerun()

                except Exception:
                    st.toast("📖 Couldn't continue the story. Please try again.")