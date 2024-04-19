from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Union
from jose import jwt, JWTError
import os
from dotenv import load_dotenv



router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer("/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(min=15)
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY ,algorithm=ALGORITHM)
    return token_jwt


def get_user(db, username):
    if username in db:
        user_data = db[username]
        return User(**user_data)
    return []

def verify_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)




def get_user_current(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = token_decode.get("sub")
        if username == None:
            raise HTTPException(status_code=401, detail="No se pudo validar las credenciales", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar las credenciales", headers={"WWW-Authenticate": "Bearer"})
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="No se pudo validar las credenciales", headers={"WWW-Authenticate": "Bearer"})
    return user

def get_user_disabled_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="usuario inactivo")
    return user


@router.post("/token")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # Buscar el usuario en la base de datos
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidaas")
    
    # Verificar la contraseña
    if not verify_password(form_data.password, user.hash_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidaas")

    # Generar el token de acceso
    access_token_expires = timedelta(minutes=25)  # Tiempo de expiración más corto
    access_token = create_token({"sub": user.username}, access_token_expires)

    # Devolver el token de acceso en un modelo Pydantic
    return {"access_token": access_token, "token_type": "bearer"}

