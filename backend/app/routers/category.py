from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.sql_db import get_db
from app.schemas.category_schemas import CategoryCreate, CategoryRead
from app.db.queries.category_crud import (
    create_category,
    get_category,
    get_categories,
    update_category,
    delete_category
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead)
async def create_category_api(data: CategoryCreate, db: Session = Depends(get_db)):
    category = await create_category(db, data.name)
    return category


@router.get("/", response_model=list[CategoryRead])
async def list_categories_api(db: Session = Depends(get_db)):
    categories = await get_categories(db)
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
def get_category_api(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category_api(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    category = await update_category(db, category_id, data.name)
    if not category:
        raise HTTPException(404, "Category not found")
    return category


@router.delete("/{category_id}")
async def delete_category_api(category_id: int, db: Session = Depends(get_db)):
    ok = await delete_category(db, category_id)
    if not ok:
        raise HTTPException(404, "Category not found")
    return {"detail": "Category deleted"}
