from fastapi import APIRouter
from typing import Annotated

from api_service.data_settings.database import *
from api_service.auth_settings.jwt_auth import *

router = APIRouter()

@router.get('/api/about_user', response_model=AbstractUser)
def about_user(current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    return current_user