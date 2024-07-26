import os
import requests
from PIL import Image
from io import BytesIO

IMAGE_DIR = "images"

# Ensure the images directory exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def save_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        image = Image.open(BytesIO(response.content))
        image_name = os.path.basename(image_url)
        image_path = os.path.join(IMAGE_DIR, image_name)

        image.save(image_path)
        print(f"Image saved to {image_path}")
        return image_path
    except Exception as e:
        print(f"Failed to save image from {image_url}: {e}")
        return None

def delete_images():
    for file_name in os.listdir(IMAGE_DIR):
        file_path = os.path.join(IMAGE_DIR, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
