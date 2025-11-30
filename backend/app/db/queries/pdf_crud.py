from datetime import datetime
from app.db.mongo_db import MongoConnection


class PdfRepository:
    def __init__(self, conn: MongoConnection = None, db:str = None):
        self.conn = conn or MongoConnection(db=db)
        self.files = self.conn.get_collection("pdf_files")
        self.pages = self.conn.get_collection("pdf_pages")

    def insert_pdf_meta(self, file_name, page_count):
        result = self.files.insert_one({
            "file_name": file_name,
            "page_count": page_count,
            "created_at": datetime.now()
        })
        return str(result.inserted_id)

    def insert_pdf_pages(self, file_id, pages):
        docs = [
            {
                "file_id": file_id,
                "page_number": p["page_number"],
                "type": p["type"],
                "text": p["text"],
                "created_at": datetime.now()
            }
            for p in pages
        ]
        self.pages.insert_many(docs)
        return len(docs)

    def get_pages_by_file(self, file_id):
        return list(self.pages.find({"file_id": file_id}))

    def get_file(self, file_id):
        return self.files.find_one({"_id": file_id})
