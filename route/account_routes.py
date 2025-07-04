# C:\Users\Guilherme\PycharmProjects\Delivery_Pizza\Pizzaria\pycham\route\account_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Ajuste os imports baseados na sua estrutura real
from database.models import Usuario # Supondo que Usuario está em database/models.py
from dependencies.dependencies import pegar_sessao, bcrypt_context
from schemas.schemas import UsuariosSchema, LoginSchema # Supondo que schemas estão em schemas/schemas.py
from route.auth_routes import autenticar_usuario, criar_token # Autenticar_usuario e criar_token estão no auth_routes.py


# Altere o prefixo para "/auth" para corresponder ao que o frontend espera
# Ou mude o frontend para /account/... se preferir
account_router = APIRouter(prefix="/auth", tags=["auth"])

@account_router.post("/create_account", status_code=status.HTTP_201_CREATED)
async def criar_conta(usuario_schema: UsuariosSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    print(f"DEBUG: Dados recebidos: {usuario_schema.model_dump()}")
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        # Atenção aqui: o construtor do seu modelo Usuario pode precisar de argumentos nomeados
        # Certifique-se de que usuario_schema.ativo e usuario_schema.admin estão sendo fornecidos ou têm defaults
        # Novo Usuario é instanciado com argumentos nomeados para maior clareza e segurança
        novo_usuario = Usuario(
            nome=usuario_schema.nome,
            email=usuario_schema.email,
            senha=senha_criptografada,
            ativo=usuario_schema.ativo if usuario_schema.ativo is not None else True, # Exemplo de default
            admin=usuario_schema.admin if usuario_schema.admin is not None else False # Exemplo de default
        )
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso {usuario_schema.email}"}

@account_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }

@account_router.post("/login-form")
async def login_form(dados_fomulario:OAuth2PasswordRequestForm= Depends() , session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_fomulario.username, dados_fomulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais incorreta")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }