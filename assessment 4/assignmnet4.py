from pathlib import Path
from urllib.parse import quote
import random
import requests
import streamlit as st

width = 512
height = 512

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A glowing jellyfish cathedral floating above a neon city",
    "A steampunk dragon delivering mail through clouds",
    "A dreamlike library made of crystal and moonlight"
]

def build_image_url(prompt: str, width: int, height: int) -> str:
    encoded_prompt = quote(prompt.strip(), safe="")
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"


def save_image_bytes(image_bytes: bytes, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        handle.write(image_bytes)


st.set_page_config(page_title="Image Generator", page_icon="🖼️")
st.title("Image Generator")

magic_enhance = st.sidebar.checkbox(" ✨ Enable Magic Enhance")
width = st.sidebar.number_input("Image width", min_value=64, max_value=2048, value=512, step=64)
height = st.sidebar.number_input("Image height", min_value=64, max_value=2048, value=512, step=64)

prompt_input = st.text_input("Enter a prompt for the image:", placeholder="e.g. a futuristic city at sunset")

generate_clicked = st.button("Generate Image")
surprise_clicked = st.button(" 🎲 Surprise Me!")

if generate_clicked or surprise_clicked:
    if surprise_clicked:
        prompt_to_generate = random.choice(surprise_prompts)
        st.info(f"Surprise prompt selected: {prompt_to_generate}")
    else:
        if not prompt_input.strip():
            st.warning("Please enter a prompt first.")
            st.stop()
        prompt_to_generate = prompt_input

    if magic_enhance:
        prompt_to_generate = (
            prompt_to_generate
            + ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"
        )

    url = build_image_url(prompt_to_generate, width, height)
    st.info(f"Generating your image for: {prompt_to_generate}")

    response = None
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.RequestException:
        if magic_enhance:
            st.warning("Magic Enhance failed, retrying with the original prompt...")
            if surprise_clicked:
                prompt_to_generate = prompt_to_generate.split(", masterpiece")[0]
            else:
                prompt_to_generate = prompt_input
            url = build_image_url(prompt_to_generate, width, height)
            try:
                response = requests.get(url, timeout=60)
                response.raise_for_status()
            except requests.RequestException as exc2:
                st.error(f"Failed to download image: {exc2}")
                response = None
        else:
            st.error("Failed to download image with the current prompt.")
            response = None

    if response is None:
        st.stop()

    output_path = Path("goat.png")
    save_image_bytes(response.content, output_path)
    st.success(f"Image generated successfully and saved as {output_path}")
    st.image(output_path)

    with open(output_path, "rb") as handle:
        st.download_button(
            label="Download image",
            data=handle.read(),
            file_name=output_path.name,
            mime="image/png",
        )


