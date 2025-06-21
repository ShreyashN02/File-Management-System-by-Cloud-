import cloudinary
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("dqvqyqx5l"),
    api_key=os.getenv("377445867637447"),
    api_secret=os.getenv("WFwH4NeCAhnLRSIOMOXOhbrQprI"),
    secure=True
)
