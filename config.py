import cloudinary
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("enter cloud name"),
    api_key=os.getenv("enter api key"),
    api_secret=os.getenv("enter api secret"),
    secure=True
)
