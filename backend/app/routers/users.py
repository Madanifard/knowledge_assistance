from fastapi import APIRouter, Depends

from utils.authentication import get_current_active_user
from ..schemas.user_schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user=Depends(get_current_active_user)):
    return current_user
