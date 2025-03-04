from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

fake_db = {}

class Profile(BaseModel):
    username: str
    followers_count: int
    target: int 

@app.get("/followers/{username}")
def get_followers(username: str):
    
    if username not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, **fake_db[username]}

@app.post("/set_alert")
def set_alert(data: Profile):
    if data.username not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    fake_db[data.username]["target"] = data.target
    return {"message": f"🚨 Alert set for {data.username} at {data.target} followers!"}
