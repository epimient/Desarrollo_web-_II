# Variables de entorno y `.gitignore`

## La duda

¿Por qué no puedo escribir la clave de Supabase directamente en el código?

## Respuesta corta

Porque el código suele subirse a repositorios. Si la clave queda escrita en el código, cualquiera que vea el repositorio podría usarla.

## Archivo `.env`

El archivo `.env` guarda valores privados:

```dotenv
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_clave
APP_NAME=API Clase 3
```

## Archivo `.gitignore`

El archivo `.gitignore` le dice a Git qué no debe subir:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

## Regla práctica

Sube:

- Código fuente.
- `requirements.txt`.
- Archivos de rutas, schemas y servicios.

No subas:

- `.env`.
- Claves reales.
- Entornos virtuales.

## Señal de que entendiste

Puedes mostrar tu repositorio sin exponer `SUPABASE_KEY`.

