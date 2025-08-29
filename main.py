from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
try:
    from .routers.auth_endpoints import router as auth_router
    from .routers.generation_endpoints import router as generation_router
    from .routers.user_data_endpoints import router as user_data_router
    from .data_settings.database import create_db_and_tables
except ImportError:
    from routers.auth_endpoints import router as auth_router
    from routers.generation_endpoints import router as generation_router
    from routers.user_data_endpoints import router as user_data_router
    from data_settings.database import create_db_and_tables

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://127.0.0.1:8001", "http://127.0.0.1:8000"],
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
