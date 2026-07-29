from database import crear_tabla, get_connection
from fastapi import FastAPI, HTTPException
from models import Producto

app = FastAPI()

crear_tabla()

Valor_Dolar_Cop = 3205.87


@app.get("/")
def inicio():
  return {"message": "Bienvenido a la API de usuarios"}


@app.post("/Producto/")
def crear_producto(producto: Producto):
  precio_usd_fin = (
      producto.precio_usd
      if producto.precio_usd is not None
      else round(producto.precio_cop / Valor_Dolar_Cop, 2)
  )

  conn = get_connection()
  try:
    with conn:
      conn.execute(
          """
                INSERT INTO Producto (referencia, nombre, precio_cop, precio_usd, estado)
                VALUES (?, ?, ?, ?, ?)
            """,
          (
              producto.referencia,
              producto.nombre,
              producto.precio_cop,
              precio_usd_fin,
              int(producto.estado),
          ),
      )
  finally:
    conn.close()

  return {
      "message": "Producto creado exitosamente",
      "precio_usd_calculado": precio_usd_fin,
  }


@app.get("/Producto/")
def lista_productos():
  conn = get_connection()
  productos = conn.execute("SELECT * FROM Producto").fetchall()
  conn.close()
  return {"productos": [dict(producto) for producto in productos]}

@app.put("/Producto/{referencia}")
def actualizar_producto(referencia: str, producto: Producto):
  
  precio_usd_fin = (
      producto.precio_usd
      if producto.precio_usd is not None
      else round(producto.precio_cop / Valor_Dolar_Cop, 2)
  )

  conn = get_connection()  #[cite: 1]
  try:
    with conn:
      
      cursor = conn.execute(
          """
                UPDATE Producto 
                SET nombre = ?, precio_cop = ?, precio_usd = ?, estado = ?
                WHERE referencia = ?
            """,
          (
              producto.nombre,
              producto.precio_cop,
              precio_usd_fin,
              int(producto.estado),
              referencia,
          ),
      )

      if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el producto con referencia '{referencia}'",
        )

  finally:
    conn.close()

  return {
      "mensaje": "Producto actualizado exitosamente",
      "referencia_actualizada": referencia,
      "precio_usd_calculado": precio_usd_fin,
  }

@app.delete("/Producto/{referencia}")
def eliminar(referencia: str):
  conn = get_connection()
  conn.execute("DELETE FROM Producto WHERE referencia=?", (referencia,))
  conn.commit()
  conn.close()
  return {"mensaje": "Producto eliminado"}