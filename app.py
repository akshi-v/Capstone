import streamlit as st
import requests
from PIL import Image
import io
import random
import string

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
HEADERS = {"Authorization": "Bearer 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"}


# Function to send a request to the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response


# Function to generate and display different images based on user input
def generate_different_images(prompt, num_images, selected_style):
    for i in range(num_images):
        # Add the selected style to the prompt with an explicit instruction
        prompt_with_style = f"Generate an image of {selected_style} {prompt}"

        response = query({"inputs": prompt_with_style})
        if response.status_code == 200:
            # Convert the response content (bytes) to an image
            image_bytes = response.content
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, use_column_width=True, caption=f"Generated Image {i + 1}")
        else:
            st.error("Error: Failed to generate an image.")


# Streamlit app
def main():
    st.title("Image Generator")

    user_input = st.text_input("Enter your prompt (or 'exit' to quit):")
    if user_input.lower() == 'exit':
        st.stop()

    # Ask the user to select a style
    style_selection = st.selectbox("Select a style from the collection:", [
        "Cinematic",
        "Anime",
        "Digital Art",
        "Photographic",
        "Analog Film",
        "Line Art"
    ])

    styles = {
        "Cinematic": "cinematic",
        "Anime": "anime",
        "Digital Art": "digital art",
        "Photographic": "photographic",
        "Analog Film": "analog film",
        "Line Art": "line art"
    }

    selected_style = styles.get(style_selection)

    if not selected_style:
        st.error("Invalid style selection. Please select a valid style.")
        return

    num_images = st.number_input("Enter the number of different images to generate:", min_value=1, value=1)

    if st.button("Generate Images"):
        generate_different_images(user_input, num_images, selected_style)


if __name__ == '__main__':
    main()
