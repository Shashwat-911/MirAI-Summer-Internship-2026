import random
from urllib.parse import quote

import requests
import streamlit as st

st.set_page_config(page_title="AI Image Studio", page_icon="🖼️")
st.title("🖼️ AI Image Studio")
st.write("Describe anything you can imagine, and watch it come to life.")

# Sidebar Settings
st.sidebar.title("Settings")

art_style = st.sidebar.selectbox(
    "Art Style",
    [
        "Realistic",
        "Anime",
        "Cyberpunk",
        "Fantasy",
        "Watercolor",
        "Pixel Art",
        "3D Render",
        "Oil Painting",
    ]
)

width = st.sidebar.slider("Width", min_value=256, max_value=1024, value=512, step=64)
height = st.sidebar.slider("Height", min_value=256, max_value=1024, value=512, step=64)

# Task 3: The "Magic Enhance" Toggle
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

prompt = st.text_input("Enter a prompt for the image:", placeholder="e.g. a futuristic city at sunset")

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon sleeping on a pile of gold in a crystal cave",
    "A steampunk owl mechanic fixing a robot",
    "A giant turtle carrying a floating city on its back",
]

col1, col2 = st.columns(2)
generate_clicked = col1.button("Generate Image")
surprise_clicked = col2.button("🎲 Surprise Me!")


def generate_image(final_prompt: str):
    full_prompt = f"{final_prompt}, {art_style} style"

    # Task 3: append magic enhance boost words if enabled
    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    encoded_prompt = quote(full_prompt.strip(), safe="")

    # Task 1: The Broken Sliders (URL Parameters) - now sending width & height
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"

    st.info(f"Generating your image for: {final_prompt}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        st.error(f"Failed to download image: {exc}")
        return

    st.success("Image generated successfully!")
    st.image(response.content)

    # Task 2: The File Extension Fix - dynamic filename with .png
    st.download_button(
        label="Download image",
        data=response.content,
        file_name=f"{art_style}_image.png",
        mime="image/png",
    )


# Task 4: The "Surprise Me!" Feature
if surprise_clicked:
    random_prompt = random.choice(surprise_prompts)
    generate_image(random_prompt)
elif generate_clicked:
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        generate_image(prompt)
