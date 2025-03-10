from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db, DatabaseManager
from db.models import UserProfile

app = FastAPI()

class Profile(BaseModel):
    username: str
    followers_count: int
    target: int 

@app.get("/followers/{username}")
def get_followers(username: str, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.username == username).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": profile.username, "followers_count": profile.followers_count, "target": profile.alert_threshold}

@app.post("/set_alert")
def set_alert(data: Profile, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.username == data.username).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")

    
    profile.alert_threshold = data.target
    db.add(profile)
    db.commit()
    db.refresh(profile)  # Ensure the profile is refreshed after commit
    return {"message": f"🚨 Alert set for {data.username} at {data.target} followers!"}
