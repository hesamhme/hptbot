import random

fake_db = {}

def generate_fake_profiles(count: int):
    global fake_db
    fake_db = {} 
    for i in range(count):
        username = f"user_{i}"
        fake_db[username] = {
            "followers_count": random.randint(500, 5000),
            "target": random.randint(7000, 15000)
        }
    return fake_db
