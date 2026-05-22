# Tarea: API de Items Académicos con FastAPI

## 1. Objetivo

Construir una API con FastAPI aplicando los conceptos trabajados en clase:

- Modelos Pydantic.
- Validaciones con `Field`.
- Separación de modelos de creación, actualización y respuesta.
- Uso de `response_model`.
- Códigos de estado HTTP.
- Manejo de errores con `HTTPException`.
- Organización del proyecto por carpetas.
- Uso de `APIRouter`.
- Consumo de una API externa usando `requests`.

La idea es que la API deje de estar en un solo archivo y empiece a tener una
estructura más parecida a un backend real.

## 2. Descripción general

Debes crear una API llamada **API de Items Académicos**.

La API debe permitir:

- Crear items.
- Listar items.
- Consultar un item por ID.
- Actualizar un item.
- Eliminar un item.
- Consultar un Pokémon desde PokéAPI.
- Adaptar la respuesta externa a un modelo propio.

Por ahora, los datos deben guardarse en memoria usando una lista de
diccionarios.

> Importante: no debes usar base de datos todavía.

## 3. Estructura obligatoria del proyecto

El proyecto debe tener esta estructura:

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

## 4. Dependencias

Debes instalar las siguientes dependencias:

```bash
pip install fastapi uvicorn requests
```

Para ejecutar el proyecto:

```bash
uvicorn app.main:app --reload
```

La API debe estar disponible en:

```text
http://127.0.0.1:8000
```

La documentación automática debe estar disponible en:

```text
http://127.0.0.1:8000/docs
```

## 5. Modelos obligatorios

En el archivo:

```text
app/schemas/item_schema.py
```

Debes crear los siguientes modelos:

- `ItemCreate`
- `ItemUpdate`
- `ItemResponse`
- `ExternalItemResponse`

### `ItemCreate`

Debe usarse para crear un item.

Debe tener:

| Campo         | Tipo  | Reglas                                                 |
| ------------- | ----- | ------------------------------------------------------ |
| `name`        | `str` | Obligatorio, mínimo 3 caracteres, máximo 80 caracteres |
| `description` | `str  | None`                                                  |
| `category`    | `str` | Obligatorio, mínimo 3 caracteres, máximo 50 caracteres |
| `source`      | `str  | None`                                                  |

### `ItemUpdate`

Debe usarse para actualizar un item.

Todos sus campos deben ser opcionales.

Debe permitir actualizar solo una parte del item, por ejemplo:

```json
{
  "name": "Nuevo nombre"
}
```

### `ItemResponse`

Debe usarse como modelo de respuesta para los items internos.

Debe incluir:

| Campo         | Tipo  |
| ------------- | ----- |
| `id`          | `int` |
| `name`        | `str` |
| `description` | `str  |
| `category`    | `str` |
| `source`      | `str  |

### `ExternalItemResponse`

Debe usarse para responder datos adaptados desde PokéAPI.

Debe incluir:

| Campo         | Tipo  |
| ------------- | ----- |
| `external_id` | `int` |
| `name`        | `str` |
| `source`      | `str` |

## 6. Endpoints obligatorios

La API debe implementar estos endpoints:

```http
GET     /
GET     /items/
POST    /items/
GET     /items/{item_id}
PUT     /items/{item_id}
DELETE  /items/{item_id}
GET     /external/pokemon/{pokemon_name}
```

## 7. Requisitos por endpoint

### `GET /`

Debe devolver un mensaje inicial.

Respuesta esperada:

```json
{
  "message": "Bienvenido a la API de Items Académicos",
  "docs": "/docs"
}
```

### `GET /items/`

Debe listar todos los items guardados en memoria.

Debe usar:

```python
response_model=list[ItemResponse]
```

### `POST /items/`

Debe crear un nuevo item.

Debe recibir:

```python
ItemCreate
```

Debe responder:

```python
ItemResponse
```

Debe usar el código HTTP:

```text
201 Created
```

Ejemplo de body válido:

```json
{
  "name": "Pikachu",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

### `GET /items/{item_id}`

Debe consultar un item por ID.

Si el item existe, debe devolverlo.

Si el item no existe, debe responder con:

```text
404 Not Found
```

Respuesta esperada cuando no existe:

```json
{
  "detail": "El item solicitado no existe"
}
```

### `PUT /items/{item_id}`

Debe actualizar un item existente.

Debe recibir:

```python
ItemUpdate
```

Debe usar:

```python
model_dump(exclude_unset=True)
```

Esto evita borrar campos que el usuario no envió.

Si el item no existe, debe responder con:

```text
404 Not Found
```

### `DELETE /items/{item_id}`

Debe eliminar un item existente.

Si el item se elimina correctamente, debe responder con:

```text
204 No Content
```

Si el item no existe, debe responder con:

```text
404 Not Found
```

### `GET /external/pokemon/{pokemon_name}`

Debe consultar PokéAPI usando `requests`.

Ejemplo:

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

Si el Pokémon no existe, debe responder con:

```text
404 Not Found
```

Respuesta esperada:

```json
{
  "detail": "El pokemon solicitado no existe en la API externa"
}
```

## 8. Requisitos técnicos

El proyecto debe usar obligatoriamente:

- `BaseModel`
- `Field`
- `response_model`
- `status_code`
- `HTTPException`
- `APIRouter`
- `requests`
- Separación por carpetas

No se permite:

- Poner toda la API en un solo archivo.
- Crear un único modelo para todo.
- Devolver errores como strings simples.
- Devolver toda la respuesta cruda de PokéAPI.
- Usar base de datos en esta tarea.

## 9. Pruebas mínimas

Debes probar tu API desde `/docs`.

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

Resultado esperado:

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

```text
422 Unprocessable Entity
```

### Prueba 3: listar items

Endpoint:

```http
GET /items/
```

Resultado esperado:

Debe aparecer la lista de items creados.

### Prueba 4: consultar item existente

Endpoint:

```http
GET /items/1
```

Resultado esperado:

Debe devolver el item con `id` igual a `1`.

### Prueba 5: consultar item inexistente

Endpoint:

```http
GET /items/999
```

Resultado esperado:

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

Resultado esperado:

Debe actualizar únicamente el campo `name`.

### Prueba 7: consultar PokéAPI

Endpoint:

```http
GET /external/pokemon/pikachu
```

Resultado esperado:

```json
{
  "external_id": 25,
  "name": "pikachu",
  "source": "pokeapi"
}
```

### Prueba 8: consultar Pokémon inexistente

Endpoint:

```http
GET /external/pokemon/noexiste123
```

Resultado esperado:

```text
404 Not Found
```

## 10. Entrega

Debes entregar:

- Carpeta del proyecto con la estructura solicitada.
- Código funcionando.
- Captura o evidencia de `/docs`.
- Captura o evidencia de al menos 4 pruebas realizadas.

## 11. Criterios de evaluación

| Criterio                                         |  Puntos |
| ------------------------------------------------ | ------: |
| Estructura correcta de carpetas                  |      20 |
| Modelos Pydantic bien definidos                  |      20 |
| Endpoints internos funcionando                   |      20 |
| Manejo correcto de errores                       |      15 |
| Uso correcto de `response_model` y `status_code` |      10 |
| Consumo y adaptación de PokéAPI                  |      10 |
| Orden, claridad y legibilidad del código         |       5 |
| **Total**                                        | **100** |

## 12. Preguntas de reflexión

Responde brevemente:

1. ¿Por qué `ItemCreate` no debe tener `id`?
2. ¿Por qué `ItemUpdate` tiene campos opcionales?
3. ¿Qué problema evita `response_model`?
4. ¿Cuál es la diferencia entre un error `404` y un error `422`?
5. ¿Por qué no conviene devolver toda la respuesta original de PokéAPI?
6. ¿Por qué es mejor separar rutas, modelos y servicios en archivos distintos?

## 13. Reto opcional

Si terminas antes, agrega una validación adicional:

- El campo `source` solo puede aceptar valores como `"manual"` o `"pokeapi"`.

También puedes agregar un endpoint extra:

```http
GET /items/category/{category_name}
```

Este endpoint debe listar únicamente los items que pertenezcan a una categoría
específica.
