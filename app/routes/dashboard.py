from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from app.models import Persona, Vehiculo, Oficial, Infraccion
from app.routes.login import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi import Form


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer("/token")
templates = Jinja2Templates(directory="templates")



# Función para obtener la instancia de la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para mostrar el dashboard después de iniciar sesión
@router.post("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db), access_token: str = Form(...)):
    # Verificar si el token es válido
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        print(username)
        if not username:
            raise HTTPException(status_code=401, detail="No se pudo validar las credenciales", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar las credenciales", headers={"WWW-Authenticate": "Bearer"})

    # Obtener datos necesarios para el dashboard desde la base de datos
    oficiales = db.query(Oficial).all()
    personas = db.query(Persona).all()
    vehiculos = db.query(Vehiculo).all()
    infracciones = db.query(Infraccion).all()

    # Renderizar el template del dashboard con los datos obtenidos
    return templates.TemplateResponse("dashboard.html", {"request": request, "oficiales": oficiales, "personas": personas, "vehiculos": vehiculos, "infracciones": infracciones})


@router.post("/generar_informe/")
async def generar_informe(correo: str ,db: Session = Depends(get_db)):
    # Buscar la persona por su correo electrónico
    persona = db.query(Persona).filter(Persona.correo == correo).first()
    if persona is None:
        raise HTTPException(status_code=404, detail="La persona no fue encontrada")
    
    # Obtener todos los vehículos asociados a la persona
    vehiculos = db.query(Vehiculo).filter(Vehiculo.propietario_id == persona.id).all()

    # Obtener todas las infracciones asociadas a los vehículos de la persona
    infracciones = []
    for vehiculo in vehiculos:
        vehiculo_infracciones = db.query(Infraccion).filter(Infraccion.placa_patente == vehiculo.placa_patente).all()
        infracciones.extend(vehiculo_infracciones)

    # Formatear los datos de las infracciones en un formato JSON
    informe = []
    infracciones_json = []
    for infraccion in infracciones:
        infracciones_json.append({
            "id": infraccion.id,
            "placa_patente": infraccion.placa_patente,
            "timestamp": infraccion.timestamp.isoformat(),
            "comentarios": infraccion.comentarios,
        })
    informe.append({"infractor": persona, "infracciones": infracciones_json})


    return informe
