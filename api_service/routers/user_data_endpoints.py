from fastapi import APIRouter, Request
from typing import Annotated

from api_service.data_settings.database import *
from api_service.auth_settings.jwt_auth import *

router = APIRouter()

@router.get('/api/about_user')
def about_user(current_user: Annotated[UserBase, Depends(get_current_active_user)], request: Request):

    return {"user": current_user, "token": request.cookies.get("access_token")}