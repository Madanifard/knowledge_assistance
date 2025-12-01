from app.celery_app import celery_app
from app.utils.pdf_extractor import PDFExtractor
from app.db.sql_db import get_db
from app.db.queries.document_crud import DocumentCRUD


@celery_app.task(bind=True)
def extract_and_store_pdf(self, document_id):
    document = DocumentCRUD.get(get_db, document_id)

    output_dir = document.file_path + "/extracts"
    extractor = PDFExtractor(document.file_path, output_dir)

    metadata = extractor.export_all()

    DocumentCRUD.update_metadata(metadata)

    return {
        "document_id": document_id,
        "status": "OK"
    }
