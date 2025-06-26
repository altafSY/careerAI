from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.services.parser import save_profile, ProfileData   # <- same file

router = APIRouter()

@router.post("/upload_resume")
async def upload_resume(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    save_profile(db, user_id, content)
    return {"detail": "uploaded"}

@router.get("/resume_data/{user_id}")
def resume_data(user_id: int, db: Session = Depends(get_db)):
    rec = db.query(ProfileData).filter_by(user_id=user_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="No resume for this user")
    return rec.__dict__["_sa_instance_state"].dict  # or a Pydantic model