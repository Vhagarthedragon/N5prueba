from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Vehiculo
from app.schemas import VehiculoBase, VehiculoCreate, VehiculoUpdate

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer("/token")

# Función para obtener la instancia de la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/vehiculo/", response_model=VehiculoBase)
def create_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_vehiculo = Vehiculo(**vehiculo.dict())
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

@router.get("/vehiculo/{vehiculo_id}", response_model=VehiculoBase)
def read_vehiculo(vehiculo_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    return vehiculo

@router.put("/vehiculo/{vehiculo_id}", response_model=VehiculoBase)
def update_vehiculo(vehiculo_id: int, vehiculo_update: VehiculoUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    for key, value in vehiculo_update.dict().items():
        setattr(db_vehiculo, key, value)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

@router.delete("/vehiculo/{vehiculo_id}")
def delete_vehiculo(vehiculo_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    db.delete(db_vehiculo)
    db.commit()
    return {"message": "Vehiculo eliminado exitosamente"}
