from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import re
import tempfile
from pyresparser import ResumeParser
from backend.models.profileData import ProfileData
from backend.db.database import SessionLocal
from sqlalchemy.orm import Session
import json
from io import BytesIO, StringIO

def get_text(file_content: bytes) -> str:
    output_string = StringIO()
    laparams = LAParams(
        char_margin=2.0,
        line_margin=0.5,
        word_margin=0.1,  # ↓ reduces false tabs between words
        detect_vertical=False,  # ↓ disables vertical layout guessing
        all_texts=False
    )
    extract_text_to_fp(BytesIO(file_content), output_string, laparams=laparams, output_type='text', codec=None)
    return output_string.getvalue().replace('\t', ' ')  # extra safety: convert tabs to spaces

def extract_degree(education_text: str):
    degree_patterns = [
        r"(Bachelor(?:'s)? of [A-Za-z ]+)",
        r"(Master(?:'s)? of [A-Za-z ]+)",
        r"(B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|Ph\.?D\.?)",
        r"(Associate(?:'s)? of [A-Za-z ]+)"
    ]
    for pattern in degree_patterns:
        match = re.search(pattern, education_text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return None

def extract_college(education_text: str):
    college_pattern = r"(?:University|College|Institute|School of [A-Za-z]+|Polytechnic|Academy)[^\n,]*"
    match = re.search(college_pattern, education_text, re.IGNORECASE)
    return match.group(0).strip() if match else None

def parse_resume(file_content: bytes) -> dict:
    text = get_text(file_content)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    full_text = "\n".join(lines)

    name = lines[0] if lines else "Unknown"

    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text)
    email = email_match.group(0) if email_match else None

    phone_match = re.search(r"(\+?\d{1,2}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", full_text)
    phone = phone_match.group(0) if phone_match else None

    skills_match = re.search(r"(Skills|Technical Skills)\s*[:\-]?\s*\n(.*?)(\n[A-Z][a-z]+|\Z)", full_text,
                             re.DOTALL | re.IGNORECASE)
    skills_block = skills_match.group(2).strip() if skills_match else ""
    skills = [s.strip() for s in re.split(r"[\n,•·]", skills_block) if len(s.strip()) > 1]

    edu_match = re.search(r"Education\s*[:\-]?\s*(.*?)\n(?:[A-Z][a-z]+|\Z)", full_text, re.IGNORECASE | re.DOTALL)
    education = edu_match.group(1).strip() if edu_match else None

    degree = extract_degree(education)
    college = extract_college(education)

    exp_match = re.search(r"(Experience|Professional Experience|Work History)\s*[:\-]?\s*(.*)", full_text,
                          re.IGNORECASE | re.DOTALL)
    experience = exp_match.group(2).strip() if exp_match else ""

    designation = None
    company_names = None
    total_experience = None
    no_of_pages = None

    return {
        "name": name,
        "email": email,
        "mobile_number": phone,
        "skills": skills,
        "college_name": college,
        "degree": degree,
        "designation": designation,
        "experience": experience[:1500],  # Truncate long blobs
        "company_names": company_names,
        "no_of_pages": no_of_pages,
        "total_experience": total_experience
    }


def TEST(file_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    data = ResumeParser(tmp_path).get_extracted_data()
    return data

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_resume(parsed_skills: dict, user_id: int, db: Session = get_db):
    # Convert experience to string blob
    experience_blob = parsed_skills.get("experience")
    if isinstance(experience_blob, list):
        experience_blob = "\n".join(experience_blob)

    # Check if profile already exists
    profile = db.query(ProfileData).filter(ProfileData.user_id == user_id).first()

    if profile:
        # Update existing
        profile.name = parsed_skills.get("name", profile.name)
        profile.email = parsed_skills.get("email", profile.email)
        profile.mobile_number = parsed_skills.get("mobile_number", profile.mobile_number)
        profile.college = parsed_skills.get("college_name", profile.college)
        profile.degree = parsed_skills.get("degree", profile.degree)
        profile.designation = parsed_skills.get("designation", profile.designation)
        profile.company_names = parsed_skills.get("company_names", profile.company_names)
        profile.skills = json.dumps(parsed_skills.get("skills", []))
        profile.experience = experience_blob
    else:
        # Insert new
        profile = ProfileData(
            user_id=user_id,
            name=parsed_skills.get("name", "Unknown"),
            email=parsed_skills.get("email"),
            mobile_number=parsed_skills.get("mobile_number"),
            college=parsed_skills.get("college_name"),
            degree=parsed_skills.get("degree"),
            designation=parsed_skills.get("designation"),
            company_names=parsed_skills.get("company_names"),
            skills=json.dumps(parsed_skills.get("skills", [])),
            experience=experience_blob
        )
        db.add(profile)

    db.commit()

