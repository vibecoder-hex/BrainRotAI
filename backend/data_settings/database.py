from backend.main import *
from backend.data_settings.series import *

fake_users_db = {
    "goyda": {
        "username": "goyda",
        "full_name": "Goyda",
        "email": "goyda@mail.ru",
        "hashed_password": "$2b$12$xNmI4yXJdgcktYt/L/znJ.SxoZ2fdW4HruHcK90hW8D2VtgTts5QO",
        "disabled": False
    }
}

# Функция запроса в базу данных для получения пользователя
def get_user(db, username: str):  
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)