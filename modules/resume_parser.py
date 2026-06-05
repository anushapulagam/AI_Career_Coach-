import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            # Check if PDF is empty
            if len(reader.pages) == 0:
                return None, "❌ Your PDF has no pages. Please upload a valid resume."

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        # Check if text was extracted
        if not text.strip():
            return None, "❌ Could not extract text from your PDF. This usually means your resume is a scanned image. Please use a PDF created from Word or Google Docs."

        return text, None

    except PyPDF2.errors.PdfReadError:
        return None, "❌ Your PDF file is corrupted or password protected. Please upload a different file."
    except FileNotFoundError:
        return None, "❌ File not found. Please upload your resume again."
    except Exception as e:
        return None, f"❌ Unexpected error reading PDF: {str(e)}"

def clean_text(text):
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def get_resume_text(pdf_path):
    raw_text, error = extract_text_from_pdf(pdf_path)
    if error:
        return None, error
    clean = clean_text(raw_text)
    if len(clean) < 100:
        return None, "❌ Your resume text is too short. Please upload a complete resume with at least one page of content."
    return clean, None