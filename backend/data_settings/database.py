from sqlmodel import Field, SQLModel
from ..vars import engine

class AbstractUser(SQLModel):
    username: str
    full_name: str 
    email: str 


class UserBase(AbstractUser, table=True):
    id: int | None = Field(default = None, primary_key = True)
    username: str = Field(index = True)
    full_name: str = Field(index = True)
    email: str = Field(index = True)
    hashed_password: str = Field(index = True)
    disabled: bool = Field(index=True, default=False)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    