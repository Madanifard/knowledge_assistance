import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path


def extract_page_text(pdf_page):
    """Extract text from a pdfplumber page if possible."""
    try:
        text = pdf_page.extract_text()
        return text.strip() if text else None
    except Exception:
        return None


def ocr_page(file_path: str, page_number: int, dpi: int = 300, lang: str = "fas+eng"):
    """Perform OCR on a specific page of a PDF and return extracted text."""
    images = convert_from_path(
        file_path,
        dpi=dpi,
        first_page=page_number,
        last_page=page_number,
    )
    img = images[0]
    ocr_text = pytesseract.image_to_string(img, lang=lang)
    return ocr_text.strip()


def smart_extract_pdf_to_dicts(file_path: str):
    """
    Extract text from a PDF file using pdfplumber for text-based pages
    and Tesseract OCR for scanned/image-based pages.

    Returns:
        List[dict]: Each dict contains page_number, type ('text' or 'ocr'), and extracted text.
    """
    pages_output = []
    file_path = str(Path(file_path))

    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)

        for idx, page in enumerate(pdf.pages, start=1):
            text = extract_page_text(page)

            if text:
                pages_output.append({
                    "page_number": idx,
                    "type": "text",
                    "text": text,
                })
            else:
                ocr_text = ocr_page(file_path, idx)
                pages_output.append({
                    "page_number": idx,
                    "type": "ocr",
                    "text": ocr_text,
                })

    return pages_output


if __name__ == "__main__":
    # Example usage
    pdf_path = "html_tutorial.pdf"
    results = smart_extract_pdf_to_dicts(pdf_path)
    for page in results:
        print(page)
