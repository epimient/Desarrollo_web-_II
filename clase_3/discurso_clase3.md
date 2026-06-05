# Clase 3 - FastAPI + Supabase

## Persistencia real para el CRUD construido en la Clase 2

**Fecha:** viernes 5 de junio de 2026  
**Tema central:** conectar una API de FastAPI con Supabase para guardar datos reales en PostgreSQL.

---

# 1. Idea principal de la clase

En la Clase 2 ya construimos una API con rutas, schemas y un CRUD básico. Esa API podía recibir peticiones, validar datos y responder JSON.

El problema era dónde vivían los datos.

En la Clase 2 los datos estaban en memoria:

```python
items_db = []
```

Eso servía para aprender rutas y operaciones CRUD, pero no sirve para una aplicación real porque la memoria se pierde cuando el servidor se apaga o se reinicia.

En la Clase 3 damos el siguiente paso:

```txt
Clase 2: FastAPI -> lista en memoria
Clase 3: FastAPI -> servicio -> Supabase -> PostgreSQL
```

La meta es que la API recuerde la información aunque cerremos la terminal, reiniciemos Uvicorn o abramos el proyecto otro día.

Si esta diferencia todavía no está clara, revisa [dudas/01_memoria_vs_persistencia.md](./dudas/01_memoria_vs_persistencia.md).

---

# 2. Hilo conductor: Clase 2 vs Clase 3

No empezamos desde cero. Usamos lo aprendido y lo hacemos más realista.

| Lo que ya teníamos en Clase 2 | Cómo evoluciona en Clase 3 |
|---|---|
| Schemas con Pydantic | Schemas con UUID, fechas y datos que vienen de la base de datos |
| Rutas con `APIRouter` | Rutas que delegan el trabajo a servicios |
| CRUD con `items_db = []` | CRUD conectado a Supabase |
| Proyecto organizado por carpetas | Nueva estructura con `core`, `database` y `services` |
| Pruebas en Swagger UI | Pruebas en Swagger UI verificando persistencia real |

La Clase 3 no vuelve a explicar desde cero qué es FastAPI, `BaseModel` o `APIRouter`. Los usamos como herramientas conocidas para resolver un nuevo problema: la persistencia.

---

# 3. Pregunta de apertura

Piensa en esta situación:

```python
items_db = []
```

Creamos tres productos desde Swagger. Luego apagamos el servidor y volvemos a ejecutar:

```bash
uvicorn app.main:app --reload
```

Pregunta:

> ¿Dónde quedaron esos tres productos?

Respuesta esperada:

> Se perdieron, porque estaban en una lista dentro de la memoria del proceso de Python.

Esto no es un error de FastAPI. Es una limitación de usar memoria temporal para guardar datos que deberían permanecer.

---

# 4. Memoria volátil y ciclo de vida del servidor

Cuando ejecutamos Uvicorn, Python abre un proceso. Dentro de ese proceso se crean variables, listas, objetos y funciones.

Mientras el proceso está vivo, una lista como `items_db` puede guardar información. Pero cuando el proceso termina, esa memoria se libera.

El ciclo es así:

```txt
1. Inicia Uvicorn
2. Python crea items_db = []
3. Llegan peticiones POST y se agregan datos
4. Se detiene o reinicia el servidor
5. Python crea una lista nueva
6. Los datos anteriores ya no existen
```

Por eso una lista en memoria es útil para practicar, pero no para persistir.

---

# 5. Analogía: hoja temporal vs sistema de registro

Imagina una biblioteca.

Si una persona anota los libros en una hoja suelta, la información puede servir durante un rato. Pero si la hoja se pierde, todo el registro desaparece.

Una base de datos es como el sistema oficial de la biblioteca. Cada registro queda guardado y se puede consultar después.

En nuestra API:

| Elemento | En la aplicación |
|---|---|
| Puerta de entrada | FastAPI |
| Registro permanente | Supabase |
| Motor de almacenamiento | PostgreSQL |
| Tabla principal | `items` |
| Fila individual | Un item |

---

# 6. CRUD aplicado a base de datos

CRUD significa crear, leer, actualizar y eliminar.

En la Clase 2 estas acciones modificaban una lista.

En la Clase 3 estas acciones modifican filas de una tabla.

| Verbo HTTP | Ruta | Operación en la tabla |
|---|---|---|
| `POST` | `/items` | Insertar una fila |
| `GET` | `/items` | Leer varias filas |
| `GET` | `/items/{id}` | Leer una fila por identificador |
| `PUT` | `/items/{id}` | Actualizar una fila |
| `DELETE` | `/items/{id}` | Eliminar una fila |

La ruta HTTP sigue siendo la entrada. Lo que cambia es el trabajo interno.

---

# 7. Supabase y PostgreSQL

Supabase nos permite crear un proyecto con una base de datos PostgreSQL en la nube.

Para esta clase nos interesan cuatro partes:

1. El editor SQL, donde creamos la tabla.
2. La tabla `items`, donde quedan guardados los registros.
3. La URL del proyecto, necesaria para conectarnos desde Python.
4. La API key, necesaria para autorizar la conexión.

FastAPI no guarda directamente los datos. FastAPI recibe la petición y llama a un servicio. El servicio usa el cliente de Supabase para ejecutar operaciones en PostgreSQL.

Si tienes dudas sobre la relación entre Supabase y PostgreSQL, revisa [dudas/02_supabase_postgresql.md](./dudas/02_supabase_postgresql.md).

---

# 8. Tabla `items` en SQL

En Supabase crearemos esta tabla:

```sql
create extension if not exists "pgcrypto";

create table if not exists public.items (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text,
  price numeric(10, 2) not null check (price >= 0),
  available boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_items_created_at
  on public.items (created_at desc);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_items_updated_at on public.items;

create trigger trg_items_updated_at
before update on public.items
for each row
execute function public.set_updated_at();
```

Esta tabla no solo guarda datos. También ayuda a proteger la calidad de esos datos.

---

# 9. Explicación de los campos de la tabla

## `id`

```sql
id uuid primary key default gen_random_uuid()
```

Es el identificador único de cada item. No lo escribe el usuario. PostgreSQL lo genera automáticamente.

Un UUID se ve así:

```txt
6f47a90d-10db-42f8-a934-cf6a7f1fd248
```

Sirve para identificar una fila sin depender de números manuales.

## `name`

```sql
name text not null
```

Es el nombre del item. Es obligatorio.

## `description`

```sql
description text
```

Es una descripción opcional.

## `price`

```sql
price numeric(10, 2) not null check (price >= 0)
```

Guarda el precio. `numeric(10, 2)` permite números con dos decimales. El `check` impide precios negativos.

## `available`

```sql
available boolean not null default true
```

Indica si el item está disponible. Si no enviamos este campo, queda en `true`.

## `created_at`

```sql
created_at timestamptz not null default now()
```

Guarda la fecha de creación. La genera la base de datos.

## `updated_at`

```sql
updated_at timestamptz not null default now()
```

Guarda la fecha de última actualización. El trigger `trg_items_updated_at` la actualiza cada vez que cambia una fila.

Si tienes dudas sobre UUID o fechas generadas por el servidor, revisa [dudas/03_uuid_fechas_servidor.md](./dudas/03_uuid_fechas_servidor.md).

---

# 10. Seguridad: variables de entorno

Para conectarnos a Supabase necesitamos:

```txt
SUPABASE_URL
SUPABASE_KEY
```

No debemos escribir esos valores directamente dentro del código.

Mal:

```python
SUPABASE_URL = "https://mi-proyecto.supabase.co"
SUPABASE_KEY = "clave-real-escrita-en-el-codigo"
```

Mejor:

```python
from app.core.config import settings

settings.supabase_url
settings.supabase_key
```

Las credenciales se guardan en `.env`, y `.env` se excluye del repositorio con `.gitignore`.

Si tienes dudas sobre esto, revisa [dudas/04_variables_entorno_gitignore.md](./dudas/04_variables_entorno_gitignore.md).

---

# 11. Archivos `.env` y `.gitignore`

Archivo `.env`:

```dotenv
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_clave_de_supabase
APP_NAME=API Clase 3
```

Archivo `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

Regla básica:

> El código puede subirse. Las claves privadas no.

---

# 12. Estructura evolucionada del proyecto

La estructura recomendada para esta práctica es:

```txt
app/
  main.py
  core/
    config.py
  database/
    supabase_client.py
  routes/
    item_routes.py
  schemas/
    item_schema.py
  services/
    item_service.py
.env
.gitignore
requirements.txt
```

Responsabilidad de cada carpeta:

| Carpeta | Responsabilidad |
|---|---|
| `core` | Configuración general del proyecto |
| `database` | Cliente de conexión con Supabase |
| `schemas` | Modelos de entrada y salida con Pydantic |
| `services` | Operaciones contra la base de datos |
| `routes` | Endpoints HTTP |

Si dudas sobre por qué se separan rutas y servicios, revisa [dudas/06_rutas_servicios_capas.md](./dudas/06_rutas_servicios_capas.md).

---

# 13. Instalación de dependencias

Desde la raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\activate

pip install fastapi uvicorn supabase pydantic-settings python-dotenv
pip freeze > requirements.txt
```

En Linux o macOS:

```bash
python -m venv .venv
source .venv/bin/activate

pip install fastapi uvicorn supabase pydantic-settings python-dotenv
pip freeze > requirements.txt
```

Dependencias clave:

| Paquete | Uso |
|---|---|
| `fastapi` | Crear la API |
| `uvicorn` | Ejecutar el servidor local |
| `supabase` | Conectarse a Supabase desde Python |
| `pydantic-settings` | Leer variables de entorno |
| `python-dotenv` | Soporte para archivo `.env` |

---

# 14. Configuración: `app/core/config.py`

Este archivo lee las variables de entorno.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    app_name: str = "API Clase 3"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
```

Explicación:

- `BaseSettings` crea un modelo de configuración.
- `supabase_url` y `supabase_key` se leen desde `.env`.
- `settings = Settings()` deja disponible un objeto reutilizable.

---

# 15. Conexión: `app/database/supabase_client.py`

Este archivo inicializa el cliente de Supabase.

```python
from supabase import Client, create_client

from app.core.config import settings


supabase: Client = create_client(
    settings.supabase_url,
    settings.supabase_key,
)
```

La idea es simple:

```txt
config.py lee las credenciales
supabase_client.py crea la conexión
item_service.py usa esa conexión
```

---

# 16. Schemas: `app/schemas/item_schema.py`

Los schemas definen qué datos entran y qué datos salen.

```python
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str | None = None
    price: float = Field(gt=0)
    available: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    available: bool | None = None


class ItemResponse(ItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
```

Explicación:

- `ItemCreate` representa el cuerpo para crear un item.
- `ItemUpdate` permite cambios parciales.
- `ItemResponse` incluye campos generados por la base de datos.
- `id` es `UUID`, no `int`.
- `created_at` y `updated_at` son fechas generadas por PostgreSQL.

Si tienes dudas sobre Pydantic o `model_dump()`, revisa [dudas/05_schemas_pydantic_model_dump.md](./dudas/05_schemas_pydantic_model_dump.md).

---

# 17. Servicio: crear y listar items

Archivo:

```txt
app/services/item_service.py
```

Primera parte:

```python
from fastapi import HTTPException, status

from app.database.supabase_client import supabase
from app.schemas.item_schema import ItemCreate, ItemUpdate


TABLE_NAME = "items"


def create_item(item: ItemCreate) -> dict:
    payload = item.model_dump()
    response = supabase.table(TABLE_NAME).insert(payload).execute()

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear el item",
        )

    return response.data[0]


def list_items() -> list[dict]:
    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data
```

Explicación:

- `item.model_dump()` convierte el modelo Pydantic en diccionario.
- `.insert(payload)` inserta una fila.
- `.select("*")` consulta todas las columnas.
- `.order("created_at", desc=True)` muestra primero los registros recientes.

---

# 18. Servicio: consultar, actualizar y eliminar

Continuación del mismo archivo:

```python
def get_item(item_id: str) -> dict:
    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .eq("id", item_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    return response.data[0]


def update_item(item_id: str, item: ItemUpdate) -> dict:
    payload = item.model_dump(exclude_unset=True, exclude_none=True)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay campos para actualizar",
        )

    response = (
        supabase.table(TABLE_NAME)
        .update(payload)
        .eq("id", item_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    return response.data[0]


def delete_item(item_id: str) -> dict:
    response = (
        supabase.table(TABLE_NAME)
        .delete()
        .eq("id", item_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    return {"message": "Item eliminado"}
```

Explicación:

- `.eq("id", item_id)` filtra la fila exacta.
- `exclude_unset=True` evita actualizar campos que el usuario no envió.
- `exclude_none=True` evita reemplazar valores existentes con `null`.
- Si Supabase no devuelve datos, asumimos que el item no existe.

---

# 19. Rutas: `POST` y `GET`

Archivo:

```txt
app/routes/item_routes.py
```

Primera parte:

```python
from uuid import UUID

from fastapi import APIRouter, status

from app.schemas.item_schema import ItemCreate, ItemResponse, ItemUpdate
from app.services import item_service


router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(item: ItemCreate):
    return item_service.create_item(item)


@router.get("/", response_model=list[ItemResponse])
def list_items():
    return item_service.list_items()
```

La ruta no sabe cómo funciona Supabase. Solo recibe la petición y llama al servicio.

---

# 20. Rutas por ID

Continuación de `app/routes/item_routes.py`:

```python
@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: UUID):
    return item_service.get_item(str(item_id))


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: UUID, item: ItemUpdate):
    return item_service.update_item(str(item_id), item)


@router.delete("/{item_id}")
def delete_item(item_id: UUID):
    return item_service.delete_item(str(item_id))
```

FastAPI valida el UUID antes de ejecutar la función. Si el valor de la URL no parece un UUID, la API responde con error de validación.

---

# 21. Punto de entrada: `app/main.py`

Archivo:

```python
from fastapi import FastAPI

from app.core.config import settings
from app.routes.item_routes import router as item_router


app = FastAPI(title=settings.app_name)


@app.get("/")
def health_check():
    return {"status": "ok", "service": settings.app_name}


app.include_router(item_router)
```

Sin esta línea:

```python
app.include_router(item_router)
```

las rutas de `items` no aparecen en Swagger UI.

---

# 22. Ejecutar y probar

Desde la carpeta donde está `app/`:

```bash
uvicorn app.main:app --reload
```

Luego abre:

```txt
http://127.0.0.1:8000/docs
```

Ahí deben aparecer:

```txt
POST   /items/
GET    /items/
GET    /items/{item_id}
PUT    /items/{item_id}
DELETE /items/{item_id}
```

---

# 23. Flujo completo de datos

Cuando se crea un item, el camino es:

```txt
Swagger UI
  -> POST /items/
  -> item_routes.py
  -> ItemCreate
  -> item_service.create_item()
  -> supabase_client.py
  -> tabla items en PostgreSQL
  -> respuesta JSON
```

Cada capa tiene una responsabilidad:

| Capa | Responsabilidad |
|---|---|
| Swagger UI | Enviar una petición de prueba |
| Ruta | Recibir HTTP y validar parámetros |
| Schema | Validar forma de los datos |
| Servicio | Ejecutar la operación de base de datos |
| Supabase | Persistir la información |

---

# 24. `model_dump()`

FastAPI recibe JSON y lo convierte en un objeto Pydantic.

Ejemplo:

```python
item = ItemCreate(
    name="Mouse",
    description="Mouse inalámbrico",
    price=85.90,
    available=True,
)
```

Pero Supabase necesita un diccionario:

```python
payload = item.model_dump()
```

Resultado:

```python
{
    "name": "Mouse",
    "description": "Mouse inalámbrico",
    "price": 85.90,
    "available": True,
}
```

Para actualizar usamos:

```python
payload = item.model_dump(exclude_unset=True, exclude_none=True)
```

Así solo viajan los campos enviados por el usuario.

---

# 25. Troubleshooting

## Error: `ModuleNotFoundError: No module named 'app'`

Probablemente estás ejecutando Uvicorn desde una carpeta incorrecta.

Solución:

```bash
uvicorn app.main:app --reload
```

debe ejecutarse desde la carpeta que contiene `app/`.

## Error: `Field required supabase_url`

Revisa:

1. Que exista `.env`.
2. Que esté en la raíz del proyecto.
3. Que las variables se llamen `SUPABASE_URL` y `SUPABASE_KEY`.
4. Que no estés ejecutando el servidor desde otra carpeta.

## Error: `relation "items" does not exist`

La tabla no existe o se creó en otro schema.

Solución:

1. Abre SQL Editor en Supabase.
2. Ejecuta el script de la tabla.
3. Verifica que la tabla exista en `public.items`.

## Error: no inserta datos

Puede estar relacionado con los permisos de la tabla. Verifica en Supabase que la tabla `items` exista en el schema `public` y que la API key que usas tenga permiso para insertar datos.

## Error: ID inválido

Si llamas:

```txt
GET /items/123
```

puede fallar porque `123` no es UUID. Usa un `id` real devuelto por Supabase.

Para una lista más amplia, revisa [dudas/08_errores_frecuentes.md](./dudas/08_errores_frecuentes.md).

---

# 26. Práctica guiada paso a paso

Esta sección es la ruta de desarrollo. Sigue los pasos en orden.

## Paso 1: crear el proyecto en Supabase

1. Entra a Supabase.
2. Crea un proyecto nuevo.
3. Espera a que el proyecto termine de inicializar.
4. Abre SQL Editor.
5. Ejecuta el script de la sección 8.
6. Verifica que exista la tabla `items`.

Resultado esperado:

```txt
Tabla public.items creada con columnas:
id, name, description, price, available, created_at, updated_at
```

## Paso 2: obtener URL y API key

En Supabase busca la configuración del proyecto y copia:

```txt
Project URL
API key
```

No pegues esas credenciales en archivos públicos.

## Paso 3: crear estructura de carpetas

Desde la raíz del backend:

```powershell
mkdir app
mkdir app\core
mkdir app\database
mkdir app\routes
mkdir app\schemas
mkdir app\services
```

Crea estos archivos:

```txt
app/main.py
app/core/config.py
app/database/supabase_client.py
app/routes/item_routes.py
app/schemas/item_schema.py
app/services/item_service.py
.env
.gitignore
requirements.txt
```

## Paso 4: crear entorno virtual e instalar dependencias

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install fastapi uvicorn supabase pydantic-settings python-dotenv
pip freeze > requirements.txt
```

## Paso 5: configurar `.env`

```dotenv
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_clave
APP_NAME=API Clase 3
```

## Paso 6: configurar `.gitignore`

```gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

## Paso 7: escribir `config.py`

Usa el código de la sección 14.

Prueba mental:

```txt
Si config.py funciona, settings.supabase_url y settings.supabase_key existen.
```

## Paso 8: escribir `supabase_client.py`

Usa el código de la sección 15.

Prueba mental:

```txt
Si el cliente se crea, Python ya tiene una conexión preparada hacia Supabase.
```

## Paso 9: escribir `item_schema.py`

Usa el código de la sección 16.

Verifica:

```txt
ItemCreate pide name y price.
ItemUpdate permite campos opcionales.
ItemResponse incluye id, created_at y updated_at.
```

## Paso 10: escribir `item_service.py`

Une el código de las secciones 17 y 18 en un solo archivo.

Orden de funciones:

```txt
create_item
list_items
get_item
update_item
delete_item
```

## Paso 11: escribir `item_routes.py`

Une el código de las secciones 19 y 20 en un solo archivo.

Verifica que exista:

```python
router = APIRouter(prefix="/items", tags=["items"])
```

## Paso 12: escribir `main.py`

Usa el código de la sección 21.

Verifica que exista:

```python
app.include_router(item_router)
```

## Paso 13: ejecutar el servidor

```powershell
uvicorn app.main:app --reload
```

Resultado esperado:

```txt
Application startup complete
Uvicorn running on http://127.0.0.1:8000
```

## Paso 14: abrir Swagger UI

Abre:

```txt
http://127.0.0.1:8000/docs
```

Verifica que aparezca el grupo `items`.

## Paso 15: probar `GET /`

Respuesta esperada:

```json
{
  "status": "ok",
  "service": "API Clase 3"
}
```

## Paso 16: probar `POST /items/`

Body:

```json
{
  "name": "Mouse inalámbrico",
  "description": "Mouse para computador portátil",
  "price": 85.9,
  "available": true
}
```

Resultado esperado:

```json
{
  "id": "uuid-generado-por-supabase",
  "name": "Mouse inalámbrico",
  "description": "Mouse para computador portátil",
  "price": 85.9,
  "available": true,
  "created_at": "fecha-generada",
  "updated_at": "fecha-generada"
}
```

Copia el `id` real para las siguientes pruebas.

## Paso 17: verificar en Supabase

En la tabla `items`, revisa que exista una fila nueva.

Esta verificación confirma que la API ya no depende de `items_db = []`.

## Paso 18: probar `GET /items/`

Debe listar los registros creados.

## Paso 19: probar persistencia

1. Detén Uvicorn con `Ctrl + C`.
2. Vuelve a ejecutar:

```powershell
uvicorn app.main:app --reload
```

3. Abre Swagger.
4. Ejecuta `GET /items/`.

Resultado esperado:

```txt
Los items siguen existiendo.
```

Ese es el punto central de la clase.

## Paso 20: probar `GET /items/{item_id}`

Usa el UUID que devolvió `POST`.

Resultado esperado:

```txt
La API devuelve solo ese item.
```

## Paso 21: probar `PUT /items/{item_id}`

Body:

```json
{
  "price": 99.9,
  "available": false
}
```

Resultado esperado:

```txt
Solo cambian price y available.
updated_at se actualiza automáticamente.
```

## Paso 22: probar `DELETE /items/{item_id}`

Resultado esperado:

```json
{
  "message": "Item eliminado"
}
```

Luego ejecuta `GET /items/{item_id}` y debe responder que el item no existe.

---

# 27. Reto práctico

Migra el backend de la Clase 2:

1. Localiza dónde usabas `items_db = []`.
2. Conserva los endpoints.
3. Crea la tabla en Supabase.
4. Crea la capa `services`.
5. Cambia la lógica de memoria por llamadas a Supabase.
6. Prueba cada endpoint en Swagger.
7. Reinicia Uvicorn y verifica que los datos sigan existiendo.

La entrega mínima debe demostrar:

```txt
POST /items/
GET  /items/
```

La entrega completa debe demostrar:

```txt
POST   /items/
GET    /items/
GET    /items/{item_id}
PUT    /items/{item_id}
DELETE /items/{item_id}
```

---

# 28. Criterios de evaluación

| Criterio | Valor |
|---|---:|
| CRUD completo conectado a Supabase | 35% |
| Estructura modular del proyecto | 20% |
| Manejo seguro de `.env` y `.gitignore` | 20% |
| Validaciones y respuestas correctas en Swagger UI | 15% |
| Evidencias ordenadas de funcionamiento | 10% |

Evidencias recomendadas:

1. Captura de la tabla creada en Supabase.
2. Captura de `.env` ocultando la clave.
3. Captura de Swagger con endpoints.
4. Captura de `POST /items/` funcionando.
5. Captura de `GET /items/` funcionando después de reiniciar Uvicorn.
6. Captura de `PUT` o `DELETE` funcionando.
7. Repositorio sin `.env`.

---

# 29. Cierre

En esta clase la API dejó de depender de memoria temporal.

Antes:

```txt
FastAPI -> items_db = []
```

Ahora:

```txt
FastAPI -> rutas -> servicios -> Supabase -> PostgreSQL
```

La idea más importante:

> Una API real no solo responde datos. También debe persistirlos de forma segura y organizada.
