from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker, Session

from main import SECRET_KEY, ALGORITHM, oauth2_schema
from passlib.context import CryptContext
from database.models import db, Usuario

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema) , session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))

    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Negado")
    return usuario
