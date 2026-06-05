# Rutas, servicios y capas

## La duda

¿Por qué no ponemos todo el código dentro de la ruta?

## Respuesta corta

Porque mezclar todo hace que el proyecto sea difícil de leer, probar y modificar.

## Ruta

La ruta recibe HTTP:

```python
@router.post("/")
def create_item(item: ItemCreate):
    return item_service.create_item(item)
```

Responsabilidades de una ruta:

- Recibir la petición.
- Validar parámetros.
- Llamar al servicio correcto.
- Devolver respuesta.

## Servicio

El servicio trabaja con la base de datos:

```python
def create_item(item: ItemCreate) -> dict:
    payload = item.model_dump()
    response = supabase.table("items").insert(payload).execute()
    return response.data[0]
```

Responsabilidades de un servicio:

- Preparar datos.
- Ejecutar consultas.
- Manejar resultados.
- Lanzar errores si algo no existe.

## Comparación

| Capa | Pregunta que responde |
|---|---|
| Ruta | ¿Qué endpoint llamó el cliente? |
| Schema | ¿Los datos tienen la forma correcta? |
| Servicio | ¿Qué hago con la base de datos? |
| Cliente Supabase | ¿Cómo me conecto a Supabase? |

## Señal de que entendiste

Si mañana cambiamos Supabase por otra base de datos, las rutas deberían cambiar poco o nada.

