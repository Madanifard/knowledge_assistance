from app.celery_app import celery_app
from app.utils.pdf_reader import smart_extract_pdf_to_dicts
from app.db.queries.pdf_crud import PdfRepository
from pathlib import Path


@celery_app.task(bind=True)
def extract_and_store_pdf(self, file_path, collection_name):
    repo = PdfRepository(db=collection_name)

    file_name = Path(file_path).name
    pages = smart_extract_pdf_to_dicts(file_path)

    file_id = repo.insert_pdf_meta(file_name, len(pages))
    count = repo.insert_pdf_pages(file_id, pages)

    return {
        "file_id": file_id,
        "pages_saved": count,
        "status": "OK"
    }
