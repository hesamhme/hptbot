import random
import time
from db.fake_db import fake_db

def increase_followers():
    while True:
        for user, data in fake_db.items():
            data["followers_count"] += random.randint(50, 200)  
            target = data["target"] if data["target"] is not None else 999999
            print(f"📈 {user} -> {data['followers_count']} followers")
            if data["followers_count"] >= target:
                print(f"🚨 ALARM! {user} reached target: {target} 🚨")

        time.sleep(10) 


def start_scheduler():
    from threading import Thread
    t = Thread(target=increase_followers, daemon=True)
    t.start()
