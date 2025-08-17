from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from backend.routers.auth_endpoints import router as auth_router
from backend.routers.generation_endpoints import router as generation_router
from .data_settings.database import create_db_and_tables

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"]
                    )
app.include_router(auth_router)
app.include_router(generation_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()