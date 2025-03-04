import time
from db.database import DatabaseManager
from bot.main import logger
from bot.utils import send_telegram_message  

db = DatabaseManager()

def check_alerts():
    while True:
        profiles = db.db.query(UserProfile).filter(UserProfile.alert_threshold.isnot(None)).all()
        
        for profile in profiles:
            current_followers = 100  

            if current_followers >= profile.alert_threshold:
                send_telegram_message(profile.telegram_id, f"🎉 you arrived to the point number of follower is {current_followers}.")
                profile.alert_threshold = None  
                db.db.commit()

        time.sleep(60)  
