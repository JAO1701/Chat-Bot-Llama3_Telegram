from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = 'ecommerce.db'

def connect_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def get_db_schema():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema[table_name] = cursor.fetchall()
    conn.close()
    return schema

@app.on_event("startup")
async def startup_event():
    try:
        conn = connect_db()
        print("Conexión a la DB exitosa")
        schema = get_db_schema()
        print("Esquema de la base de datos:", json.dumps(schema, indent=2))
        conn.close()
    except Exception as e:
        print("Error al conectar con la base de datos:", e)

@app.post("/message")
async def receive_message(request: Request):
    data = await request.json()
    message = data.get('message')
    print(f"Mensaje recibido: {message}")

    # Enviar el prompt a LLaMA 3
    try:
        llama_url = 'http://localhost:11434/api/generate'
        payload = {
            'model': 'llama3',
            'prompt': message,
            'options': {
                'max_tokens': 150
            }
        }
        response = requests.post(llama_url, json=payload, stream=True)
        
        llama_response = ""
        for line in response.iter_lines():
            if line:
                line_data = json.loads(line.decode('utf-8'))
                llama_response += line_data.get('response', '')
                if line_data.get('done'):
                    break
        
        print("Respuesta completa de LLaMA 3:", llama_response)

    except Exception as e:
        print(f"Error al comunicarse con LLaMA 3: {str(e)}")
        llama_response = "Error al obtener respuesta de LLaMA 3"

    # Conectar a la base de datos y realizar operaciones (este bloque es solo un ejemplo)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas")  # Cambia 'ventas' al nombre de tu tabla
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error en la base de datos: {str(e)}")
        rows = []

    return {"message": "Mensaje recibido", "llama_response": llama_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
