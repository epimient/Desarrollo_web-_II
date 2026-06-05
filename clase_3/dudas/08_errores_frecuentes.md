# Errores frecuentes

## `ModuleNotFoundError: No module named 'app'`

Estás ejecutando Uvicorn desde una carpeta incorrecta.

Ejecuta desde la carpeta que contiene `app/`:

```bash
uvicorn app.main:app --reload
```

## `Field required supabase_url`

Revisa:

- Existe `.env`.
- Está en la raíz del proyecto.
- La variable se llama `SUPABASE_URL`.
- La variable se llama `SUPABASE_KEY`.

## `relation "items" does not exist`

La tabla no existe o no está en el schema esperado.

Revisa en Supabase:

```txt
Table Editor -> items
```

También confirma que el SQL se ejecutó en `public`.

## Error con UUID

Si haces:

```txt
GET /items/123
```

puede fallar porque `123` no es un UUID.

Usa el `id` real que devuelve `POST /items/`.

## No se actualiza nada

Revisa que el body de `PUT` tenga al menos un campo:

```json
{
  "price": 99.9
}
```

Si envías `{}`, el servicio debe responder que no hay campos para actualizar.

## No aparecen las rutas en Swagger

Revisa que `main.py` tenga:

```python
app.include_router(item_router)
```

## Se expuso la clave por accidente

1. Elimina la clave del repositorio.
2. Agrega `.env` a `.gitignore`.
3. Regenera o cambia la clave si es necesario.
4. No vuelvas a compartir capturas donde aparezca completa.

