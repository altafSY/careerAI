from pyresparser import ResumeParser
import tempfile

def parse_resume(file_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    data = ResumeParser(tmp_path).get_extracted_data()
    return data
