import cloudinary
from src.utills.setting import setting

cloudinary.config(
    cloud_name= setting.CLOUD_NAME,
    api_key= setting.API_KEY,
    api_secret= setting.API_SECRET
)