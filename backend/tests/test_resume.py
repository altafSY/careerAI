import os
from fastapi.testclient import TestClient
from backend.main import app
import io
from unittest.mock import patch


client = TestClient(app)

SAMPLE_RESUME_PATH = os.path.join(os.path.dirname(__file__), "testResources/TestResume.pdf")


def test_upload_resume_success():
    """
    Tests the /upload_resume route with a valid resume.
    """
    with open(SAMPLE_RESUME_PATH, "rb") as f:
        response = client.post(
            "/upload_resume",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "parsed_resume" in data
    assert isinstance(data["parsed_resume"], dict)


def test_upload_resume_invalid():
    """
    Tests the /upload_resume route with an invalid file format.
    """
    fake_file = b"This is not a PDF"
    response = client.post(
        "/upload_resume",
        files={"file": ("resume.txt", fake_file, "text/plain")},
    )

    assert response.status_code in (400, 422, 500)

def test_upload_resume_rejects_jpg():
    """
    Should return 400 when uploading a .jpg file.
    """
    fake_image = b"\xff\xd8\xff\xe0\x00\x10JFIF"  # JPEG file header
    response = client.post(
        "/upload_resume",
        files={"file": ("resume.jpg", io.BytesIO(fake_image), "image/jpeg")},
    )
    assert response.status_code == 400
    assert "Only .pdf and .docx files are allowed" in response.json()["detail"]

def test_upload_resume_parsing_exception_handled():
    """
    Should return 500 if parse_resume raises an exception (mocked).
    """
    with patch("backend.routers.resume.parse_resume") as mock_parser:
        mock_parser.side_effect = Exception("Mocked parsing failure")

        response = client.post(
            "/upload_resume",
            files={"file": ("resume.pdf", b"%PDF-1.4", "application/pdf")},
        )

    assert response.status_code == 500
    assert "Error parsing resume" in response.json()["detail"]