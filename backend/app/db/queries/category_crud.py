from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.db.models.category_model import Category
from typing import Sequence


# CREATE
async def create_category(db: AsyncSession, name: str) -> Category:
    category = Category(name=name)
    db.add(category)
    await db.commit()          # باید await کنی
    await db.refresh(category)  # باید await کنی
    return category


# READ by id
async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    return result.scalar_one_or_none()  # درست‌ترین روش برای گرفتن یک شیء یا None


# READ all with pagination
async def get_categories(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[Category]:
    result = await db.execute(
        select(Category).offset(skip).limit(limit)
    )
    return result.scalars().all()


# UPDATE
async def update_category(
    db: AsyncSession, category_id: int, new_name: str
) -> Category | None:
    # روش بهتر: مستقیم آپدیت کنیم بدون لود کردن آبجکت (بهینه‌تر)
    result = await db.execute(
        update(Category)
        .where(Category.id == category_id)
        .values(name=new_name)
        .returning(Category)
    )
    category = result.scalar_one_or_none()

    if category:
        await db.commit()
        return category
    else:
        return None

    # اگر حتماً می‌خوای از روش قبلی استفاده کنی:
    # category = await get_category(db, category_id)
    # if not category:
    #     return None
    # category.name = new_name
    # await db.commit()
    # await db.refresh(category)
    # return category


# DELETE
async def delete_category(db: AsyncSession, category_id: int) -> bool:
    result = await db.execute(
        delete(Category)
        .where(Category.id == category_id)
        .returning(Category.id)  # فقط برای چک کردن که حذف شده یا نه
    )
    deleted = result.scalar_one_or_none()
    if deleted:
        await db.commit()
        return True
    return False

    # یا روش ساده‌تر:
    # category = await get_category(db, category_id)
    # if not category:
    #     return False
    # await db.delete(category)
    # await db.commit()
    # return True
