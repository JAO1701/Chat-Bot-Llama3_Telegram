﻿# Chat-Bot-Llama3_Telegram

Este código define una API RESTful utilizando FastAPI de Python. Su funcionalidad principal es recibir mensajes a través de una petición POST en el endpoint /message, enviar ese mensaje como un prompt a un modelo de lenguaje llamado LLaMA 3 (que está corriendo localmente en localhost), obtiene la respuesta del LLM LLaMA 3 y luego devuelve un mensaje de confirmación y la respuesta del modelo. También interactúa con una base de datos SQLite.

Además, el código realiza las siguientes acciones:
•	Configura CORS: Permite peticiones desde cualquier origen (*) para facilitar la interacción con la API desde diferentes dominios.
•	Conecta con SQLite: Establece una conexión con una base de datos SQLite llamada ecommerce.db.
•	Obtiene el esquema de la base de datos: Define una función para leer la estructura (tablas y columnas) de la base de datos SQLite.
•	Evento de inicio: Al iniciar la aplicación, intenta conectarse a la base de datos e imprime el esquema en la consola.
•	Ejemplo de consulta a la base de datos: Dentro del endpoint /message, incluye un bloque de código (a modo de ejemplo) que intenta consultar la tabla ventas de la base de datos.
•	Ejecución con Uvicorn: Utiliza uvicorn para correr la aplicación FastAPI en el host 0.0.0.0 y el puerto 5000.

Tecnologías Utilizadas:
•	FastAPI
•	Python
•	uvicorn
•	sqlite3
•	requests
•	fastapi.middleware.cors

