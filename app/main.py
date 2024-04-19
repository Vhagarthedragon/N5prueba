from fastapi import FastAPI, Request
from app.database import engine
from app.routes import persona, vehiculo, oficial, infraccion, login, dashboard
from app.models import Base
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)


# Agrega las rutas a la aplicación
app.include_router(persona.router)
app.include_router(vehiculo.router)
app.include_router(oficial.router)
app.include_router(infraccion.router)
app.include_router(login.router)
app.include_router(dashboard.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/personasCrud", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("personas.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




