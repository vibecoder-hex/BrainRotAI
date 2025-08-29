import decouple
from passlib.context import CryptContext
from sqlmodel import create_engine

try:
    from .data_settings.object_storage import ImageStorage
except ImportError:
    from data_settings.object_storage import ImageStorage

# JWT константы
JWT_SECRET_KEY = decouple.config("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Иницаализация алгоритма хеширования пароля
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Параметры базы данных sqlite
postgresql_url = f"""postgresql://{decouple.config("DB_USER")}:{decouple.config("DB_PASSWORD")}@89fbd271ed2f1155e73a99ed.twc1.net:5432/brainrot_db"""
engine = create_engine(postgresql_url)

image_storage = ImageStorage("https://s3.twcstorage.ru",
                                 decouple.config("AWS_ACCESS_KEY_ID"),
                                 decouple.config("AWS_SECRET_ACCESS_KEY"),
                                 decouple.config("AWS_BUCKET_NAME"),
                                 'png'
                    )