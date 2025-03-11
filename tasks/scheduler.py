import random
import time
import logging
from threading import Thread
from db.fake_db import fake_db
from db.database import DatabaseManager
from telegram import Bot
from config import config
from tasks.alert_checker import check_alerts

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

db = DatabaseManager()
bot = Bot(token=config.BOT_TOKEN)

def increase_followers():
    logger.info("Starting the increase_followers task...")
    while True:
        for user, data in fake_db.items():
            old_count = data["followers_count"]
            increment = random.randint(50, 200)
            data["followers_count"] += increment
            new_count = data["followers_count"]
            logger.info(f"📈 {user} followers increased from {old_count} to {new_count} (+{increment})")
        time.sleep(10)

def start_increase_followers():
    t1 = Thread(target=increase_followers, daemon=True)
    t1.start()
    logger.info("Increase followers task started.")

def start_check_alerts():
    t2 = Thread(target=check_alerts, daemon=True)
    t2.start()
    logger.info("Alert checker started.")

def start_scheduler():
    start_increase_followers()
    start_check_alerts()