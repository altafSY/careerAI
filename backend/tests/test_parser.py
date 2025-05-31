import os
import pytest
from backend.services.parser import parse_resume

# Sample PDF location for testing
SAMPLE_RESUME_PATH = os.path.join(os.path.dirname(__file__), "testResources/TestResume.pdf")


@pytest.fixture(scope="module")
def sample_pdf_bytes():
    """
    Fixture to load a small sample resume PDF for testing.
    """
    if not os.path.exists(SAMPLE_RESUME_PATH):
        pytest.skip("Sample resume file not found.")
    with open(SAMPLE_RESUME_PATH, "rb") as f:
        return f.read()


def test_parse_resume_success(sample_pdf_bytes):
    """
    Tests if parse_resume correctly extracts data from a valid PDF.
    """
    result = parse_resume(sample_pdf_bytes)

    # Basic checks
    assert isinstance(result, dict), "Expected result to be a dictionary"
    assert "name" in result and "email" in result, "Expected at least name and email to be parsed"
    assert isinstance(result.get("skills"), list)


def test_parse_resume_empty_file():
    """
    Tests behavior when given an empty PDF file.
    """
    empty_content = b""
    with pytest.raises(Exception):
        parse_resume(empty_content)


def test_parse_resume_invalid_format():
    """
    Tests behavior with a non-PDF input.
    """
    fake_pdf = b"This is not a real PDF file"
    with pytest.raises(Exception):
        parse_resume(fake_pdf)