# Use a base image appropriate for your programming language
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the source code into the container
COPY . .


RUN echo "preparando enviroment"
# Install dependencies
RUN pip install -r requirements.txt

RUN echo "Corriendo proyecto"

RUN echo "el primer usuario tienes que crearlo directo en la bd"

# Exponemos el puerto 80 para la aplicación FastAPI
EXPOSE 80
# Ejecutamos la aplicación FastAPI al iniciar el contenedor
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
