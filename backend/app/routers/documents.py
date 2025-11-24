from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
import os

from app.db.queries.document_crud import DocumentCRUD
from app.db.sql_db import get_db
from app.schemas.document_schemas import DocumentOut

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ----------------------------
# Upload Document (Create)
# ----------------------------
@router.post("/upload", response_model=DocumentOut)
async def upload_document(
    user_id: int = Form(...),
    category_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["pdf", "md", "docx"]:
        raise HTTPException(400, "File type not allowed")

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # ذخیره فایل روی دیسک
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    document = await DocumentCRUD.create(
        db=db,
        user_id=user_id,
        category_id=category_id,
        name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_size,
    )

    return document


# ----------------------------
# Get by ID
# ----------------------------
@router.get("/{doc_id}", response_model=DocumentOut)
async def get_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    document = await DocumentCRUD.get(db, doc_id)
    if not document:
        raise HTTPException(404, "Document not found")

    return document


# ----------------------------
# List all
# ----------------------------
@router.get("/", response_model=list[DocumentOut])
async def list_documents(db: AsyncSession = Depends(get_db)):
    return await DocumentCRUD.list(db)


# ----------------------------
# Delete
# ----------------------------
@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):

    document = await DocumentCRUD.get(db, doc_id)
    if not document:
        raise HTTPException(404, "Document not found")

    # حذف فایل فیزیکی
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    await DocumentCRUD.delete(db, document)

    return {"message": "deleted"}
