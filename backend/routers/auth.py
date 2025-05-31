from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.user import User
from backend.auth.utils import hash_password, verify_password
from pydantic import BaseModel

class UserCredentials(BaseModel):
    name: str
    username: str
    password: str
    email: str | None = None
    linkedin_url: str | None = None

class LoginCredentials(BaseModel):
    username: str
    password: str


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/register")
def register(credentials: UserCredentials, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=credentials.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(name=credentials.name,username=credentials.username, hashed_password=hash_password(credentials.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created", "user_id": user.id}


@router.post("/login")
def login(credentials: LoginCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user.id}
