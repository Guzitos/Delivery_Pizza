from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

from starlette.staticfiles import StaticFiles

load_dotenv(dotenv_path="environment/.env")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

dirname = os.path.dirname(__file__)
app.mount("/assets", StaticFiles(directory=os.path.join(dirname, 'assets')), name="assets")

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from route.auth_routes import auth_router
from route.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

