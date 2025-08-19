from datetime import datetime, timezone, timedelta
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from typing import Annotated
from jwt.exceptions import InvalidTokenError

import jwt
from api_service.data_settings.database import *
from api_service.data_settings.series import *
from api_service.data_settings.db_session import *
from ..vars import *

# Верификация пароля с его хешем
def verify_password(plain_password, hashed_password): 
    return pwd_context.verify(plain_password, hashed_password)

# Классическая хеш-функция для пароля
def get_password_hash(password: str):    
    return pwd_context.hash(password)

# Аутентификация пользователя, проверка хешей паролей и логина в бд
def authenticate_user(db, username: str, password: str, session: SessionDep):  
    user = get_user(db, username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Генерация JWT-токена c довалением срока действия
def create_access_token(data: dict, expires_delta: timedelta | None = None):  
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Расшифровка JWT-токена и получение user-данных из бд для верификации токена от подделки
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(UserBase, username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user

# Доп провека для поля active 
async def get_current_active_user(current_user: Annotated[UserBase, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

