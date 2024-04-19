from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional
from app.database import SessionLocal
from app.models import Persona, Vehiculo, Oficial
from datetime import datetime


# User BaseModel
class User(BaseModel):
    __tablename__ = "user"
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    is_superuser: bool = False
    is_active: bool = True
    hash_password: str



# Schema para crear una nueva persona
class PersonaCreate(BaseModel):
    nombre: str
    correo: EmailStr

    @validator('nombre')
    def check_nombre_unique(cls, nombre):
        db = SessionLocal()
        existing_persona = db.query(Persona).filter(Persona.nombre == nombre).first()
        if existing_persona:
            raise ValueError('Ya existe una persona con ese nombre')
        return nombre

    @validator('correo')
    def check_correo_unique(cls, correo):
        db = SessionLocal()
        existing_persona = db.query(Persona).filter(Persona.correo == correo).first()
        if existing_persona:
            raise ValueError('Ya existe una persona con ese correo electrónico')
        return correo


# Schema para actualizar una persona existente
class PersonaUpdate(BaseModel):
    nombre: Optional[str]
    correo: Optional[str]

# Schema para representar una persona completa (incluyendo su ID)
class PersonaBase(BaseModel):
    id: int
    nombre: str
    correo: str

    class Config:
        orm_mode = True

# Definición del modelo Pydantic para Vehiculo


class VehiculoCreate(BaseModel):
    id: int
    placa_patente: str
    marca: str
    color: str
    propietario_id: int

    @validator('placa_patente')
    def check_placa_patente_unique(cls, placa_patente):
        db = SessionLocal()
        existing_placa_patente = db.query(Vehiculo).filter(Vehiculo.placa_patente == placa_patente).first()
        if existing_placa_patente:
            raise ValueError('Ya existe un vehiculo con esa placa')
        return placa_patente


class VehiculoUpdate(BaseModel):
    color: Optional[str]
    propietario_id: Optional[int]


class VehiculoBase(BaseModel):
    id: int
    placa_patente: str
    marca: str
    color: str
    propietario_id: int

    class Config:
        orm_mode = True


####### Definición del modelo Pydantic para Oficial #######

class OficialCreate(BaseModel):
    id: int
    nombre: str
    identificador: str
    @validator('nombre')
    def check_nombre_unique(cls, nombre):
        db = SessionLocal()
        existing_persona = db.query(Oficial).filter(Oficial.nombre == nombre).first()
        if existing_persona:
            raise ValueError('Ya existe una oficial con ese nombre')
        return nombre

    @validator('identificador')
    def check_identificador_unique(cls, identificador):
        db = SessionLocal()
        existing_identificador = db.query(Oficial).filter(Oficial.identificador == identificador).first()
        if existing_identificador:
            raise ValueError('Ya existe un oficial con ese identificador')
        return identificador

class OficialUpdate(BaseModel):
    id: Optional[int]
    nombre: Optional[str]
    identificador: Optional[str]

    class Config:
        orm_mode = True

class OficialBase(BaseModel):
    id: int
    nombre: str
    identificador: str

    class Config:
        orm_mode = True


# modelo para infraccion 
class InfraccionCreate(BaseModel):
    placa_patente: str
    timestamp: datetime
    comentarios: Optional[str]
 
class InfraccionUpdate(BaseModel):
    placa_patente: str
    timestamp: datetime
    comentarios: Optional[str]

class InfraccionBase(BaseModel):
    placa_patente: str
    timestamp: datetime
    comentarios: Optional[str]
    class Config:
        orm_mode = True


class InformeBase(BaseModel):
    correo: str
    class Config:
        orm_mode = True

