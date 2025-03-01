import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_API_KEY = os.getenv("BOT_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

    POSTGRES_DB = os.getenv("POSTGRES_DB", "socialdb")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

    # check for change each 60 seconds
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))  

config = Config()
