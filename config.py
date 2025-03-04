import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DATABASE_URL = os.getenv("DATABASE_URL")

    required_vars = ["BOT_TOKEN", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "DATABASE_URL"]
    for var in required_vars:
        if not locals()[var]:
            raise ValueError(f"Environment variable {var} is missing!")

    # check for change each 60 seconds
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))  

config = Config()
