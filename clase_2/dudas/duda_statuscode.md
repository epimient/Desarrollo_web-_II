# Duda: ¿Qué va en el decorador y qué va dentro de la función?

## 1. Pregunta principal

La duda está en diferenciar qué cosas se escriben en el decorador del endpoint y
qué cosas se escriben dentro de la función.

En FastAPI, un endpoint normalmente tiene dos partes:

- El **decorador**, donde declaramos información HTTP del endpoint.
- La **función**, donde recibimos datos y escribimos la lógica.

## 2. Ejemplo inicial

```python
from fastapi import APIRouter, status
from app.schemas.item_schema import ItemCreate, ItemResponse

router = APIRouter()


@router.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_item(item: ItemCreate):
    new_item = {
        "id": 1,
        "name": item.name,
        "description": item.description,
        "category": item.category,
        "source": item.source
    }

    return new_item
```

Aquí hay tres partes importantes:

- `item: ItemCreate`
- `response_model=ItemResponse`
- `status_code=status.HTTP_201_CREATED`

## 3. `item: ItemCreate`

Esto va en la función:

```python
def create_item(item: ItemCreate):
```

Significa:

> Lo que el cliente envía en el body debe cumplir el modelo `ItemCreate`.

Es decir, esto valida la **entrada**.

Por ejemplo, el cliente envía:

```json
{
  "name": "Pikachu",
  "description": "Pokémon eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

FastAPI revisa si ese JSON cumple con `ItemCreate`.

Si no cumple, FastAPI responde automáticamente con un error de validación.

## 4. `response_model=ItemResponse`

Esto va en el decorador:

```python
response_model=ItemResponse
```

Significa:

> Lo que mi endpoint devuelve debe tener la forma de `ItemResponse`.

Es decir, esto valida, documenta y organiza la **salida**.

Por ejemplo, la respuesta debería salir así:

```json
{
  "id": 1,
  "name": "Pikachu",
  "description": "Pokémon eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

## 5. `status_code=status.HTTP_201_CREATED`

Esto también va en el decorador:

```python
status_code=status.HTTP_201_CREATED
```

Significa:

> Si todo sale bien, el endpoint responde con código HTTP `201 Created`.

El `status_code` no es una validación de datos.

Es la forma en que declaramos el código HTTP exitoso que debería devolver el
endpoint.

## 6. ¿Por qué usar `status.HTTP_201_CREATED` en vez de `201`?

Estas dos líneas hacen lo mismo:

```python
status_code=201
```

Y:

```python
status_code=status.HTTP_201_CREATED
```

Pero esta versión es más clara:

```python
status_code=status.HTTP_201_CREATED
```

Porque cuando alguien lee el código entiende:

> Este endpoint responde `201 Created` porque está creando algo.

Usar `status.HTTP_201_CREATED` evita números "mágicos" y mejora la legibilidad.

## 7. ¿Dónde va cada cosa?

| Parte           | Dónde va                             | Para qué sirve                        |
| --------------- | ------------------------------------ | ------------------------------------- |
| `ItemCreate`    | En la función                        | Valida lo que entra                   |
| `ItemResponse`  | En el decorador con `response_model` | Controla lo que sale                  |
| `status_code`   | En el decorador                      | Define el código HTTP exitoso         |
| `HTTPException` | Dentro de la función                 | Devuelve errores cuando algo sale mal |

## 8. Ejemplo completo de creación

```python
from fastapi import APIRouter, HTTPException, status
from app.schemas.item_schema import ItemCreate, ItemResponse

router = APIRouter()

items_db = []


@router.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_item(item: ItemCreate):
    new_item = {
        "id": 1,
        "name": item.name,
        "description": item.description,
        "category": item.category,
        "source": item.source
    }

    items_db.append(new_item)

    return new_item
```

En este ejemplo:

- `@router.post("/items")` define la ruta.
- `response_model=ItemResponse` define cómo debe salir la respuesta.
- `status_code=status.HTTP_201_CREATED` define el código exitoso.
- `item: ItemCreate` define lo que debe llegar en el body.
- `return new_item` devuelve la respuesta.

## 9. Ejemplo completo con error

```python
@router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK
)
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El item no existe"
    )
```

Aquí pasa esto:

```python
item_id: int
```

Valida que el parámetro de la URL sea un número.

```python
response_model=ItemResponse
```

Dice cómo debe salir la respuesta.

```python
status_code=status.HTTP_200_OK
```

Dice que si todo sale bien responde `200 OK`.

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="El item no existe"
)
```

Dice qué pasa si el item no existe.

## 10. Decorador vs función

Piensa en esta separación:

### En el decorador

Declaramos la "promesa" HTTP del endpoint:

- Qué método usa: `GET`, `POST`, `PUT`, `DELETE`.
- Qué ruta tiene: `"/items"`, `"/items/{item_id}"`.
- Qué modelo usa para la respuesta: `response_model`.
- Qué código devuelve si todo sale bien: `status_code`.
- En qué grupo aparece en `/docs`: `tags`.

### En la función

Escribimos la entrada y la lógica:

- Qué datos recibe.
- Qué parámetros llegan por la URL.
- Qué body llega desde el cliente.
- Qué validaciones de negocio se hacen.
- Qué se guarda.
- Qué se retorna.
- Qué errores se lanzan con `HTTPException`.

## 11. Regla mental

Puedes recordarlo así:

> En el decorador pongo la promesa del endpoint: qué ruta es, qué devuelve y con
> qué código responde si todo sale bien.

> En la función pongo lo que recibe el endpoint y la lógica para procesarlo.

## 12. Resumen final

| Elemento                              | Pregunta que responde                   |
| ------------------------------------- | --------------------------------------- |
| `@router.post("/items")`              | ¿Cuál es la ruta y el método HTTP?      |
| `item: ItemCreate`                    | ¿Qué datos entran?                      |
| `response_model=ItemResponse`         | ¿Qué forma tiene la respuesta?          |
| `status_code=status.HTTP_201_CREATED` | ¿Qué código devuelve si todo sale bien? |
| `raise HTTPException(...)`            | ¿Qué pasa si algo sale mal?             |
