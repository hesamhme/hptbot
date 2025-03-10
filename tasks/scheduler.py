import random
import time
import logging
from threading import Thread
from db.database import DatabaseManager
from db.models import UserProfile
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
        profiles = db.db.query(UserProfile).all()
        for profile in profiles:
            old_count = profile.followers_count
            increment = random.randint(50, 200)
            profile.followers_count += increment
            new_count = profile.followers_count
            logger.info(f"📈 {profile.username} followers increased from {old_count} to {new_count} (+{increment})")
        db.db.commit()
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