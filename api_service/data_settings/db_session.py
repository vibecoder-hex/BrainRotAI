from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, select
from ..vars import engine

from api_service.data_settings.database import *


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Функция запроса в базу данных для получения пользователя
def get_user(db: UserBase, username: str, session: SessionDep):
    statement = select(db).where(db.username == username)
    results = session.exec(statement)
    return results.first()

