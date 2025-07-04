from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Request

from main import app, templates, bcrypt_context
from database.models import Usuario
from dependencies.dependencies import pegar_sessao
from schemas.schemas import UsuariosSchema, LoginSchema
from sqlalchemy.orm import Session
from datetime import timedelta

from route.auth_routes import autenticar_usuario, criar_token


account_router = APIRouter(prefix="/account", tags=["account"])


##PÁGINA HTML
@app.get("/sing_in", response_class=HTMLResponse)
async def cadastar(request: Request):
    return templates.TemplateResponse("singin.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page_request(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


##ROTAS
@account_router.post("/create_account")
async def criar_conta(usuario_schema: UsuariosSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    print(f"DEBUG: Dados recebidos: {usuario_schema.model_dump()}")
    if usuario:
        # ja existe um usuario com esse email
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso {usuario_schema.email}"}



@account_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais incorreta")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@account_router.post("/login-form")
async def login_form(dados_fomulario:OAuth2PasswordRequestForm = Depends() , session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_fomulario.username, dados_fomulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais incorreta")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }