# Curso de Desarrollo Web II con FastAPI

Repositorio de materiales para el curso de **Desarrollo Web II**, enfocado en la
construccion de APIs web usando **FastAPI**.

El curso trabaja conceptos como:

- Creacion de APIs REST.
- Uso de FastAPI.
- Modelos y validaciones con Pydantic.
- Codigos de estado HTTP.
- Manejo de errores con `HTTPException`.
- Organizacion de proyectos por carpetas.
- Separacion de rutas con `APIRouter`.
- Consumo de APIs externas.
- Persistencia de datos con PostgreSQL y Supabase.
- Uso de variables de entorno y archivos `.env`.
- Arquitectura de capas (Rutas, Servicios, Esquemas).

## Estructura del curso

```text
.
├── clase_1/
├── clase_2/
│   ├── discurso_clase2.md
│   ├── tarea.md
│   └── dudas/
└── clase_3/
    ├── discurso_clase3.md
    ├── ejemplo/
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── core/config.py
    │   │   ├── database/supabase_client.py
    │   │   ├── routes/item_routes.py
    │   │   ├── schemas/item_schema.py
    │   │   └── services/item_service.py
    │   ├── crear_tabla_items.sql
    │   ├── .env.example
    │   ├── .gitignore
    │   └── requirements.txt
    └── dudas/
```

## Materiales

### Clase 1

Por ahora no hay archivos Markdown registrados dentro de `clase_1/`.

### Clase 2

| Material | Descripcion |
| --- | --- |
| [Modelos, Validaciones y Estructura Correcta](clase_2/discurso_clase2.md) | Guia de clase sobre Pydantic, validaciones, modelos de entrada y salida, `response_model`, codigos HTTP y organizacion del proyecto. |
| [Tarea: API de Items Academicos con FastAPI](clase_2/tarea.md) | Actividad practica para construir una API organizada por carpetas, con rutas, esquemas, servicios y consumo de una API externa. |

#### Dudas de la clase 2

| Duda | Tema |
| --- | --- |
| [Como se separan las rutas con APIRouter](clase_2/dudas/duda_estructura.md) | Explica como dividir rutas por responsabilidad usando archivos dentro de `routers/`. |
| [Que significa Item y por que usamos varios modelos](clase_2/dudas/duda_item.md) | Aclara el concepto de `Item` y la diferencia entre modelos de creacion, actualizacion y respuesta. |
| [Pydantic evita escribir muchos if](clase_2/dudas/duda_pydantic.md) | Muestra como Pydantic valida datos y reduce validaciones manuales en los endpoints. |
| [Que va en el decorador y que va dentro de la funcion](clase_2/dudas/duda_statuscode.md) | Diferencia entre parametros del decorador, como `response_model` y `status_code`, y parametros de la funcion. |

### Clase 3

| Material | Descripcion |
| --- | --- |
| [Persistencia, Supabase y Variables de Entorno](clase_3/discurso_clase3.md) | Guía sobre como conectar FastAPI con Supabase, manejo de PostgreSQL, variables de entorno, arquitectura de capas y manejo de errores. |
| [Proyecto ejemplo](clase_3/ejemplo/) | Código fuente completo de la API CRUD con FastAPI + Supabase, listo para ejecutar. |

#### Dudas de la clase 3

| Duda | Tema |
| --- | --- |
| [Memoria Volatíl vs Persistencia](clase_3/dudas/01_memoria_vs_persistencia.md) | Diferencias entre guardar datos en una lista de Python y una base de datos real. |
| [Supabase es PostgreSQL](clase_3/dudas/02_supabase_postgresql.md) | Explicación de qué es Supabase y por qué usamos PostgreSQL. |
| [UUIDs y Fechas en el Servidor](clase_3/dudas/03_uuid_fechas_servidor.md) | Por qué es mejor generar IDs y fechas en la base de datos o el backend. |
| [Variables de Entorno y Gitignore](clase_3/dudas/04_variables_entorno_gitignore.md) | Seguridad y configuración de credenciales sensibles. |
| [Pydantic y model_dump](clase_3/dudas/05_schemas_pydantic_model_dump.md) | Uso de esquemas para filtrar datos y enviar diccionarios a la base de datos. |
| [Rutas vs Servicios vs Capas](clase_3/dudas/06_rutas_servicios_capas.md) | Cómo organizar la lógica de negocio separada de los endpoints. |
| [Errores Frecuentes](clase_3/dudas/08_errores_frecuentes.md) | Solución a problemas comunes al conectar con la base de datos. |
| [PostgreSQL vs MySQL](clase_3/dudas/09_postgresql_vs_mysql.md) | Por qué PostgreSQL es el estándar de la industria IT y sus superpoderes. |
| [¿Qué es REST y RESTful?](clase_3/dudas/10_api_rest_vs_restful.md) | Explicación para principiantes sobre APIs, verbos HTTP y falta de estado. |

## Ejecucion de proyectos FastAPI

Cuando una clase incluya una aplicacion FastAPI, normalmente se puede ejecutar
con:

```bash
uvicorn app.main:app --reload
```

Luego se puede abrir la documentacion automatica en:

```text
http://127.0.0.1:8000/docs
```
