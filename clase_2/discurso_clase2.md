# Modelos, Validaciones y Estructura Correcta

## 1. Propósito de la clase

En la clase anterior, los estudiantes pasaron de consumir una API externa
directamente con `requests` a crear una API sencilla con FastAPI. Ahora el
objetivo es dar el siguiente paso: dejar de escribir todo en un solo archivo y
comenzar a construir una API más ordenada, validada y fácil de mantener.

La idea central de esta clase es que los estudiantes entiendan que una API
profesional no solo "responde datos", sino que también:

- Valida lo que recibe.
- Controla lo que devuelve.
- Maneja errores correctamente.
- Organiza el código por responsabilidades.
- Documenta automáticamente sus endpoints.
- Separa rutas, esquemas, servicios y configuración.

FastAPI permite declarar modelos de entrada y salida con Pydantic. Estos modelos
ayudan a validar datos, generar documentación automática y controlar qué
información se expone en las respuestas.

FastAPI también permite declarar códigos de estado directamente en los
decoradores de las rutas usando `status_code`, y recomienda organizar
aplicaciones grandes en múltiples archivos usando `APIRouter`.

## 2. Objetivo de aprendizaje

Al finalizar la clase, el estudiante debe ser capaz de:

- Crear modelos Pydantic usando `BaseModel`.
- Validar datos de entrada usando tipos y `Field`.
- Diferenciar modelos de creación, actualización y respuesta.
- Usar `response_model` para controlar la salida de un endpoint.
- Definir códigos de estado HTTP en las rutas.
- Lanzar errores con `HTTPException`.
- Separar una API en carpetas.
- Usar `APIRouter` para dividir rutas por módulos.
- Explicar por qué no se debe construir toda la API en un solo archivo.

## 3. Pregunta inicial para abrir la clase

Puedes iniciar con esta pregunta:

> Si una API recibe cualquier dato sin validarlo, ¿qué problemas podrían
> aparecer?

Posibles respuestas esperadas:

- Datos incompletos.
- Campos con tipos incorrectos.
- Nombres vacíos o demasiado cortos.
- Errores difíciles de detectar.
- Respuestas inconsistentes.
- Exposición de datos que no deberían mostrarse.
- Código difícil de mantener.

Luego conectas con la idea principal:

> Hoy vamos a aprender a ponerle reglas a nuestra API. Vamos a decirle qué datos
> acepta, qué datos responde y cómo debe organizarse el proyecto para que no se
> vuelva un desorden.

## 4. Concepto 1: ¿Qué es Pydantic?

Pydantic es una librería usada por FastAPI para definir modelos de datos. Un
modelo representa la estructura que deben tener los datos que entran o salen de
la API.

En palabras simples:

> Pydantic nos permite decirle a Python: "este dato debe tener esta forma".

Por ejemplo, si una API recibe un producto, no queremos aceptar cualquier cosa.
Queremos que el producto tenga un nombre, una categoría, una descripción
opcional y, tal vez, una fuente externa.

### Ejemplo base

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str
    source: str | None = None
```

### Explicación línea por línea

```python
from pydantic import BaseModel, Field
```

Importamos `BaseModel` y `Field`.

- `BaseModel` permite crear modelos de datos.
- `Field` permite agregar reglas adicionales de validación, como longitud mínima
  o máxima.

```python
class ItemCreate(BaseModel):
```

Creamos una clase llamada `ItemCreate`.

Esta clase representa los datos que el cliente debe enviar cuando quiere crear
un nuevo item.

```python
name: str = Field(min_length=3, max_length=80)
```

El campo `name` debe ser texto.

Además, debe tener mínimo 3 caracteres y máximo 80 caracteres.

```python
description: str | None = None
```

El campo `description` puede ser texto o puede no enviarse.

La expresión `str | None` significa: "puede ser string o puede ser nulo".

El `= None` significa que el campo es opcional.

```python
category: str
```

El campo `category` es obligatorio y debe ser texto.

```python
source: str | None = None
```

El campo `source` es opcional. Puede servir para indicar de dónde viene el item,
por ejemplo `"local"` o `"pokeapi"`.

Pydantic valida los datos cuando se crea una instancia del modelo. Si los datos
no cumplen las reglas, se genera un error de validación.

La documentación oficial de Pydantic describe que los modelos permiten definir
campos con tipos y que la inicialización del modelo realiza parsing y
validación.

## 5. Concepto 2: ¿Por qué no usar el mismo modelo para todo?

Este punto es clave para la clase.

Muchos estudiantes intentan crear un único modelo y usarlo para crear,
actualizar y responder datos. Eso funciona al principio, pero es una mala
práctica.

### Ejemplo incorrecto

```python
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None
```

### Problema

Cuando el cliente crea un item, no debería enviar el `id`, porque el `id`
normalmente lo genera la base de datos o la lógica interna.

Pero cuando la API responde, sí debería devolver el `id`.

Por eso conviene separar modelos.

## 6. Modelos sugeridos para la clase

Archivo:

```text
app/schemas/item_schema.py
```

Código:

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str = Field(min_length=3, max_length=50)
    source: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=80)
    description: str | None = None
    category: str | None = Field(default=None, min_length=3, max_length=50)
    source: str | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None


class ExternalItemResponse(BaseModel):
    external_id: int
    name: str
    source: str
```

### Explicación de cada modelo

#### `ItemCreate`

Se usa cuando el cliente quiere crear un nuevo item.

```python
class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str = Field(min_length=3, max_length=50)
    source: str | None = None
```

Este modelo controla qué datos puede enviar el cliente en un `POST`.

No tiene `id`, porque el cliente no debe decidir el identificador.

#### `ItemUpdate`

Se usa cuando el cliente quiere actualizar un item existente.

```python
class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=80)
    description: str | None = None
    category: str | None = Field(default=None, min_length=3, max_length=50)
    source: str | None = None
```

Aquí todos los campos son opcionales porque el usuario puede querer actualizar
solo una parte del item.

Ejemplo de actualización válida:

```json
{
  "name": "Nuevo nombre"
}
```

No tiene sentido obligar al cliente a reenviar todos los campos si solo quiere
cambiar uno.

#### `ItemResponse`

Se usa para definir la respuesta de la API.

```python
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None
```

Este modelo sí incluye `id`, porque cuando la API responde, el cliente necesita
saber qué recurso fue creado o consultado.

#### `ExternalItemResponse`

Se usa para representar datos que vienen de una API externa.

```python
class ExternalItemResponse(BaseModel):
    external_id: int
    name: str
    source: str
```

Este modelo es útil para no devolver toda la respuesta cruda de la API externa.

Por ejemplo, si consumimos PokéAPI, la respuesta original tiene muchísimos
datos. Pero tal vez para esta clase solo necesitamos devolver:

```json
{
  "external_id": 25,
  "name": "pikachu",
  "source": "pokeapi"
}
```

## 7. Concepto 3: `response_model`

`response_model` sirve para decirle a FastAPI cuál será la forma de la
respuesta.

### Ejemplo

```python
@router.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    ...
```

Esto significa:

- El cliente envía datos con forma de `ItemCreate`.
- La API responde datos con forma de `ItemResponse`.
- Si todo sale bien, el código HTTP será `201 Created`.

FastAPI usa modelos de respuesta para validar, documentar, convertir y filtrar
los datos de salida. Esto es importante porque ayuda a evitar que la API
devuelva información innecesaria o sensible.

La documentación oficial también muestra que `status_code` puede declararse
directamente en operaciones como `@app.post()`, `@app.get()`, `@app.put()` y
`@app.delete()`.

## 8. Concepto 4: códigos de estado HTTP

Explicación sencilla para estudiantes:

> Un código de estado HTTP es la forma en que la API le dice al cliente qué pasó
> con la solicitud.

### Tabla básica para esta clase

| Código | Significado          | Cuándo usarlo                                    |
| -----: | -------------------- | ------------------------------------------------ |
|  `200` | OK                   | Cuando una consulta o actualización fue exitosa. |
|  `201` | Created              | Cuando se creó un recurso.                       |
|  `204` | No Content           | Cuando se eliminó algo y no se devuelve cuerpo.  |
|  `400` | Bad Request          | Cuando la solicitud tiene un problema lógico.    |
|  `404` | Not Found            | Cuando el recurso no existe.                     |
|  `422` | Unprocessable Entity | Cuando falla una validación de Pydantic.         |

### Ejemplo

```python
@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    ...
```

Aquí se usa `201` porque se está creando un recurso.

También se puede usar el módulo `status` para que el código sea más legible:

```python
from fastapi import status


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    ...
```

Esta forma es más clara porque evita números "mágicos".

## 9. Concepto 5: manejo de errores con `HTTPException`

Cuando algo sale mal, no deberíamos devolver errores improvisados.

### Incorrecto

```python
return {"error": "No encontrado"}
```

### Mejor

```python
from fastapi import HTTPException


if not item:
    raise HTTPException(
        status_code=404,
        detail="El recurso solicitado no existe"
    )
```

### Explicación

`HTTPException` interrumpe la ejecución de la función y devuelve una respuesta
HTTP con el código indicado.

En este caso:

- `status_code=404` indica que el recurso no existe.
- `detail` contiene el mensaje de error.

Ejemplo de respuesta:

```json
{
  "detail": "El recurso solicitado no existe"
}
```

Esto es más profesional porque el cliente puede interpretar correctamente el
error.

## 10. Concepto 6: separación de archivos

Cuando una API está en un solo archivo, puede funcionar para ejercicios
pequeños, pero se vuelve difícil de mantener.

### Ejemplo de mala organización

```text
main.py
```

Todo está allí:

- Rutas.
- Modelos.
- Consumo de API externa.
- Conexión a base de datos.
- Variables de configuración.
- Lógica de negocio.

### Problema

Cuando el proyecto crece, el archivo se vuelve largo, confuso y difícil de
explicar.

La solución es separar responsabilidades.

## 11. Estructura sugerida del proyecto

```text
app/
├── main.py
├── routers/
│   ├── items.py
│   └── external.py
├── schemas/
│   └── item_schema.py
├── services/
│   └── external_service.py
└── core/
    └── config.py
```

### Explicación de carpetas

| Carpeta o archivo | Responsabilidad                               |
| ----------------- | --------------------------------------------- |
| `main.py`         | Punto de entrada de la aplicación.            |
| `routers/`        | Define endpoints.                             |
| `schemas/`        | Define modelos Pydantic.                      |
| `services/`       | Contiene lógica de negocio o consumo externo. |
| `core/`           | Configuración general del proyecto.           |

FastAPI recomienda separar aplicaciones grandes en múltiples archivos y usar
`APIRouter` para organizar rutas de forma modular.

## 12. Proyecto guiado de la clase

### Nombre del mini proyecto

**API de Items Académicos**

La API permitirá:

- Crear items.
- Listar items.
- Consultar un item por ID.
- Actualizar un item.
- Eliminar un item.
- Consultar un item externo desde PokéAPI y adaptarlo a nuestro modelo.

Por ahora, para esta clase, los datos se guardarán en memoria usando una lista
de diccionarios.

Más adelante se conectará a Supabase.

## 13. Paso 1: crear estructura de carpetas

Desde la terminal:

```bash
mkdir clase_2_fastapi
cd clase_2_fastapi
mkdir app
mkdir app/routers
mkdir app/schemas
mkdir app/services
mkdir app/core
```

Crear archivos:

```bash
touch app/main.py
touch app/routers/items.py
touch app/routers/external.py
touch app/schemas/item_schema.py
touch app/services/external_service.py
touch app/core/config.py
```

En Windows PowerShell, si `touch` no funciona, pueden crear los archivos
manualmente o usar:

```powershell
New-Item app/main.py
New-Item app/routers/items.py
New-Item app/routers/external.py
New-Item app/schemas/item_schema.py
New-Item app/services/external_service.py
New-Item app/core/config.py
```

## 14. Paso 2: instalar dependencias

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno virtual.

En Windows:

```powershell
venv\Scripts\activate
```

En macOS o Linux:

```bash
source venv/bin/activate
```

Instalar FastAPI, Uvicorn y Requests:

```bash
pip install fastapi uvicorn requests
```

## 15. Paso 3: crear modelos Pydantic

Archivo:

```text
app/schemas/item_schema.py
```

Código:

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str = Field(min_length=3, max_length=50)
    source: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=80)
    description: str | None = None
    category: str | None = Field(default=None, min_length=3, max_length=50)
    source: str | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None


class ExternalItemResponse(BaseModel):
    external_id: int
    name: str
    source: str
```

### Explicación docente

Aquí no estamos creando tablas de base de datos. Estamos creando contratos de
datos.

Un contrato de datos responde preguntas como:

- ¿Qué campos puede enviar el cliente?
- ¿Qué campos son obligatorios?
- ¿Qué campos son opcionales?
- ¿Qué tipo debe tener cada campo?
- ¿Qué estructura tendrá la respuesta?

## 16. Paso 4: crear router de items

Archivo:

```text
app/routers/items.py
```

Código:

```python
from fastapi import APIRouter, HTTPException, status
from app.schemas.item_schema import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

items_db = []
current_id = 1


@router.get("/", response_model=list[ItemResponse])
def get_items():
    return items_db


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El item solicitado no existe"
    )


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    global current_id

    new_item = {
        "id": current_id,
        "name": item.name,
        "description": item.description,
        "category": item.category,
        "source": item.source
    }

    items_db.append(new_item)
    current_id += 1

    return new_item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate):
    for item in items_db:
        if item["id"] == item_id:
            update_data = item_data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                item[key] = value

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se puede actualizar porque el item no existe"
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se puede eliminar porque el item no existe"
    )
```

## 17. Explicación del router de items

### Importaciones

```python
from fastapi import APIRouter, HTTPException, status
```

Importamos:

- `APIRouter`: permite agrupar rutas.
- `HTTPException`: permite lanzar errores HTTP.
- `status`: permite usar constantes como `HTTP_404_NOT_FOUND`.

```python
from app.schemas.item_schema import ItemCreate, ItemUpdate, ItemResponse
```

Importamos los modelos Pydantic que creamos.

### Creación del router

```python
router = APIRouter(
    prefix="/items",
    tags=["Items"]
)
```

Esto significa que todas las rutas de este archivo comenzarán con `/items`.

Además, en la documentación `/docs`, aparecerán agrupadas bajo la etiqueta
`Items`.

Por ejemplo:

```python
@router.get("/")
```

Realmente será:

```http
GET /items/
```

### Base de datos temporal

```python
items_db = []
current_id = 1
```

Por ahora usamos una lista para simular una base de datos.

> Aclaración importante para los estudiantes: esta lista no es una base de datos
> real. Si detenemos el servidor, se pierde la información. Más adelante
> conectaremos Supabase/PostgreSQL.

### Endpoint `GET`: listar items

```python
@router.get("/", response_model=list[ItemResponse])
def get_items():
    return items_db
```

Este endpoint devuelve todos los items.

`response_model=list[ItemResponse]` indica que la respuesta será una lista de
objetos con forma de `ItemResponse`.

### Endpoint `GET` por ID

```python
@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
```

Aquí `item_id` es un parámetro de ruta.

Ejemplo:

```http
GET /items/1
```

FastAPI convierte automáticamente el valor de la URL a entero porque declaramos:

```python
item_id: int
```

Si el usuario envía:

```http
/items/hola
```

FastAPI devolverá un error de validación porque esperaba un número entero.

### Búsqueda del item

```python
for item in items_db:
    if item["id"] == item_id:
        return item
```

Se recorre la lista y se busca el item cuyo `id` coincida.

### Error `404`

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="El item solicitado no existe"
)
```

Si no se encuentra el item, se lanza un error `404`.

Esto es mejor que devolver `None`, porque el cliente entiende que el recurso no
fue encontrado.

### Endpoint `POST`

```python
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
```

Este endpoint recibe un `ItemCreate`.

Eso significa que el cuerpo de la petición debe cumplir las reglas del modelo.

Ejemplo válido:

```json
{
  "name": "Pikachu",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

Ejemplo inválido:

```json
{
  "name": "Pi",
  "category": "pokemon"
}
```

Este ejemplo es inválido porque `name` tiene menos de 3 caracteres.

FastAPI devolverá automáticamente un error `422`.

### Creación del nuevo item

```python
new_item = {
    "id": current_id,
    "name": item.name,
    "description": item.description,
    "category": item.category,
    "source": item.source
}
```

Construimos un diccionario usando los datos validados.

### Endpoint `PUT`

```python
@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate):
```

Este endpoint actualiza un item existente.

Usa `ItemUpdate`, no `ItemCreate`, porque en una actualización los campos pueden
ser opcionales.

### `model_dump(exclude_unset=True)`

```python
update_data = item_data.model_dump(exclude_unset=True)
```

Esta línea convierte el modelo Pydantic en diccionario.

`exclude_unset=True` significa:

> Solo incluye los campos que el usuario realmente envió.

Ejemplo:

Si el cliente envía:

```json
{
  "name": "Charmander"
}
```

Entonces `update_data` será:

```json
{
  "name": "Charmander"
}
```

No incluirá `description`, `category` ni `source`.

Esto evita sobrescribir campos con `None` sin querer.

### Endpoint `DELETE`

```python
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
```

Este endpoint elimina un item.

Usa código `204 No Content`, porque si la eliminación fue exitosa, no
necesitamos devolver cuerpo de respuesta.

## 18. Paso 5: crear servicio externo

Archivo:

```text
app/services/external_service.py
```

Código:

```python
import requests
from fastapi import HTTPException, status


def get_pokemon_from_api(pokemon_name: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    response = requests.get(url)

    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pokemon solicitado no existe en la API externa"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error al consultar la API externa"
        )

    data = response.json()

    return {
        "external_id": data["id"],
        "name": data["name"],
        "source": "pokeapi"
    }
```

## 19. Explicación del servicio externo

Este archivo no define rutas.

Su responsabilidad es consultar la API externa.

Esto es importante porque no queremos mezclar todo en el router.

- El router debe encargarse de recibir solicitudes HTTP.
- El servicio debe encargarse de la lógica.

```python
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
```

Construimos la URL con el nombre del pokemon.

```python
response = requests.get(url)
```

Consultamos la API externa.

```python
if response.status_code == 404:
```

Si la API externa responde `404`, nosotros también respondemos con un error
claro.

```python
if response.status_code != 200:
```

Si ocurre otro error, devolvemos `502 Bad Gateway`.

Este código significa que nuestra API intentó consultar otro servicio, pero ese
servicio respondió mal o no pudo procesar correctamente la solicitud.

```python
data = response.json()
```

Convertimos la respuesta JSON en un diccionario de Python.

```python
return {
    "external_id": data["id"],
    "name": data["name"],
    "source": "pokeapi"
}
```

No devolvemos toda la respuesta original. Solo devolvemos lo que necesitamos.

## 20. Paso 6: crear router externo

Archivo:

```text
app/routers/external.py
```

Código:

```python
from fastapi import APIRouter
from app.schemas.item_schema import ExternalItemResponse
from app.services.external_service import get_pokemon_from_api

router = APIRouter(
    prefix="/external",
    tags=["External API"]
)


@router.get("/pokemon/{pokemon_name}", response_model=ExternalItemResponse)
def get_external_pokemon(pokemon_name: str):
    return get_pokemon_from_api(pokemon_name)
```

## 21. Explicación del router externo

```python
router = APIRouter(
    prefix="/external",
    tags=["External API"]
)
```

Todas las rutas de este archivo empiezan con `/external`.

```python
@router.get("/pokemon/{pokemon_name}", response_model=ExternalItemResponse)
```

La ruta completa será:

```http
GET /external/pokemon/{pokemon_name}
```

Ejemplo:

```http
GET /external/pokemon/pikachu
```

La respuesta tendrá esta forma:

```json
{
  "external_id": 25,
  "name": "pikachu",
  "source": "pokeapi"
}
```

## 22. Paso 7: archivo de configuración

Archivo:

```text
app/core/config.py
```

Código:

```python
APP_NAME = "API de Items Académicos"
APP_VERSION = "1.0.0"
```

### Explicación

Por ahora este archivo es sencillo.

Más adelante puede usarse para cargar variables de entorno como:

- URL de Supabase.
- API key.
- Configuración de entorno.
- Nombre de la aplicación.

## 23. Paso 8: archivo principal `main.py`

Archivo:

```text
app/main.py
```

Código:

```python
from fastapi import FastAPI
from app.core.config import APP_NAME, APP_VERSION
from app.routers import items, external

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API académica para practicar modelos, validaciones, routers y estructura profesional con FastAPI."
)

app.include_router(items.router)
app.include_router(external.router)


@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API de Items Académicos",
        "docs": "/docs"
    }
```

## 24. Explicación de `main.py`

```python
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="..."
)
```

Creamos la aplicación principal de FastAPI.

Estos datos aparecen en la documentación automática.

```python
app.include_router(items.router)
app.include_router(external.router)
```

Aquí conectamos los routers con la aplicación principal.

Sin estas líneas, las rutas de `items.py` y `external.py` no funcionarían.

```python
@app.get("/")
def root():
```

Creamos una ruta inicial para comprobar que la API está funcionando.

## 25. Paso 9: ejecutar el proyecto

Desde la terminal, estando en la carpeta del proyecto:

```bash
uvicorn app.main:app --reload
```

### Explicación

```bash
uvicorn
```

Es el servidor que ejecuta nuestra aplicación.

```bash
app.main:app
```

Significa:

- Busca la carpeta `app`.
- Dentro busca el archivo `main.py`.
- Dentro busca la variable `app`.

```bash
--reload
```

Reinicia automáticamente el servidor cuando modificamos el código.

Abrir en el navegador:

```text
http://127.0.0.1:8000
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

## 26. Endpoints que deben aparecer en `/docs`

Al terminar, los estudiantes deberían ver:

```http
GET     /
GET     /items/
POST    /items/
GET     /items/{item_id}
PUT     /items/{item_id}
DELETE  /items/{item_id}
GET     /external/pokemon/{pokemon_name}
```

## 27. Pruebas sugeridas en clase

### Prueba 1: crear item válido

Endpoint:

```http
POST /items/
```

Body:

```json
{
  "name": "Pikachu",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

Respuesta esperada:

```json
{
  "id": 1,
  "name": "Pikachu",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

Código HTTP esperado:

```text
201 Created
```

### Prueba 2: crear item inválido

Endpoint:

```http
POST /items/
```

Body:

```json
{
  "name": "Pi",
  "description": "Nombre demasiado corto",
  "category": "pokemon"
}
```

Resultado esperado:

FastAPI debe devolver error de validación porque `name` tiene menos de 3
caracteres.

Código esperado:

```text
422 Unprocessable Entity
```

### Prueba 3: listar items

Endpoint:

```http
GET /items/
```

Respuesta esperada:

```json
[
  {
    "id": 1,
    "name": "Pikachu",
    "description": "Pokemon de tipo eléctrico",
    "category": "pokemon",
    "source": "manual"
  }
]
```

### Prueba 4: consultar item existente

Endpoint:

```http
GET /items/1
```

Respuesta esperada:

```json
{
  "id": 1,
  "name": "Pikachu",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

### Prueba 5: consultar item inexistente

Endpoint:

```http
GET /items/999
```

Respuesta esperada:

```json
{
  "detail": "El item solicitado no existe"
}
```

Código esperado:

```text
404 Not Found
```

### Prueba 6: actualizar item

Endpoint:

```http
PUT /items/1
```

Body:

```json
{
  "name": "Pikachu actualizado"
}
```

Respuesta esperada:

```json
{
  "id": 1,
  "name": "Pikachu actualizado",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

### Prueba 7: consultar API externa

Endpoint:

```http
GET /external/pokemon/pikachu
```

Respuesta esperada:

```json
{
  "external_id": 25,
  "name": "pikachu",
  "source": "pokeapi"
}
```

### Prueba 8: consultar dato inexistente en API externa

Endpoint:

```http
GET /external/pokemon/noexiste123
```

Respuesta esperada:

```json
{
  "detail": "El pokemon solicitado no existe en la API externa"
}
```

Código esperado:

```text
404 Not Found
```

## 28. Guion sugerido para explicar la diferencia entre archivos

Puedes explicarlo así:

- `main.py` es la puerta principal de la aplicación.
- `routers/items.py` contiene las rutas relacionadas con items.
- `routers/external.py` contiene las rutas relacionadas con APIs externas.
- `schemas/item_schema.py` contiene los modelos Pydantic.
- `services/external_service.py` contiene la lógica para consumir la API
  externa.
- `core/config.py` contiene configuración general del proyecto.

Luego puedes preguntar:

> ¿Dónde pondríamos la lógica para conectarnos a Supabase?

Respuesta esperada:

```text
En una carpeta como app/db/ o app/database/
```

> ¿Dónde pondríamos las variables de entorno?

Respuesta esperada:

```text
En un archivo .env, leído desde core/config.py
```

## 29. Actividad práctica en clase

### Actividad: reorganizar la API en carpetas

#### Instrucciones para estudiantes

A partir del proyecto trabajado en la clase anterior, deben reorganizar su API
usando la siguiente estructura:

```text
app/
├── main.py
├── routers/
│   ├── items.py
│   └── external.py
├── schemas/
│   └── item_schema.py
├── services/
│   └── external_service.py
└── core/
    └── config.py
```

Deben crear los siguientes modelos:

- `ItemCreate`
- `ItemUpdate`
- `ItemResponse`
- `ExternalItemResponse`

Deben implementar como mínimo estos endpoints:

```http
GET     /items/
POST    /items/
GET     /items/{item_id}
PUT     /items/{item_id}
DELETE  /items/{item_id}
GET     /external/pokemon/{pokemon_name}
```

Deben usar:

- `BaseModel`
- `Field`
- `response_model`
- `status_code`
- `HTTPException`
- `APIRouter`
- Separación por carpetas

## 30. Preguntas durante la actividad

Mientras trabajan, puedes hacer preguntas como:

- ¿Qué archivo se encarga de levantar la aplicación?
- ¿Qué archivo contiene las rutas de items?
- ¿Qué modelo se usa para crear un item?
- ¿Por qué `ItemCreate` no tiene `id`?
- ¿Por qué `ItemUpdate` tiene campos opcionales?
- ¿Qué hace `response_model`?
- ¿Qué pasa si envío un nombre con menos de 3 caracteres?
- ¿Qué error debe devolver la API si el item no existe?
- ¿Qué diferencia hay entre un error `404` y un error `422`?
- ¿Por qué no devolvemos toda la respuesta original de PokéAPI?

## 31. Mini explicación: validación automática

Puedes mostrar este ejemplo en `/docs`.

Body inválido:

```json
{
  "name": "ab",
  "category": "pokemon"
}
```

Luego explicar:

> Nosotros no escribimos un `if` manual para revisar la longitud del nombre.
> FastAPI y Pydantic lo hicieron automáticamente porque el modelo decía
> `min_length=3`.

Eso ayuda a que entiendan el valor de los modelos.

## 32. Mini explicación: documentación automática

Cuando entren a:

```text
http://127.0.0.1:8000/docs
```

Deben observar:

- Los endpoints agrupados por `tags`.
- Los modelos de entrada.
- Los modelos de respuesta.
- Los códigos de estado.
- Los parámetros de ruta.
- Los cuerpos JSON esperados.

Puedes decir:

> La documentación no la escribimos a mano. FastAPI la genera a partir del
> código. Por eso es importante escribir bien los modelos, los tipos y los
> decoradores.

## 33. Mini explicación: por qué `response_model` protege la salida

Puedes mostrar este ejemplo conceptual:

Supongamos que internamente tenemos este diccionario:

```python
user = {
    "id": 1,
    "name": "Laura",
    "email": "laura@email.com",
    "password": "123456"
}
```

Si devolvemos el diccionario completo, podríamos exponer datos sensibles.

Pero si usamos un modelo de respuesta:

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```

FastAPI puede filtrar la respuesta para que no salga el campo `password`.

### Explicación

El modelo de respuesta no solo documenta. También ayuda a controlar qué datos
salen de la API.

## 34. Errores comunes esperados

### Error 1: olvidan incluir el router

Código faltante:

```python
app.include_router(items.router)
```

Síntoma:

```text
La ruta no aparece en /docs.
```

Solución:

```text
Verificar que el router esté importado e incluido en main.py.
```

### Error 2: problema de importaciones

Ejemplo de error:

```text
ModuleNotFoundError: No module named 'app'
```

Causas comunes:

- Ejecutaron `uvicorn` desde una carpeta incorrecta.
- No están ubicados en la raíz del proyecto.
- Escribieron mal la ruta del import.

Solución:

Ejecutar desde la carpeta donde está `app/`:

```bash
uvicorn app.main:app --reload
```

### Error 3: modelo mal usado

Ejemplo:

```python
@router.post("/", response_model=ItemCreate)
```

Problema:

La respuesta no debería usar `ItemCreate`, porque al crear un item esperamos
devolver también el `id`.

Solución:

```python
@router.post("/", response_model=ItemResponse)
```

### Error 4: actualizaciones que borran datos

Código problemático:

```python
update_data = item_data.model_dump()
```

Esto puede incluir campos con `None` y sobrescribir datos existentes.

Mejor:

```python
update_data = item_data.model_dump(exclude_unset=True)
```

### Error 5: devolver error como texto

Incorrecto:

```python
return "No encontrado"
```

Mejor:

```python
raise HTTPException(
    status_code=404,
    detail="El recurso solicitado no existe"
)
```

## 35. Cierre conceptual de la clase

Puedes cerrar con esta idea:

> Hoy la API dejó de ser un archivo suelto y empezó a parecerse a un backend
> real. Ya tenemos modelos, validaciones, códigos de estado, manejo de errores,
> documentación automática y separación por carpetas. Todavía no tenemos base de
> datos real, pero ya estamos preparando el proyecto para conectarlo después a
> Supabase.

## Referencias oficiales

- [FastAPI: Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI: Body - Fields](https://fastapi.tiangolo.com/tutorial/body-fields/)
- [FastAPI: Response Model](https://fastapi.tiangolo.com/es/tutorial/response-model/)
- [FastAPI: Response Status Code](https://fastapi.tiangolo.com/es/tutorial/response-status-code/)
- [FastAPI: Handling Errors](https://fastapi.tiangolo.com/es/tutorial/handling-errors/)
- [FastAPI: Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/es/tutorial/bigger-applications/)
- [Pydantic: Models](https://docs.pydantic.dev/latest/concepts/models/)
