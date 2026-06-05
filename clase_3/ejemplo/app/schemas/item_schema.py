# ============================================================
# Schemas (esquemas) de datos para los items.
# Los schemas definen QUÉ datos entran a la API y QUÉ datos salen.
# Pydantic se encarga de validar automáticamente que los datos
# cumplan con las reglas que definimos aquí.
# ============================================================

from datetime import datetime  # Para manejar fechas y horas.
from uuid import UUID  # Para manejar identificadores UUID.

# BaseModel es la clase base de Pydantic para crear modelos.
# Field permite agregar validaciones extra (mínimo, máximo, etc).
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """
    Modelo base con los campos comunes de un item.
    Los otros modelos heredan de este para no repetir código.
    """

    # Nombre del item: obligatorio, mínimo 2 caracteres, máximo 80.
    name: str = Field(min_length=2, max_length=80)

    # Descripción: opcional (puede ser None si no se envía).
    description: str | None = None

    # Precio: obligatorio, debe ser mayor que 0.
    price: float = Field(gt=0)

    # Disponibilidad: por defecto es True (disponible).
    available: bool = True


class ItemCreate(ItemBase):
    """
    Schema para CREAR un item (POST /items/).
    Hereda todos los campos de ItemBase.
    No agrega campos extra porque para crear solo necesitamos
    name, description, price y available.

    Nota: el id, created_at y updated_at los genera la base de datos,
    por eso NO los pedimos aquí.
    """

    pass


class ItemUpdate(BaseModel):
    """
    Schema para ACTUALIZAR un item (PUT /items/{id}).
    Todos los campos son opcionales (None por defecto).
    Esto permite actualizar solo los campos que el usuario envíe,
    sin obligarlo a enviar todos cada vez.
    """

    # Cada campo es opcional (str | None, float | None, etc).
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    available: bool | None = None


class ItemResponse(ItemBase):
    """
    Schema para las RESPUESTAS de la API.
    Incluye los campos que genera la base de datos:
    id, created_at y updated_at.

    FastAPI usa este modelo para dar forma al JSON de respuesta.
    """

    # UUID generado por PostgreSQL (ejemplo: "6f47a90d-10db-42f8-a934-cf6a7f1fd248").
    id: UUID

    # Fecha de creación, generada automáticamente por la base de datos.
    created_at: datetime

    # Fecha de última actualización, actualizada por el trigger en PostgreSQL.
    updated_at: datetime
