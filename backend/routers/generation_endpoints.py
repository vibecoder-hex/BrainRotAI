from generation_model.yandex_art_api import generate
from fastapi import APIRouter
from typing import Annotated

from backend.data_settings.database import *
from backend.auth_settings.jwt_auth import *

router = APIRouter()

# Главный endpoint(заглушка)
@router.get('/')
async def root():
    return {"message": "Hello World"}

# Endpoint для генерации изображения через YandexArtAPI
@router.post("/generate/")
async def generate_image(request: PromptRequest, current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    image_code = await generate(text=request.prompt, image_ratio = request.image_ratio)
    return {"result": image_code}