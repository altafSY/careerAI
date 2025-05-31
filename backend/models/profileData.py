from sqlalchemy import Column, Integer, String, ForeignKey
from backend.base import Base

class ProfileData(Base):
    __tablename__ = 'profile_data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill = Column(String, nullable=False)
    experience = Column(String)  # e.g., "2 years", "internship"