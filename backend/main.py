from fastapi import FastAPI, Depends, HTTPException, status
from generation_model import generate
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Annotated, List

import jwt, decouple
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"]
                    )

JWT_SECRET_KEY = decouple.config("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "goyda": {
        "username": "goyda",
        "full_name": "Goyda",
        "email": "goyda@mail.ru",
        "hashed_password": "$2b$12$xNmI4yXJdgcktYt/L/znJ.SxoZ2fdW4HruHcK90hW8D2VtgTts5QO",
        "disabled": False
    }
}

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Верификация пароля с его хешем
def verify_password(plain_password, hashed_password): 
    return pwd_context.verify(plain_password, hashed_password)

# Классическая хеш-функция для пароля
def get_password_hash(password: str):   
    return pwd_context.hash(password)


# Модель промпта
class PromptRequest(BaseModel): 
    prompt: str
    image_ratio: List[str]


# Абстрактная модель пользователя
class User(BaseModel):     
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# Модель токена
class Token(BaseModel):     
    access_token: str
    token_type: str

# Модель расшифрованного username токена
class TokenData(BaseModel):     
    username: str | None = None


# Добавление хеша в User
class UserInDB(User):       
    hashed_password: str


# Функция запроса в базу данных для получения пользователя
def get_user(db, username: str):  
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Аутентификация пользователя, проверка хешей паролей и логина в бд
def authenticate_user(fake_db, username: str, password: str):  
    user = get_user(fake_db, username)
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
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Доп провека для поля active 
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Главный endpoint(заглушка)
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Endpoint для генерации изображения через YandexArtAPI
@app.post("/generate/")
async def generate_image(request: PromptRequest, current_user: Annotated[User, Depends(get_current_active_user)]):
    image_code = await generate(text=request.prompt, image_ratio = request.image_ratio)
    return {"result": image_code}

@app.post("/token/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):    # Endpoint логина: прием данных от клиента
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,                            # Аутентификация и генерация токена с заданным временем истечения
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

@app.get('/users/me')
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user