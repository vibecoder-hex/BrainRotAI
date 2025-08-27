from generation_model.yandex_art_api import generate
from fastapi import APIRouter
from typing import Annotated
from datetime import datetime
from decouple import config
from random import choice

from sqlalchemy.exc import NoResultFound

from api_service.data_settings.database import *
from api_service.auth_settings.jwt_auth import *
from ..vars import image_storage

router = APIRouter()

# Главный endpoint(заглушка)
@router.get('/api/')
async def root():
    return {"message": "Hello World"}

# Endpoint для генерации изображения через YandexArtAPI
@router.post("/api/generate/")
async def generate_image(request: PromptRequest, current_user: Annotated[UserBase, Depends(get_current_active_user)], session: SessionDep):
    image_code = await generate(text=request.prompt, image_ratio=request.image_ratio)

    alph = "qwertyuiopasdfghjklzxcvbnm1234567890"
    random_filename = 'image_' + ''.join([choice(alph) for _ in range(30)]) + '.png'
    image_filepath = f'images/{random_filename}'
    image_storage.put_image_object(image_code, image_filepath)

    image_to_base = Image(prompt=request.prompt, image=image_filepath, publish=datetime.now(), user=current_user.id)
    session.add(image_to_base)
    session.commit()

    return {"db_id": image_to_base.id}

@router.get("/api/get_images/")
async def get_images(session: SessionDep, current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    statement = select(Image, UserBase).where(Image.user == UserBase.id)
    data = session.exec(statement)
    result = {"image": [], "user": {}}
    for image, user in data:
        result["image"].append({"image_id": image.id,
                                "prompt": image.prompt,
                                "image_url": image_storage.get_image_object(image.image),
                                "publish": image.publish
                                })
        result["user"]["username"] = user.username
    return {"result": result}

@router.delete("/api/delete_image/{image_id}/")
async def delete_image(image_id: int, session: SessionDep, current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    statement = select(Image, UserBase).where(Image.id == image_id).where(Image.user == UserBase.id)
    try:
        data = session.exec(statement).one()
        image = data[0]
        session.delete(image)
        image_storage.delete_image_object(image.image)
        session.commit()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found in database")
    return {"message": "Delete Successfull"}

@router.get('/api/get_current_image/{image_id}')
async def get_current_image(image_id: int, session: SessionDep, current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    statement = select(Image, UserBase).where(Image.id == image_id).where(Image.user == UserBase.id)
    try:
        data = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No found in database")
    image, user = data
    result = {"prompt": image.prompt,
              "image_url": image_storage.get_image_object(image.image),
              "publish": image.publish,
              "user": user.username
            }
    
    return  {"result": result}