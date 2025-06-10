from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from sqlalchemy.orm import Session
from backend.services.parser import parse_resume, save_resume
from backend.models.profileData import ProfileData
from backend.models.user import User
from backend.db.database import SessionLocal
import json

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
        parsed = parse_resume(content)
        print(parsed)
        save_resume(user_id=user_id, parsed_skills=parsed, db=db)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing resume: {str(e)}"
        )

    return {"message": "Resume parsed and saved"}

@router.get("/resume_data/{user_id}")
def get_resume_data(user_id: int, db: Session = Depends(get_db)):
    record = db.query(ProfileData).filter(ProfileData.user_id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No resume data found for this user.")

    try:
        skills = json.loads(record.skills)
    except (TypeError, json.JSONDecodeError):
        skills = []

    return {
        "name": record.name,
        "email": record.email,
        "mobile_number": record.mobile_number,
        "college": record.college,
        "degree": record.degree,
        "designation": record.designation,
        "company_names": record.company_names,
        "skills": skills,
        "experience": record.experience,  # assuming this is a string blob
    }