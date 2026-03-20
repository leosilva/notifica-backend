import cloudinary
from cloudinary.uploader import upload_image
from dotenv import load_dotenv
import os

load_dotenv()


cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    secure=True,
)
