import time
from db.database import DatabaseManager
from bot.main import logger
from telegram import Bot
from config import config
from db.models import UserProfile

db = DatabaseManager()
bot = Bot(token=config.BOT_TOKEN)

def send_telegram_message(chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text)
        logger.info(f"Sent message to {chat_id}: {text}")
    except Exception as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")

def check_alerts():
    logger.info("Starting check_alerts function...")
    while True:
        logger.info("Checking alerts...")
        profiles = db.db.query(UserProfile).filter(UserProfile.alert_threshold.isnot(None)).all()
        
        for profile in profiles:
            current_followers = profile.followers_count
            logger.info(f"Checking profile {profile.username} with {current_followers} followers...")

            if current_followers >= profile.alert_threshold:
                send_telegram_message(profile.telegram_id, f"🎉 {profile.username} has reached the target of {profile.alert_threshold} followers!")
                profile.alert_threshold = None  
                db.db.commit()
                db.db.expire(profile)  # Ensure the profile is refreshed after commit

        time.sleep(60)
