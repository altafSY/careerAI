from fastapi import APIRouter, UploadFile, File
from services.parser import parse_resume

router = APIRouter()

@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    parsed = parse_resume(content)
    return {"parsed_resume": parsed}
