# Duda: ¿Qué significa `Item` y por qué usamos varios modelos?

## 1. Pregunta principal

En la clase estamos usando nombres como:

- `ItemCreate`
- `ItemUpdate`
- `ItemResponse`
- `ExternalItemResponse`

La duda principal es:

> ¿Qué significa `Item` y por qué no usamos un solo modelo para todo?

## 2. ¿Qué significa `Item`?

`Item` significa **elemento**.

En una API se usa muchas veces como un nombre genérico para representar:

- Un recurso.
- Un registro.
- Una entidad.
- Un dato principal que la API administra.

En nuestra clase, `Item` es simplemente un ejemplo. No es algo especial de
FastAPI.

## 3. Ejemplos según el tipo de proyecto

El nombre `Item` podría representar cosas distintas dependiendo del proyecto:

| Si el proyecto es de... | El item podría ser... |
| ----------------------- | --------------------- |
| Pokemones               | Un Pokémon            |
| Libros                  | Un libro              |
| Productos               | Un producto           |
| Tareas                  | Una tarea             |
| Noticias                | Una noticia guardada  |
| Clima                   | Una ciudad consultada |
| Recetas                 | Una receta            |
| Películas               | Una película          |

Entonces, cuando escribimos:

```python
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    category: str
```

Estamos diciendo:

> Para crear un elemento en mi sistema, necesito como mínimo un nombre y una
> categoría.

## 4. Ejemplos de `Item`

### Si el item fuera un Pokémon

```json
{
  "name": "Pikachu",
  "description": "Pokémon de tipo eléctrico",
  "category": "pokemon"
}
```

### Si el item fuera un libro

```json
{
  "name": "Cien años de soledad",
  "description": "Novela de Gabriel García Márquez",
  "category": "literatura"
}
```

### Si el item fuera una tarea

```json
{
  "name": "Estudiar FastAPI",
  "description": "Repasar modelos Pydantic",
  "category": "academico"
}
```

## 5. Idea importante

`Item` no es una palabra especial de FastAPI.

Es solo un nombre que usamos para representar un recurso de ejemplo.

En una API real, normalmente usaríamos nombres más claros según el proyecto.

Por ejemplo:

```python
class ProductCreate(BaseModel):
    name: str
    price: float
```

O:

```python
class TaskCreate(BaseModel):
    title: str
    completed: bool = False
```

O:

```python
class PokemonCreate(BaseModel):
    name: str
    type: str
```

En la clase usamos `Item` porque sirve como ejemplo general.

Puedes explicarlo así:

> Piensen en `Item` como "el registro principal que mi API administra". En un
> proyecto real, le ponemos un nombre más específico según el dominio:
> `Product`, `Task`, `Book`, `Movie`, `Pokemon`, etc.

## 6. ¿Por qué no usamos un solo modelo llamado `Item`?

Porque una API no recibe y responde exactamente la misma información en todos
los casos.

Cada operación tiene una necesidad distinta:

| Operación                | Modelo recomendado     | Motivo                                                        |
| ------------------------ | ---------------------- | ------------------------------------------------------------- |
| Crear un item            | `ItemCreate`           | El cliente envía datos nuevos, pero no debe enviar el `id`.   |
| Actualizar un item       | `ItemUpdate`           | El cliente puede enviar solo los campos que quiere cambiar.   |
| Responder un item        | `ItemResponse`         | La API sí debe devolver el `id` generado.                     |
| Responder datos externos | `ExternalItemResponse` | La API adapta datos de otra API y devuelve solo lo necesario. |

## 7. ¿Por qué `ItemCreate` no tiene `id`?

Cuando el cliente crea un item, no debería decidir el `id`.

Ejemplo de body correcto para crear:

```json
{
  "name": "Pikachu",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

Observa que no se envía `id`.

Eso pasa porque el `id` normalmente lo genera:

- La base de datos.
- El backend.
- La lógica interna de la aplicación.

Por eso usamos este modelo:

```python
class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str = Field(min_length=3, max_length=50)
    source: str | None = None
```

## 8. ¿Por qué `ItemResponse` sí tiene `id`?

Cuando la API responde, el cliente necesita saber cuál fue el recurso creado o
consultado.

Ejemplo de respuesta después de crear:

```json
{
  "id": 1,
  "name": "Pikachu",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

Aquí sí aparece `id`.

Por eso usamos este modelo:

```python
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None
```

## 9. ¿Por qué `ItemUpdate` tiene campos opcionales?

Cuando el cliente actualiza un item, puede querer cambiar solo una parte.

Ejemplo:

```json
{
  "name": "Pikachu actualizado"
}
```

No tiene sentido obligar al cliente a enviar otra vez:

- `description`
- `category`
- `source`

Por eso todos los campos de `ItemUpdate` son opcionales:

```python
class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=80)
    description: str | None = None
    category: str | None = Field(default=None, min_length=3, max_length=50)
    source: str | None = None
```

## 10. ¿Qué problema evita `exclude_unset=True`?

En una actualización parcial usamos:

```python
update_data = item_data.model_dump(exclude_unset=True)
```

Esto significa:

> Convierte el modelo en diccionario, pero solo con los campos que el cliente
> envió.

Si el cliente envía:

```json
{
  "name": "Charmander"
}
```

Entonces `update_data` queda así:

```json
{
  "name": "Charmander"
}
```

No incluye los campos que no fueron enviados.

Esto evita borrar datos accidentalmente.

## 11. ¿Qué pasaría si usáramos un solo modelo?

Supongamos este modelo:

```python
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None
```

Problemas:

- Para crear un item, el cliente tendría que enviar `id`.
- Para actualizar, el cliente tendría que enviar todos los campos.
- Para responder, no podríamos controlar bien qué datos salen.
- El contrato de entrada y salida quedaría mezclado.

Por eso separamos los modelos.

## 12. Diferencia entre modelo de entrada y modelo de salida

| Tipo de modelo | Se usa para                      | Ejemplo                                |
| -------------- | -------------------------------- | -------------------------------------- |
| Entrada        | Validar lo que el cliente envía  | `ItemCreate`, `ItemUpdate`             |
| Salida         | Controlar lo que la API responde | `ItemResponse`, `ExternalItemResponse` |

## 13. Resumen mental

Puedes recordarlo así:

- `Item`: nombre genérico del recurso de ejemplo.
- `ItemCreate`: lo que necesito para crear.
- `ItemUpdate`: lo que puedo cambiar.
- `ItemResponse`: lo que quiero responder.
- `ExternalItemResponse`: lo que adapto desde una API externa.

## 14. Frase clave

> No todos los modelos representan tablas. En FastAPI, muchas veces los modelos
> representan contratos de datos.

Un contrato de datos responde:

- ¿Qué campos se aceptan?
- ¿Qué campos son obligatorios?
- ¿Qué campos son opcionales?
- ¿Qué tipo debe tener cada campo?
- ¿Qué estructura tendrá la respuesta?

## 15. Ejemplo completo

### Crear item

Request:

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

Modelo usado para entrada:

```python
ItemCreate
```

Respuesta:

```json
{
  "id": 1,
  "name": "Pikachu",
  "description": "Pokemon de tipo eléctrico",
  "category": "pokemon",
  "source": "manual"
}
```

Modelo usado para salida:

```python
ItemResponse
```

## 16. Conclusión

Separar modelos hace que la API sea más clara, más segura y más fácil de
mantener.

No usamos varios modelos por capricho. Los usamos porque cada operación tiene
una responsabilidad distinta.
