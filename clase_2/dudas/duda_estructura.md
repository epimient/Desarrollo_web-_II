# Duda: ¿Cómo se separan las rutas con `APIRouter`?

## 1. Idea principal

La recomendación significa:

> No meter todas las rutas de toda la API en un solo archivo gigante.

Lo ideal es dividirlas por tema o responsabilidad usando varios archivos dentro
de la carpeta `routers/`.

## 2. Proyecto pequeño

En un proyecto pequeño podrías tener algo así:

```text
app/
├── main.py
└── routers/
    └── items.py
```

Eso está bien si solo tienes rutas de items.

## 3. Problema: un solo archivo para todas las rutas

Si el proyecto empieza a tener más cosas, no conviene hacer esto:

```text
app/
├── main.py
└── routers/
    └── routes.py
```

Y dentro de `routes.py` meter todo:

```python
# routes.py

@app.get("/items")
def get_items():
    ...


@app.post("/items")
def create_item():
    ...


@app.get("/external/pokemon/{name}")
def get_pokemon():
    ...


@app.get("/users")
def get_users():
    ...


@app.post("/tasks")
def create_task():
    ...
```

Eso funciona, pero con el tiempo se vuelve desordenado.

## 4. Estructura recomendada para rutas

Lo recomendado es separar así:

```text
app/
├── main.py
└── routers/
    ├── items.py
    ├── external.py
    ├── users.py
    └── tasks.py
```

Cada archivo maneja un grupo de rutas.

## 5. Ejemplo: `items.py`

El archivo `items.py` tendría solo rutas de items:

```python
@router.get("/items")
def get_items():
    ...


@router.post("/items")
def create_item():
    ...
```

## 6. Ejemplo: `external.py`

El archivo `external.py` tendría solo rutas relacionadas con APIs externas:

```python
@router.get("/external/pokemon/{name}")
def get_pokemon():
    ...
```

## 7. Ejemplo: `users.py`

El archivo `users.py` tendría solo rutas de usuarios:

```python
@router.get("/users")
def get_users():
    ...
```

## 8. ¿Qué permite `APIRouter`?

`APIRouter` permite crear mini grupos de rutas separados y luego conectarlos a
la aplicación principal.

En `items.py` podrías hacer esto:

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.get("/")
def get_items():
    return {"message": "Lista de items"}


@router.post("/")
def create_item():
    return {"message": "Item creado"}
```

Y en `main.py` lo conectas:

```python
from fastapi import FastAPI
from app.routers import items

app = FastAPI()

app.include_router(items.router)
```

Entonces la ruta final queda así:

```http
GET /items/
POST /items/
```

## 9. ¿Por qué queda `/items/`?

Porque el archivo `items.py` tiene:

```python
prefix="/items"
```

Y cada endpoint tiene:

```python
@router.get("/")
```

Entonces:

```text
prefix="/items" + @router.get("/") = GET /items/
```

## 10. Más ejemplos de combinación

### Ejemplo 1

```python
router = APIRouter(prefix="/items")


@router.get("/")
def get_items():
    ...
```

Resultado:

```http
GET /items/
```

### Ejemplo 2

```python
router = APIRouter(prefix="/items")


@router.get("/{item_id}")
def get_item(item_id: int):
    ...
```

Resultado:

```http
GET /items/{item_id}
```

### Ejemplo 3

```python
router = APIRouter(prefix="/external")


@router.get("/pokemon/{pokemon_name}")
def get_pokemon(pokemon_name: str):
    ...
```

Resultado:

```http
GET /external/pokemon/{pokemon_name}
```

## 11. Entonces, ¿cuál es la idea?

No se trata de tener una sola carpeta con un solo archivo para todo.

Se trata de organizar varios archivos dentro de esa carpeta según la
responsabilidad.

Una forma sencilla de explicárselo a los estudiantes sería:

- `main.py` prende la aplicación.
- Cada archivo dentro de `routers/` maneja una familia de endpoints.
- `APIRouter` permite separar esas familias y luego unirlas en `main.py`.

## 12. Estructura de la clase

Para el proyecto de clase, esta estructura está perfecta:

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

## 13. Si el proyecto creciera

Si el proyecto creciera, también podrías tener:

```text
app/
├── main.py
├── routers/
│   ├── items.py
│   ├── external.py
│   ├── favorites.py
│   └── reports.py
├── schemas/
│   ├── item_schema.py
│   ├── external_schema.py
│   ├── favorite_schema.py
│   └── report_schema.py
├── services/
│   ├── item_service.py
│   ├── external_service.py
│   ├── favorite_service.py
│   └── report_service.py
└── core/
    └── config.py
```

## 14. Regla práctica

Puedes recordarlo así:

> Si un archivo empieza a tener demasiadas rutas de temas diferentes, sepáralo.

> Si todas las rutas son del mismo tema, pueden quedarse juntas.

## 15. Resumen rápido

| Archivo o carpeta     | Responsabilidad                                 |
| --------------------- | ----------------------------------------------- |
| `main.py`             | Crea la app y conecta routers.                  |
| `routers/items.py`    | Rutas relacionadas con items.                   |
| `routers/external.py` | Rutas relacionadas con APIs externas.           |
| `schemas/`            | Modelos Pydantic.                               |
| `services/`           | Lógica interna o consumo de servicios externos. |
| `core/`               | Configuración general.                          |

## 16. Frase clave

> `APIRouter` nos permite dividir la API en grupos de rutas pequeños, claros y
> fáciles de mantener.
