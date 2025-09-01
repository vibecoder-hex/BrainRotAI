from fastapi import APIRouter, Response, Form
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database import *
from jwt_auth import *
from vars import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

def authorize_user(user, response):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=30 * 60,
            secure=True,
            samesite="none",
            path="/"
    )
    
@router.post("/api/token/")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):    # Endpoint логина: прием данных от клиента
    user = authenticate_user(UserBase, form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,                            # Аутентификация и генерация токена с заданным временем истечения
            detail="Incorrect username or password"
        )
    authorize_user(user, response)
    return {"message": "Login successfull"}


@router.get('/api/logout/')
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "logout successfull"}


@router.post('/api/register')
async def register(username: Annotated[str, Form()],
                   fullname: Annotated[str, Form()],
                   email: Annotated[str, Form()],
                   password: Annotated[str, Form()],
                   repeat_password: Annotated[str, Form()], session: SessionDep, response: Response):
    if not validate_password(password, repeat_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid password: password is small or passwords does not match"
                            )
    hashed_password = get_password_hash(password)
    new_user = UserBase(username=username, full_name=fullname, email=email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()

    user = authenticate_user(UserBase, username, password, session)
    authorize_user(user, response)
    return {"message": "Registration successfull"}

def validate_password(pass1, pass2):
    if pass1 != pass2:
        return False
    if len(pass1) < 8:
        return False
    return True