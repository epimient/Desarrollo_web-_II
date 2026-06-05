# ============================================================
# Servicio de items.
# Este archivo contiene las funciones que se comunican con Supabase.
# Las rutas (endpoints) llaman a estas funciones para ejecutar
# las operaciones CRUD en la base de datos.
#
# CRUD significa:
#   C = Create (crear)
#   R = Read   (leer)
#   U = Update (actualizar)
#   D = Delete (eliminar)
# ============================================================

# HTTPException sirve para devolver errores HTTP (404, 400, etc).
# status contiene las constantes de códigos HTTP para no usar números mágicos.
from fastapi import HTTPException, status

# Importamos el cliente de Supabase que creamos en database/supabase_client.py.
from app.database.supabase_client import supabase

# Importamos los schemas que definen la forma de los datos de entrada.
from app.schemas.item_schema import ItemCreate, ItemUpdate


# Nombre de la tabla en Supabase. Lo guardamos en una constante
# para no repetir el string "items" en cada función.
TABLE_NAME = "items"


# -----------------------------------------------
# CREATE: Insertar un nuevo item en la tabla.
# -----------------------------------------------
def create_item(item: ItemCreate) -> dict:
    """
    Recibe un objeto ItemCreate (validado por Pydantic) y lo inserta
    en la tabla "items" de Supabase.
    Devuelve el item creado con todos los campos (incluyendo id y fechas).
    """

    # model_dump() convierte el objeto Pydantic en un diccionario.
    # Supabase espera un diccionario, no un objeto de Python.
    # Ejemplo: {"name": "Mouse", "price": 85.90, "available": True}
    payload = item.model_dump()

    # .insert(payload) inserta una nueva fila en la tabla.
    # .execute() ejecuta la operación y devuelve la respuesta.
    response = supabase.table(TABLE_NAME).insert(payload).execute()

    # Si no hay datos en la respuesta, algo salió mal.
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear el item",
        )

    # response.data es una lista. Tomamos el primer (y único) elemento.
    return response.data[0]


# -----------------------------------------------
# READ: Listar todos los items.
# -----------------------------------------------
def list_items() -> list[dict]:
    """
    Consulta todos los items de la tabla.
    Los devuelve ordenados del más reciente al más antiguo.
    """

    response = (
        supabase.table(TABLE_NAME)
        .select("*")  # Seleccionar todas las columnas.
        .order("created_at", desc=True)  # Ordenar por fecha, más recientes primero.
        .execute()
    )

    # response.data es una lista de diccionarios (uno por cada fila).
    return response.data


# -----------------------------------------------
# READ: Obtener un item por su ID.
# -----------------------------------------------
def get_item(item_id: str) -> dict:
    """
    Busca un item específico usando su UUID.
    Si no lo encuentra, devuelve error 404.
    """

    response = (
        supabase.table(TABLE_NAME)
        .select("*")  # Seleccionar todas las columnas.
        .eq("id", item_id)  # Filtrar donde id sea igual al item_id.
        .execute()
    )

    # Si la lista está vacía, no existe un item con ese ID.
    if not response.data:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    # Devolvemos el primer (y único) resultado.
    return response.data[0]


# -----------------------------------------------
# UPDATE: Actualizar un item existente.
# -----------------------------------------------
def update_item(item_id: str, item: ItemUpdate) -> dict:
    """
    Actualiza solo los campos que el usuario envió.
    Si el usuario envía {"price": 99.90}, solo cambia el precio.
    Los demás campos quedan como estaban.
    """

    # model_dump() con estas opciones filtra los campos:
    # - exclude_unset=True: ignora campos que el usuario NO envió.
    # - exclude_none=True: ignora campos con valor None.
    # Así solo viajan al UPDATE los campos que realmente cambian.
    payload = item.model_dump(exclude_unset=True, exclude_none=True)

    # Si después de filtrar no queda nada, no hay nada que actualizar.
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay campos para actualizar",
        )

    # .update(payload) actualiza los campos indicados.
    # .eq("id", item_id) filtra la fila exacta a modificar.
    response = (
        supabase.table(TABLE_NAME)
        .update(payload)
        .eq("id", item_id)
        .execute()
    )

    # Si no hay datos en la respuesta, el item no existe.
    if not response.data:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    return response.data[0]


# -----------------------------------------------
# DELETE: Eliminar un item por su ID.
# -----------------------------------------------
def delete_item(item_id: str) -> dict:
    """
    Elimina un item de la tabla usando su UUID.
    Si no lo encuentra, devuelve error 404.
    """

    response = (
        supabase.table(TABLE_NAME)
        .delete()  # Operación de borrado.
        .eq("id", item_id)  # Filtrar la fila exacta.
        .execute()
    )

    # Si no hay datos, el item no existía.
    if not response.data:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    # Devolvemos un mensaje de confirmación.
    return {"message": "Item eliminado"}
