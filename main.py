from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

load_dotenv(dotenv_path="environment/.env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000", # Se seu frontend estiver rodando aqui
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5500",
    "http://localhost:8001"
    # ADICIONE O ENDEREÇO ONDE SEU `signin.html` ESTIVER RODANDO/ABERTO
    # Em produção, este deve ser o domínio público do seu frontend (ex: "https://seusite.com")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite POST para sua rota de cadastro
    allow_headers=["*"], # Permite cabeçalhos como Content-Type
)

dirname = os.path.dirname(__file__)
app.mount("/styles", StaticFiles(directory=os.path.join(dirname, 'styles')), name="styles")
app.mount("/js", StaticFiles(directory=os.path.join(dirname, "javascript")), name="js_files")


templates = Jinja2Templates(directory="templates")

@app.get("/")
async def welcome_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
@app.get("/signin")
async def welcome_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/shopping")
async def login(request: Request):
    return templates.TemplateResponse("shopping.html", {"request": request})


oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from route.auth_routes import auth_router
from route.order_routes import order_router
from route.account_routes import account_router

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(account_router)

#uvicorn main:app --reload