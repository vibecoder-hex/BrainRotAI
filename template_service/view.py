from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8003", "http://localhost:8003", "http://127.0.0.1:8001"],  # Для разработки, в production укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="view.html")

@app.get('/login/', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get('/about_user/', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="about_user.html")