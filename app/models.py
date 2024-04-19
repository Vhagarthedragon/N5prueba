from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import  Mapped, mapped_column



# Definición de las clases SQLAlchemy
class Persona(Base):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))  # Ajusta la longitud a tus necesidades
    correo = Column(String(100))  # Ajusta la longitud a tus necesidades

    vehiculos = relationship("Vehiculo", back_populates="propietario")

class Vehiculo(Base):
    __tablename__ = "vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    placa_patente = Column(String(20), unique=True, index=True)  # Ajusta la longitud a tus necesidades
    marca = Column(String(50))  # Ajusta la longitud a tus necesidades
    color = Column(String(50))  # Ajusta la longitud a tus necesidades
    propietario_id = Column(Integer, ForeignKey('persona.id'))

    propietario = relationship("Persona", back_populates="vehiculos")


class Oficial(Base):
    __tablename__ = "oficial"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))  # Ajusta la longitud a tus necesidades
    identificador = Column(String(50), unique=True)  # Ajusta la longitud a tus necesidades
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Definir la relación con la tabla User
    user = relationship("User", back_populates="oficial")

### admin ###

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(length=255), nullable=False)
    hash_password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relación con la tabla Oficial
    oficial = relationship("Oficial", back_populates="user")

    def __str__(self):
        return self.username

    

class Infraccion(Base):
    __tablename__ = "infraccion"

    id = Column(Integer, primary_key=True, index=True)
    placa_patente = Column(String(length=10), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    comentarios = Column(String(length=100))

    def __str__(self):
        return f"Infraccion(id={self.id}, placa_patente={self.placa_patente}, timestamp={self.timestamp}, comentarios={self.comentarios})"



        

