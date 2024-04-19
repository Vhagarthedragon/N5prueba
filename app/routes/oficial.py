from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Oficial
from app.schemas import OficialBase, OficialCreate, OficialUpdate

router = APIRouter()


# controladores para los oficiales, como crear, actualizar y eliminar oficiales, pueden ir aquí


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer("/token")

# Función para obtener la instancia de la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/oficial/", response_model=OficialBase)
def create_oficial(oficial: OficialCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_oficial = Oficial(**oficial.dict())
    db.add(db_oficial)
    db.commit()
    db.refresh(db_oficial)
    return db_oficial

@router.get("/oficial/{oficial_id}", response_model=OficialBase)
def read_oficial(oficial_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    oficial = db.query(Oficial).filter(Oficial.id == oficial_id).first()
    if oficial is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    return oficial

@router.put("/oficial/{oficial_id}", response_model=OficialBase)
def update_oficial(oficial_id: int, oficial_update: OficialUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_oficial = db.query(Oficial).filter(Oficial.id == oficial_id).first()
    if db_oficial is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    for key, value in oficial_update.dict().items():
        setattr(db_oficial, key, value)
    db.commit()
    db.refresh(db_oficial)
    return db_oficial

@router.delete("/oficial/{oficial_id}")
def delete_oficial(oficial_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_oficial = db.query(Oficial).filter(Oficial.id == oficial_id).first()
    if db_oficial is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    db.delete(db_oficial)
    db.commit()
    return {"message": "Oficial eliminado exitosamente"}
