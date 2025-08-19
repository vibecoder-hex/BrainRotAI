from pydantic import BaseModel
from typing import List


# Модель промпта
class PromptRequest(BaseModel): 
    prompt: str
    image_ratio: List[str]


# Модель токена
class Token(BaseModel):     
    access_token: str
    token_type: str

# Модель расшифрованного username токена
class TokenData(BaseModel):     
    username: str | None = None