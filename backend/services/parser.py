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
from collections import defaultdict
from typing import List, Dict, Any

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

# ── 1) trivial field regexes ───────────────────────────────────
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s.\-]*)?(?:\(\d{3}\)|\d{3})[\s.\-]*\d{3}[\s.\-]*\d{4}")
NAME_RE  = re.compile(r"^[A-Z][A-Za-z'’\-\.]+(?:\s+[A-Z][A-Za-z'’\-\.]+){1,3}$")

# ── 2) section splitter ────────────────────────────────────────
SECTION_RE = re.compile(
    r""" ^\s*(?:[-–—•●▪‣◦∙]\s*)?
          (?P<hdr> (?:                                   # A) canonical keywords
              (?P<kw>
                  (?:technical\s+)?skills? |
                  (?:professional\s+)?experience |
                  work\s+history |
                  research\s+experience |
                  internships? |
                  projects? |
                  certifications? |
                  activities |
                  extracurriculars? |
                  leadership |
                  interests? |
                  education |
                  summary | objective | profile |
                  additional\s+information |
                  technologies | languages
              )\b.* )
            | [A-Z][A-Z0-9\s&/]{2,}                     # B) ALL-CAPS fallback
          )
          \s*:?\s*$ """,
    re.I | re.VERBOSE,
)

_NORMALISE = {
    **{k: "skills" for k in (
        "technical skills", "skills", "skill", "core competencies",
        "technologies", "languages",
        "skills & abilities", "skills & assets", "skills & interests", "skills & expertise")},
    **{k: "experience" for k in (
        "professional experience", "work history",
        "research experience", "internships", "internship")},
    "projects":       "projects",
    "certifications": "certifications",
    "activities":     "activities",
    "summary":        "summary", "objective": "summary", "profile": "summary",
    "interests":      "interests",
}

def _split_sections(lines: List[str]) -> Dict[str, List[str]]:
    secs, current = defaultdict(list), "preamble"
    for ln in lines:
        if (m := SECTION_RE.match(ln)):
            kw = m.group("kw") or m.group("hdr")
            current = _NORMALISE.get(kw.lower(), kw.lower())
            continue
        secs[current].append(ln)
    return secs


# ── 3) degree / college helpers ────────────────────────────────
_BS_RE = re.compile(r"(?:B\.?S\.?|Bachelor(?:'s)?\s+of\s+Science)\s*(?:in)?\s*"
                    r"(?P<maj>[A-Za-z&\s/+-]{3,}?)(?=[,/|-]|$)", re.I)
def extract_degree(edu: str) -> str|None:
    for ln in edu.splitlines():
        if (m := _BS_RE.search(ln)):
            maj = " ".join(w.capitalize() for w in m["maj"].split())
            return f"BS in {maj}"
    return None

def extract_college(edu: str) -> str|None:
    if (m := re.search(r"(University|College|Institute|Polytechnic|Academy)[^\n,]*", edu, re.I)):
        return m[0].strip()
    return None


# ── 4) skills cleaner ──────────────────────────────────────────
def _clean_bullets(txt: str) -> List[str]:
    return [p.strip() for p in re.split(r"[\n,;•·●\u2022]", txt) if len(p.strip()) > 1]


# ── 5) experience extractor  – smarter bullet/header detection ─
DATE_RE   = re.compile(r"\b(?:19|20)\d{2}\b|\bPresent\b")
BULLETS   = "•-–—▪‣◦∙·"

def _looks_like_header(line: str) -> bool:
    """Heuristic: header usually has a comma/location & at least one year/dash."""
    if DATE_RE.search(line):
        return True
    return bool(re.search(r"\bIntern|Assistant|Engineer|Research|Developer|Analyst\b", line))

def extract_experiences(block: str) -> List[Dict[str, Any]]:
    jobs, header, bullets = [], None, []
    for raw in block.splitlines():
        ln = raw.rstrip()
        if not ln.strip():
            continue

        stripped = ln.lstrip(BULLETS + " ").rstrip()

        # 1) Header line (even if it starts with a bullet)
        if _looks_like_header(stripped):
            if header:
                jobs.append({"header": header, "bullets": bullets})
            header, bullets = stripped, []
            continue

        # 2) Bullet continuation
        if header:
            if ln.lstrip().startswith(tuple(BULLETS)):
                bullets.append(stripped)
            elif bullets and ln.strip()[0].islower():        # wrapped line
                bullets[-1] += " " + ln.strip()
            else:                                            # accidental stray line → append
                bullets.append(stripped)
    if header:
        jobs.append({"header": header, "bullets": bullets})
    return jobs


# ── 6) main entry point ───────────────────────────────────────
def parse_resume(file_content: bytes) -> Dict[str, Any]:
    text  = get_text(file_content)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # simple one-liners
    name  = next((ln for ln in lines if NAME_RE.match(ln)), "Unknown")
    email = (EMAIL_RE.search(text) or [None])[0]
    phone = (PHONE_RE.search(text) or [None])[0]

    # sections
    secs       = _split_sections(lines)
    skills_blk = "\n".join(secs.get("skills", []))
    edu_blk    = "\n".join(secs.get("education", []))
    exp_blk    = "\n".join(secs.get("experience", []))

    return {
        "name":            name,
        "email":           email,
        "mobile_number":   phone,
        "skills":          _clean_bullets(skills_blk),
        "college_name":    extract_college(edu_blk),
        "degree":          extract_degree(edu_blk),
        "experiences":     extract_experiences(exp_blk),
        "experience_raw":  exp_blk[:2000],     # keep a preview
        # placeholders
        "designation":      None,
        "company_names":    None,
        "no_of_pages":      None,
        "total_experience": None,
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

def save_profile(session: Session, user_id: int, file_bytes: bytes) -> ProfileData:
    """
    Parse the résumé and upsert it into profile_data; returns the DB row.
    Assumes ProfileData.skills / experiences are JSONB (Postgres) or TEXT (SQLite).
    """
    parsed = parse_resume(file_bytes)

    record = session.query(ProfileData).filter_by(user_id=user_id).first()
    if not record:
        record = ProfileData(user_id=user_id)
        session.add(record)

    # flat columns
    record.name          = parsed["name"]
    record.email         = parsed["email"]
    record.mobile_number = parsed["mobile_number"]
    record.college       = parsed["college_name"]
    record.degree        = parsed["degree"]
    record.designation   = parsed["designation"]
    record.company_names = parsed["company_names"]

    # JSON columns  (if TEXT, SQLAlchemy will auto-cast str/list on Postgres ≥14)
    record.skills        = parsed["skills"]
    record.experiences   = parsed["experiences"]
    record.experience_raw = parsed["experience_raw"]

    session.commit()
    session.refresh(record)
    return record

