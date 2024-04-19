from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import SessionLocal
from app.models import Infraccion
from app.schemas import InfraccionBase, InfraccionCreate, InfraccionUpdate

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer("/token")

# Función para obtener la instancia de la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cargar_infraccion/", response_model=InfraccionBase)
def create_infraccion(infraccion: InfraccionCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_infraccion = Infraccion(**infraccion.dict())
    db.add(db_infraccion)
    db.commit()
    db.refresh(db_infraccion)
    return db_infraccion

@router.get("/infraccion/{infraccion_id}", response_model=InfraccionBase)
def read_infraccion(infraccion_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    infraccion = db.query(Infraccion).filter(Infraccion.id == infraccion_id).first()
    if infraccion is None:
        raise HTTPException(status_code=404, detail="Infracción no encontrada")
    return infraccion

@router.put("/infraccion/{infraccion_id}", response_model=InfraccionBase)
def update_infraccion(infraccion_id: int, infraccion_update: InfraccionUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_infraccion = db.query(Infraccion).filter(Infraccion.id == infraccion_id).first()
    if db_infraccion is None:
        raise HTTPException(status_code=404, detail="Infracción no encontrada")
    for key, value in infraccion_update.dict().items():
        setattr(db_infraccion, key, value)
    db.commit()
    db.refresh(db_infraccion)
    return db_infraccion

@router.delete("/infraccion/{infraccion_id}")
def delete_infraccion(infraccion_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_infraccion = db.query(Infraccion).filter(Infraccion.id == infraccion_id).first()
    if db_infraccion is None:
        raise HTTPException(status_code=404, detail="Infracción no encontrada")
    db.delete(db_infraccion)
    db.commit()
    return {"message": "Infracción eliminada exitosamente"}
