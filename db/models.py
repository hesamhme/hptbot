from sqlalchemy import Column, Integer, String, Enum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class SocialMediaType(PyEnum):
    X = "X"
    Instagram = "Instagram"
    TikTok = "TikTok"

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, nullable=False) # user key
    social_media = Column(Enum(SocialMediaType), nullable=False)   
    username = Column(String, nullable=False)  # username in social media
    alert_threshold = Column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint("telegram_id", "social_media", name="unique_user_social"),)

    def __repr__(self):
        return f"<UserProfile(telegram_id={self.telegram_id}, social_media={self.social_media.name}, username={self.username})>"
