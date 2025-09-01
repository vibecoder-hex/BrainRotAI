from fastapi import APIRouter
from typing import Annotated

from database import *
from jwt_auth import *

router = APIRouter()

@router.get('/api/users/me', response_model=AbstractUser)
def about_user(current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    return current_user