import decouple
from passlib.context import CryptContext
from sqlmodel import create_engine

# JWT константы
JWT_SECRET_KEY = decouple.config("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Иницаализация алгоритма хеширования пароля
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Параметры базы данных sqlite
postgresql_url = f"""postgresql://{decouple.config("DB_NAME")}:{decouple.config("DB_PASSWORD")}@localhost:5432/brainrot_db"""
engine = create_engine(postgresql_url)