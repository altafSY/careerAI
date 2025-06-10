from sqlalchemy import Column, Integer, String, ForeignKey
from .user import User
from backend.db.base import Base
import json

class ProfileData(Base):
    __tablename__ = 'profile_data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    mobile_number = Column(String, nullable=True)
    college = Column(String, nullable=True)
    degree = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    company_names = Column(String, nullable=True)
    skills = Column(String)
    experience = Column(String)