import requests
from PIL import Image
import io
import random
import string

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer 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"}


# Function to send a request to the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
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
            image.show()
        else:
            print("Error: Failed to generate an image.")
            return None


# Main loop to take user input and generate images
while True:
    user_input = input("Enter your prompt (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    # Ask the user to select a style
    print("Select a style from the collection:")
    print("1. Cinematic")
    print("2. Anime")
    print("3. Digital Art")
    print("4. Photographic")
    print("5. Analog Film")
    print("6. Line Art")
    style_selection = input("Enter the style number: ")

    styles = {
        "1": "cinematic",
        "2": "anime",
        "3": "digital art",
        "4": "photographic",
        "5": "analog film",
        "6": "line art"
    }

    selected_style = styles.get(style_selection)

    if not selected_style:
        print("Invalid style selection. Please select a valid style.")
        continue

    num_images = int(input("Enter the number of different images to generate: "))
    generate_different_images(user_input, num_images, selected_style)