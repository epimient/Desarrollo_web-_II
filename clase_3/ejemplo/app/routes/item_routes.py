# ============================================================
# Rutas (endpoints) de items.
# Este archivo define las URLs de la API y conecta cada una
# con la función correspondiente del servicio.
#
# Las rutas NO saben cómo funciona Supabase.
# Solo reciben la petición HTTP y llaman al servicio.
# ============================================================

from uuid import UUID  # Para validar que los IDs sean UUID válidos.

# APIRouter permite agrupar rutas relacionadas.
# status contiene las constantes de códigos HTTP.
from fastapi import APIRouter, status

# Importamos los schemas para validar entradas y dar forma a las respuestas.
from app.schemas.item_schema import ItemCreate, ItemResponse, ItemUpdate

# Importamos el módulo de servicio que contiene la lógica de negocio.
from app.services import item_service


# Creamos un router con:
# - prefix="/items": todas las rutas empiezan con /items
# - tags=["items"]: en Swagger UI se agrupan bajo la etiqueta "items"
router = APIRouter(prefix="/items", tags=["items"])


# -----------------------------------------------
# POST /items/ → Crear un nuevo item.
# -----------------------------------------------
@router.post(
    "/",
    response_model=ItemResponse,  # La respuesta tendrá la forma de ItemResponse.
    status_code=status.HTTP_201_CREATED,  # Código 201 = "Recurso creado".
)
def create_item(item: ItemCreate):
    """
    Recibe los datos del item en el cuerpo de la petición (JSON).
    FastAPI valida automáticamente que cumplan con ItemCreate.
    Luego llama al servicio para insertarlo en la base de datos.
    """
    return item_service.create_item(item)


# -----------------------------------------------
# GET /items/ → Listar todos los items.
# -----------------------------------------------
@router.get(
    "/",
    response_model=list[ItemResponse],  # La respuesta es una LISTA de items.
)
def list_items():
    """
    No recibe parámetros. Devuelve todos los items de la tabla,
    ordenados del más reciente al más antiguo.
    """
    return item_service.list_items()


# -----------------------------------------------
# GET /items/{item_id} → Obtener un item por su ID.
# -----------------------------------------------
@router.get(
    "/{item_id}",
    response_model=ItemResponse,
)
def get_item(item_id: UUID):
    """
    Recibe el UUID del item desde la URL.
    FastAPI valida automáticamente que sea un UUID válido.
    Si no lo es (ejemplo: "abc123"), responde con error de validación.

    Convertimos el UUID a string con str() porque Supabase
    espera strings, no objetos UUID de Python.
    """
    return item_service.get_item(str(item_id))


# -----------------------------------------------
# PUT /items/{item_id} → Actualizar un item.
# -----------------------------------------------
@router.put(
    "/{item_id}",
    response_model=ItemResponse,
)
def update_item(item_id: UUID, item: ItemUpdate):
    """
    Recibe el UUID desde la URL y los campos a actualizar en el cuerpo.
    Solo se actualizan los campos que el usuario envíe.
    """
    return item_service.update_item(str(item_id), item)


# -----------------------------------------------
# DELETE /items/{item_id} → Eliminar un item.
# -----------------------------------------------
@router.delete("/{item_id}")
def delete_item(item_id: UUID):
    """
    Recibe el UUID desde la URL y elimina el item correspondiente.
    Devuelve un mensaje de confirmación.
    """
    return item_service.delete_item(str(item_id))
