from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.document_model import Document

class DocumentCRUD:

    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
        category_id: int,
        name: str,
        file_path: str,
        file_type: str,
        file_size: int
    ):
        document = Document(
            user_id=user_id,
            category_id=category_id,
            name=name,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
        )

        db.add(document)
        await db.commit()
        await db.refresh(document)
        return document

    @staticmethod
    async def get(db: AsyncSession, doc_id: int):
        result = await db.execute(
            select(Document).where(Document.id == doc_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list(db: AsyncSession):
        result = await db.execute(select(Document))
        return result.scalars().all()

    @staticmethod
    async def delete(db: AsyncSession, doc: Document):
        await db.delete(doc)
        await db.commit()
        return True
