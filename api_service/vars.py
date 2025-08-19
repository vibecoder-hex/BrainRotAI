import decouple
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from sqlmodel import create_engine

# JWT константы
JWT_SECRET_KEY = decouple.config("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Иницаализация алгоритма хеширования пароля
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Обработчик JWT токена из запроса
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token/")

# Параметры базы данных sqlite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)