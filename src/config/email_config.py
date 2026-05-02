import os
from dotenv import load_dotenv

load_dotenv()

class EmailConfig:
<<<<<<< HEAD
    SENDER_EMAIL = "dinhtruongphong2752004@gmail.com"
    APP_PASSWORD = "hxhi ijay qlav gpxo"
=======
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
    APP_PASSWORD = os.getenv("APP_PASSWORD", "")
>>>>>>> temp-branch
