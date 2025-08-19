from fastapi import APIRouter, Response
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api_service.data_settings.database import *
from api_service.auth_settings.jwt_auth import *
from ..vars import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/api/token/")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):    # Endpoint логина: прием данных от клиента
    user = authenticate_user(UserBase, form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,                            # Аутентификация и генерация токена с заданным временем истечения
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=30 * 60,  
        )
    return {"message": "Login successfull"}


@router.post('/api/logout/')
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "logout successfull"}