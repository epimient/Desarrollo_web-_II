# RLS y permisos en Supabase

## La duda

¿Por qué la tabla existe pero la API no puede insertar o leer datos?

## Respuesta corta

Puede ser por Row Level Security, conocido como RLS.

## Qué es RLS

RLS es una capa de seguridad de PostgreSQL que controla qué filas puede leer o modificar un usuario.

Si RLS está activo y no hay políticas, Supabase puede bloquear operaciones como:

- `select`
- `insert`
- `update`
- `delete`

## Síntomas comunes

- `401 Unauthorized`
- `403 Forbidden`
- El endpoint responde vacío aunque la tabla tenga datos.
- El insert no crea filas.

## Qué revisar

1. Que la API key sea correcta.
2. Que la tabla exista en `public.items`.
3. Que RLS no esté bloqueando la operación.
4. Que existan políticas para la operación que intentas ejecutar.

## Idea importante

RLS no es un error. Es una protección. En proyectos reales se configuran políticas según usuarios, roles y permisos.

## Señal de que entendiste

Puedes diferenciar entre:

```txt
La tabla no existe
```

y:

```txt
La tabla existe, pero los permisos bloquean la operación
```

