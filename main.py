import logging
import fastapi
import sqlite3
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Crea la base de datos
conn = sqlite3.connect("iot.db")

app = fastapi.FastAPI()

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   


class iot(BaseModel):
    id : int
    dispositivo : str
    valor : int



@app.get("/")
async def obtener_dispositivos():
    """Obtiene todos los contactos."""
    # TODO Consulta todos los contactos de la base de datos y los envia en un JSON
    c = conn.cursor()
    c.execute('SELECT * FROM iot;')
    response = []
    for row in c:
        iot = {"id":row[0],"dispositivo":row[1], "valor":row[2]}
        response.append(iot)
    return response




@app.get("/iot/{id}")
async def obtener_dispositivo(id: int):
    """Obtiene un dispositivo por su ID."""
    # Consulta el dispositivo por su ID
    c = conn.cursor()
    c.execute('SELECT * FROM iot WHERE id = ?', (id,))
    row = c.fetchone()

    if row is not None:
      
        valor = row[2]
        return valor
    else:
        
        return -1



@app.put("/iot/{id}/{valor}")
async def actualizar_dispositivo(id: int, valor: int):
    """Actualiza un dispositivo."""
    # Consulta el dispositivo por su ID antes de la actualización
    c = conn.cursor()
    c.execute('SELECT * FROM iot WHERE id = ?', (id,))
    row = c.fetchone()

    if row is not None:
        # Si se encuentra el dispositivo, realiza la actualización
        c.execute('UPDATE iot SET valor = ? WHERE id = ?', (valor, id))
        conn.commit()
        return valor
    else:
        return -1
