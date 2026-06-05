# UUID y fechas generadas por el servidor

## La duda

¿Por qué el `id`, `created_at` y `updated_at` no los escribe el usuario?

## Respuesta corta

Porque esos campos los debe controlar la base de datos para evitar errores y mantener consistencia.

## UUID

Un UUID es un identificador único.

Ejemplo:

```txt
6f47a90d-10db-42f8-a934-cf6a7f1fd248
```

En SQL:

```sql
id uuid primary key default gen_random_uuid()
```

Eso significa:

- `id`: columna identificadora.
- `uuid`: tipo de dato.
- `primary key`: no se repite y permite ubicar la fila.
- `default gen_random_uuid()`: PostgreSQL lo genera automáticamente.

## Fechas

```sql
created_at timestamptz not null default now()
updated_at timestamptz not null default now()
```

`created_at` indica cuándo se creó la fila.  
`updated_at` indica cuándo se actualizó por última vez.

## ¿Por qué no mandarlas desde FastAPI?

Porque el cliente podría enviar una fecha falsa, vacía o con zona horaria incorrecta.

La base de datos es una fuente más confiable para estos valores.

## Señal de que entendiste

En Swagger no envías `id`, `created_at` ni `updated_at`, pero aparecen en la respuesta.

