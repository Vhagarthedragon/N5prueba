from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
# Define la URL de conexión a la base de datos MySQL.
# Cambia 'username', 'password', 'hostname' y 'database_name' con tus propias credenciales y detalles de la base de datos.
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_CONNECTION")

# Crea una instancia de la clase declarative_base, que es la base para todas las clases de modelos de SQLAlchemy.
Base = declarative_base()

# Crea un motor de base de datos SQLAlchemy.
engine = create_engine(DATABASE_URL)

# Crea una sesión de base de datos para interactuar con la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
