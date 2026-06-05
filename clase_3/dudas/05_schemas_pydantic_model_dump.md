# Schemas, Pydantic y `model_dump()`

## La duda

¿Por qué no enviamos el objeto Pydantic directamente a Supabase?

## Respuesta corta

Porque Supabase espera datos en forma de diccionario. Pydantic crea objetos de Python.

## Objeto Pydantic

```python
item = ItemCreate(
    name="Mouse",
    description="Mouse inalámbrico",
    price=85.9,
    available=True,
)
```

## Diccionario

```python
payload = item.model_dump()
```

Resultado:

```python
{
    "name": "Mouse",
    "description": "Mouse inalámbrico",
    "price": 85.9,
    "available": True,
}
```

Ese `payload` sí puede enviarse a Supabase:

```python
supabase.table("items").insert(payload).execute()
```

## Actualizaciones parciales

Para `PUT` usamos:

```python
item.model_dump(exclude_unset=True, exclude_none=True)
```

Esto evita enviar campos que no se modificaron.

## Señal de que entendiste

Puedes explicar que `model_dump()` traduce de "objeto validado por Pydantic" a "diccionario listo para Supabase".

