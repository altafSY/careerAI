from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from sqlalchemy.orm import Session
from backend.services.parser import parse_resume
from backend.models.profileData import ProfileData
from backend.models.user import User
from backend.database import SessionLocal

router = APIRouter()

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload_resume")
async def upload_resume(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Only .pdf and .docx files are allowed."
        )

    try:
        content = await file.read()
        parsed = parse_resume(content)  # e.g., returns list of skills like ["Python", "SQL"]

        for skill in parsed:
            db.add(ProfileData(user_id=user_id, skill=skill, experience="parsed"))

        db.commit()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing resume: {str(e)}"
        )

    return {"message": "Resume parsed and saved"}

@router.get("/resume_data/{user_id}")
def get_resume_data(user_id: int, db: Session = Depends(get_db)):
    records = db.query(ProfileData).filter(ProfileData.user_id == user_id).all()
    if not records:
        return {"skills": []}

    skills = [record.skill for record in records]
    return {"skills": skills}