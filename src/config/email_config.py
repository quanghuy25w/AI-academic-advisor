import os
from dotenv import load_dotenv

load_dotenv()

class EmailConfig:
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
    APP_PASSWORD = os.getenv("APP_PASSWORD", "")
