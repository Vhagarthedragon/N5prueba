import typer
import subprocess

app = typer.Typer()

@app.command()
def create_env_file():

    comando_shell = "openssl rand -hex 32"
    resultado = subprocess.run(comando_shell, capture_output=True, text=True)
    secret_key = resultado.stdout.strip()
    SECRET_KEY = "SECRET_KEY= " + str(secret_key)
    """
    Crea un archivo .env con valores predeterminados.
    """
    env_content = """
    # Archivo de configuración de la aplicación
    DATABASE_URL="mysql://usuario:contraseña@localhost/dbname"
    ALGORITHM = HS256
    """ + SECRET_KEY
    with open(".env", "w") as env_file:
        env_file.write(env_content)

    typer.echo("Archivo .env creado con éxito")
    typer.echo("No olvides poner las credenciales de la BD mysql")

if __name__ == "__main__":
    app()