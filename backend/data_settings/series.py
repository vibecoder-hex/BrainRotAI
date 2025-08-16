from pydantic import BaseModel
from typing import List


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