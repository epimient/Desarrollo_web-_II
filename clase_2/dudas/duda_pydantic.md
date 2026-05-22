# Duda: ¿Pydantic evita escribir muchos `if`?

## 1. Respuesta corta

Sí, la idea va bien.

Pydantic sirve para **validar** y **definir la forma de los datos**, evitando
que tengamos que escribir muchos `if` manuales para revisar cosas básicas.

Por ejemplo, Pydantic ayuda a validar:

- Tipos de datos.
- Campos obligatorios.
- Campos opcionales.
- Longitudes mínimas y máximas.
- Reglas básicas de entrada.
- Estructura del JSON que llega a la API.

## 2. Ejemplo sin Pydantic

Sin Pydantic, podríamos terminar escribiendo muchas validaciones manuales dentro
del endpoint.

Ejemplo:

```python
if len(name) < 3:
    return {"error": "El nombre debe tener mínimo 3 caracteres"}

if len(name) > 80:
    return {"error": "El nombre no puede superar 80 caracteres"}

if not isinstance(name, str):
    return {"error": "El nombre debe ser texto"}
```

Este código funciona, pero tiene varios problemas:

- Hace que el endpoint crezca demasiado.
- Mezcla validación con lógica de negocio.
- Es fácil olvidar una validación.
- Las respuestas pueden quedar inconsistentes.
- La documentación automática no sabe claramente qué reglas tiene el dato.

## 3. Ejemplo con Pydantic

Con Pydantic, declaramos la forma esperada de los datos en un modelo.

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    category: str
```

Con este modelo, estamos diciendo:

- `name` debe ser texto.
- `name` debe tener mínimo 3 caracteres.
- `name` debe tener máximo 80 caracteres.
- `category` debe ser texto.
- `category` es obligatorio.

## 4. Ejemplo de JSON válido

Si enviamos este body:

```json
{
  "name": "Pikachu",
  "category": "pokemon"
}
```

FastAPI lo acepta porque cumple las reglas del modelo.

## 5. Ejemplo de JSON inválido

Si enviamos este body:

```json
{
  "name": "Pi",
  "category": "pokemon"
}
```

FastAPI responde automáticamente con un error de validación porque `"Pi"` tiene
menos de 3 caracteres.

En este caso, no tuvimos que escribir manualmente:

```python
if len(name) < 3:
    ...
```

Pydantic y FastAPI hicieron esa validación por nosotros.

## 6. Idea principal

En vez de llenar el endpoint de `if` para validar tipos, campos obligatorios y
longitudes, usamos modelos Pydantic.

Ejemplo:

```python
class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str = Field(min_length=3, max_length=50)
```

Este modelo funciona como un contrato de datos.

El contrato responde:

- ¿Qué campos puede enviar el cliente?
- ¿Qué campos son obligatorios?
- ¿Qué campos son opcionales?
- ¿Qué tipo debe tener cada campo?
- ¿Qué reglas básicas debe cumplir cada campo?

## 7. Pero cuidado: Pydantic no reemplaza todos los `if`

Pydantic es excelente para validar la **estructura de los datos**, pero no
reemplaza toda la lógica del backend.

Pydantic sirve muy bien para validar cosas como:

```python
name: str
age: int
price: float
email: EmailStr
name: str = Field(min_length=3)
```

Pero todavía necesitamos `if` para reglas de negocio.

## 8. ¿Qué son reglas de negocio?

Las reglas de negocio son condiciones que dependen de lo que está pasando en la
aplicación.

Por ejemplo:

- Verificar si un item existe.
- Verificar si hay stock disponible.
- Verificar si un usuario tiene permisos.
- Verificar si un recurso ya fue creado.
- Verificar si una API externa respondió correctamente.

## 9. Ejemplo de `if` que sí necesitamos

Si buscamos un item y no existe, necesitamos responder con `404`.

```python
if not item:
    raise HTTPException(
        status_code=404,
        detail="Item no encontrado"
    )
```

Pydantic no puede saber si un item existe en nuestra lista, base de datos o
sistema.

Eso es lógica de negocio.

## 10. Otro ejemplo de regla de negocio

Supongamos que tenemos productos con stock.

```python
if item["stock"] == 0:
    raise HTTPException(
        status_code=400,
        detail="No hay stock disponible"
    )
```

Pydantic puede validar que `stock` sea un número, pero la decisión de no vender
si el stock es `0` es una regla del negocio.

## 11. Comparación rápida

| Caso                                  | ¿Lo valida Pydantic? | ¿Necesita `if`? |
| ------------------------------------- | -------------------- | --------------- |
| `name` debe ser texto                 | Sí                   | No              |
| `name` debe tener mínimo 3 caracteres | Sí                   | No              |
| `category` es obligatoria             | Sí                   | No              |
| `item_id` debe ser entero             | Sí                   | No              |
| El item existe en la base de datos    | No                   | Sí              |
| El stock es suficiente                | No                   | Sí              |
| El usuario tiene permisos             | No                   | Sí              |
| La API externa respondió con error    | No                   | Sí              |

## 12. Frase correcta para recordar

> Pydantic valida automáticamente la forma y las reglas básicas de los datos.
> Así evitamos muchos `if`, pero seguimos usando `if` para lógica de negocio o
> errores específicos.

## 13. Conclusión

Pydantic nos ayuda a mantener los endpoints más limpios.

En lugar de escribir validaciones repetitivas, declaramos modelos.

Pero una API real todavía necesita condiciones para tomar decisiones propias del
sistema.

En resumen:

- Pydantic valida datos.
- FastAPI usa esos modelos para validar requests y documentar la API.
- Los `if` siguen siendo necesarios para lógica de negocio.
