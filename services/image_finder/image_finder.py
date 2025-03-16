import os
import requests
from flask import Blueprint, render_template, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key from .env
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Blueprint setup
image_finder_bp = Blueprint("image_finder", __name__)

# Function to fetch image from Unsplash
def fetch_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("urls", {}).get("regular", None)  # Get image URL
    return None

# Route to handle image search
@image_finder_bp.route("/image_finder", methods=["GET", "POST"])
def image_finder():
    image_url = None

    if request.method == "POST":
        user_input = request.form.get("query")  # Get user input
        if user_input:
            image_url = fetch_image(user_input)  # Fetch image

    return render_template("image_finder.html", image_url=image_url)
