# Supabase y PostgreSQL

## La duda

¿Supabase es la base de datos o es otra cosa?

## Respuesta corta

Supabase es una plataforma. Dentro de Supabase usamos una base de datos PostgreSQL.

## Relación

```txt
Supabase = plataforma
PostgreSQL = motor de base de datos
Tabla items = lugar donde guardamos filas
```

Supabase facilita:

- Crear proyectos.
- Ejecutar SQL.
- Ver tablas desde el navegador.
- Obtener URL y API key.
- Conectarse desde Python con un SDK.

## En esta clase

FastAPI no se conecta a PostgreSQL escribiendo SQL manual en cada ruta. Usamos el cliente de Supabase:

```python
supabase.table("items").select("*").execute()
```

## Señal de que entendiste

Puedes explicar que Supabase es el servicio que nos permite usar PostgreSQL en la nube sin instalar PostgreSQL localmente.

