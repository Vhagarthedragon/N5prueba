# Test N5 python dev
## sistema de registro de infracciones de tránsito en Python.

###  interfaz administrativa, donde puedan manejarse los registros:
- para poder acceder a ella puede usar esta direccion
- http://127.0.0.1:8000/docs
- en esta interfaz podra ver todos las api registradas, con los modelos base para saber que datos puedes crear, buscar, editar o eliminar

### generar token
- para generar el token debemos ir a http://127.0.0.1:8000/token, tendremos que enviar mediante peticion POST el sig Form:
- usuario y contraseña
- esto nos generara un Json con el token generado, el cual vencera 15 minutos despues de inactividad
-   `{
	"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxMzU2NDg5MH0.5RCl1snftFUrERQM3vnGFfRV9OUXdOb6hcA0dFYUXD8",
	"token_type": "bearer"
}`

### API que permita a una App usada por los oficiales de policía cargar una infracción a un vehículo. 
- Este sera el Json a mandar, para poder usar la api debes usar como autenticacion el metodo bearer token
  se debe enviar en el header

  `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxMzU2NDM3M30.Rdmoy2WkhT_o42ekcOeHGrnRjNaDUyiDh48sotfy45E`

  `{
    "placa_patente": "string",
    "timestamp": "2024-04-19T21:33:55.154Z",
    "comentarios": "string"
   }`

### genarar informe
- para poder generar un informe solo debemos acceder meiante post a esta url, agregando el correo en query de la url como muestro en este ejemplo, esta api
no necesita autenticacion ni token

- `http://127.0.0.1:8000/generar_informe/?correo=fer_cesar98%40hotmail.com'`
- esto nos dara como resultado un Json como el de este ejemplo, en caso de existir la persona y esta tenga infracciones:
- `[
  {
    "infractor": {
      "nombre": "Cesar Diaz",
      "id": 1,
      "correo": "fer_cesar98@hotmail.com"
    },
    "infracciones": [
      {
        "id": 2,
        "placa_patente": "LIP774",
        "timestamp": "2024-04-19T00:31:31",
        "comentarios": "string"
      },
      {
        "id": 3,
        "placa_patente": "LIP774",
        "timestamp": "2024-04-19T00:31:31",
        "comentarios": "Exceso de velocidad"
      }
    ]
  }
]`

## Analisis final y propuesta de arquitectura
- Para una aplicación como esta, una instancia EC2 podría ser más adecuada si la aplicación es grande y compleja, requiere un control detallado sobre el entorno y la infraestructura,
y tiene un tráfico constante o requiere una instancia siempre disponible. Sin embargo, si nuestra aplicación es más pequeña, consta de funciones independientes y tiene picos de tráfico impredecibles
 o invocaciones poco frecuentes, Lambda sería una opción más conveniente y rentable. En resumen, para nuestra aplicación, recomendaría comenzar con Lambda debido a su facilidad de uso, escalabilidad
automática y modelo de precios basado en el uso. Si más adelante surge la necesidad de un mayor control o capacidad de personalización, podríamos considerar migrar a una instancia EC2.

-para la base de datos seria RDS, un buen manejo de vpc por seguridad y cloudwatch para poder monitorear bien la app.

-propondria un sistema de logs, para mantener un buen registro de eventos, tambien un sistema de logs en las transacciones de la bd, si hablaramos de que esta app fuera real y llegara a ser usada por transito

-tambien pienso que los schemas y modelos de la bd hay que mejorarlos, hace falta mas datos y mejorar su estructura para garantizar una escalabilidad mejor, ademas de seguridad, dado que estaria registrado
la informacion de los comparendos, datos los cuales son delicados y de interes en general.

-tambien propondria migrar a futuro a django rest framework, por ser un framework mas robusto, en mi opinion con mejor orm, mejor manejo de apis, y mejor integracion con otras librerias y funcionalidades de python

- para el Frontend propondria usar vue.js o react.js, para poder tener mas funcionalidades que las basicas que pueden ofrecer las plantillas base de html y css, el tema responsive, el manejo de las peticiones al backend
scripts para mejorar la experiencia y el uso de la app.

-se podria separar a futuro en microservicios

-Esto me gustaria poder discutirlo de manera hipotetica con ustedes, seria interesante.

## por ultimo, les debo el container docker, debido a que trata de conectarse a la bd, primero antes de correr la imagen, se debe crear el archivo .env con las variable de entorno que se necesitan.
para eso deje un comando en cli. solo debes correr esto en el terminal 
`python cli.py`
