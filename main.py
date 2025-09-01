from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from auth_endpoints import router as auth_router
from generation_endpoints import router as generation_router
from user_data_endpoints import router as user_data_router
from database import create_db_and_tables

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://127.0.0.1:8001", "http://127.0.0.1:8000", "http://localhost:8000", 'https://vibecoder-hex-brainrotai-6cd6.twc1.net'],
                   allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                    expose_headers=["*"] 
                    )
app.include_router(auth_router)
app.include_router(generation_router)
app.include_router(user_data_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
