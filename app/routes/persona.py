from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Persona
from app.schemas import PersonaCreate, PersonaUpdate, PersonaBase

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer("/token")

# Función para obtener la instancia de la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/persona/", response_model=PersonaBase)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_persona = Persona(**persona.dict())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

@router.get("/persona/{persona_id}", response_model=PersonaBase)
def read_persona(persona_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.put("/persona/{persona_id}", response_model=PersonaBase)
def update_persona(persona_id: int, persona_update: PersonaUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    for key, value in persona_update.dict().items():
        setattr(db_persona, key, value)
    db.commit()
    db.refresh(db_persona)
    return db_persona

@router.delete("/persona/{persona_id}")
def delete_persona(persona_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    db.delete(db_persona)
    db.commit()
    return {"message": "Persona eliminada exitosamente"}
