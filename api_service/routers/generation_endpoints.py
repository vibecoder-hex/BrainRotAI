from generation_model.yandex_art_api import generate
from fastapi import APIRouter
from typing import Annotated
from datetime import datetime

from sqlalchemy.exc import NoResultFound

from api_service.data_settings.database import *
from api_service.auth_settings.jwt_auth import *

router = APIRouter()

# Главный endpoint(заглушка)
@router.get('/api/')
async def root():
    return {"message": "Hello World"}

# Endpoint для генерации изображения через YandexArtAPI
@router.post("/api/generate/")
async def generate_image(request: PromptRequest, current_user: Annotated[UserBase, Depends(get_current_active_user)], session: SessionDep):
    image_code = await generate(text=request.prompt, image_ratio = request.image_ratio)
    image_to_base = Image(prompt=request.prompt, image="none", publish=datetime.now(), user=current_user.id)
    session.add(image_to_base)
    session.commit()
    return {"result": image_code}

@router.get("/api/get_images/")
async def get_images(session: SessionDep, current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    statement = select(Image, UserBase).where(Image.user == UserBase.id)
    results = session.exec(statement)
    result = {"image": [], "user": {}}
    for image, user in results:
        result["image"].append({"image_id": image.id,
                                "prompt": image.prompt,
                                "image_url": image.image,
                                "publish": image.publish
                                })
        result["user"]["username"] = user.username
    return {"result": result}

@router.delete("/api/delete_image/{image_id}/")
async def delete_image(image_id: int, session: SessionDep, current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    statement = select(Image).where(Image.id == image_id)
    try:
        result = session.exec(statement).one()
        session.delete(result)
        session.commit()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Not found in database")
    return {"message": "Delete Successfull"}