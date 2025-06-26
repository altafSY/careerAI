# backend/models/profile_data.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB             # ← requires Postgres
from backend.db.base import Base

class ProfileData(Base):
    __tablename__ = "profile_data"

    id             = Column(Integer, primary_key=True)
    user_id        = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    # flat strings (same as before)
    name           = Column(String,  nullable=False)
    email          = Column(String)
    mobile_number  = Column(String)
    college        = Column(String)
    degree         = Column(String)
    designation    = Column(String)
    company_names  = Column(String)

    # NEW: real JSON columns
    skills        = Column(JSONB, default=list)          # eg. ["C++", "Kubernetes"]
    experiences   = Column(JSONB, default=list)          # list[{"header":…, "bullets":[…]}, …]

    # keep a preview of the raw block if you like
    experience_raw = Column(String)
