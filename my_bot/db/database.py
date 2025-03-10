from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config
from .models import Base, UserProfile, SocialMediaType
from sqlalchemy.exc import OperationalError

# database connections setting
DATABASE_URL = config.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

# initialize the database with Alembic (avoid direct create_all in production)
try:
    Base.metadata.create_all(engine)
except OperationalError as e:
    print(f"Database connection failed: {e}")

class DatabaseManager:
    def __init__(self):
        self.db = SessionLocal()

    def add_user_profile(self, telegram_id: int, social_media: str, username: str) -> UserProfile:
        if social_media not in SocialMediaType.__members__:
            raise ValueError(f"Invalid social media type: {social_media}")

        profile = self.db.query(UserProfile).filter_by(telegram_id=telegram_id, social_media=SocialMediaType[social_media]).first()
        if profile:
            profile.username = username
        else:
            profile = UserProfile(telegram_id=telegram_id, social_media=SocialMediaType[social_media], username=username)
            self.db.add(profile)
        self.db.commit()
        return profile

    def get_user_profiles(self, telegram_id: int):
        return self.db.query(UserProfile).filter_by(telegram_id=telegram_id).all()

    def delete_user_profile(self, telegram_id: int, social_media: str) -> bool:
        profile = self.db.query(UserProfile).filter_by(telegram_id=telegram_id, social_media=SocialMediaType[social_media]).first()
        if profile:
            self.db.delete(profile)
            self.db.commit()
            return True
        return False

    def get_user_by_username(self, username: str):
        return self.db.query(UserProfile).filter_by(username=username).first()

    def close(self):
        # there is no GC in python, so we need to close the connection
        self.db.close()

def get_db():
    # dependency injection for direct connection to the database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
