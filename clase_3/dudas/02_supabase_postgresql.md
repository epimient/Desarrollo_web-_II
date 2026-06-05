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

- Crear proyectos de base de datos con un clic.
- Ejecutar SQL desde un editor en el navegador.
- Ver y manejar tus tablas fácilmente.

### ¿Supabase tiene una API?

**Sí.** De hecho, esa es su magia principal. En lugar de tener que configurar servidores complicados para acceder a PostgreSQL, Supabase toma tu base de datos y automáticamente construye una **API REST** sobre ella. 

### ¿Cómo nos conectamos a Supabase?

Para conectarse, Supabase te da dos cosas:
1. Una **URL** (la dirección en internet de tu API).
2. Una **API Key** (una contraseña larga para demostrar que tienes permiso de entrar).

En Python, instalamos la librería `supabase` y la usamos para conectarnos enviando la URL y la API Key, todo a través de internet.

## En esta clase

FastAPI no se conecta a PostgreSQL escribiendo SQL manual en cada ruta. Usamos el cliente de Supabase:

```python
supabase.table("items").select("*").execute()
```

## Señal de que entendiste

Puedes explicar que Supabase es el servicio que nos permite usar PostgreSQL en la nube sin instalar PostgreSQL localmente.

