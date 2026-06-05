# Memoria vs persistencia

## La duda

¿Por qué se pierden los datos si uso una lista de Python?

## Respuesta corta

Porque una lista como `items_db = []` vive dentro de la memoria del proceso de Python. Cuando el servidor se apaga, ese proceso termina y la memoria se limpia.

## Ejemplo

```python
items_db = []
items_db.append({"name": "Mouse"})
```

Mientras Uvicorn sigue encendido, el item existe. Si detienes Uvicorn y lo vuelves a iniciar, Python vuelve a ejecutar:

```python
items_db = []
```

La lista empieza vacía otra vez.

## Persistencia

Persistir significa guardar información en un lugar que sobreviva al reinicio del programa.

Ejemplos:

- Una base de datos.
- Un archivo.
- Un servicio en la nube.

En esta clase usamos Supabase, que guarda los datos en PostgreSQL.

## Señal de que entendiste

Puedes reiniciar Uvicorn, ejecutar `GET /items/` y los datos siguen apareciendo.

