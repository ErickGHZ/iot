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
    "http://localhost:8080",
    "https://heroku-mysql-frontend-ac0fa64dec05.herokuapp.com",
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

@app.post("/dispositivos")
async def crear_dispositivo(iot: iot):
        c = conn.cursor()
        c.execute('INSERT INTO iot (id, dispositivo, valor) VALUES (?, ?, ?)',
                  (iot.id, iot.dispositivo, iot.valor))
        conn.commit()
        
        return iot

@app.get("/dispositivos")
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


@app.get("/dispositivos/{id}")
async def obtener_dispositivo(id: int):
    """Obtiene un contacto por su email."""
    # Consulta el contacto por su email
    c = conn.cursor()
    c.execute('SELECT * FROM iot WHERE id = ?', (id,))
    iot = None
    for row in c:
        iot = {"id":row[0],"dispositivo":row[1],"valor":row[2]}
    return iot


@app.put("/dispositivos/{id}")
async def actualizar_dispositivo(id: int, iot: iot):
    """Actualiza un contacto."""
    c = conn.cursor()
    c.execute('UPDATE iot SET dispositivo = ?, valor = ? WHERE id = ?',
              (iot.dispositivo, iot.valor, id))
    conn.commit()
    return iot

@app.delete("/dispositivo/{id}")
async def eliminar_dispositivo(id: int):
    """Elimina un contacto."""
    # TODO Elimina el contacto de la base de datos
    c = conn.cursor()
    c.execute('DELETE FROM iot WHERE id = ?', (id,))
    conn.commit()
    return {"mensaje":"Contacto eliminado"}