from fastapi import FastAPI
from database import get_connection, crear_tabla
from models import Producto

app = FastAPI()

crear_tabla()

@app.get("/")
def inicio():
    return {"message": "Bienvenido a la API de usuarios"}

@app.post("/Producto/")        
def crear_producto(producto: Producto):
    conn = get_connection()
    conn.execute('''
        INSERT INTO Producto (referencia, nombre, precio_cop, precio_usd, estado)
        VALUES (?, ?, ?, ?, ?)
    ''', (producto.referencia, producto.nombre, producto.precio_cop, producto.precio_usd, int(producto.estado)))
    conn.commit()
    conn.close()
    return {"message": "Producto creado exitosamente"}


@app.get("/Producto/")
def lista_productos():
    conn = get_connection()

    productos = conn.execute('SELECT * FROM Producto').fetchall()

    conn.close()

    return {"productos": [dict(producto) for producto in productos]}