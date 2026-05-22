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

## Estructura del curso

```text
.
├── clase_1/
└── clase_2/
    ├── discurso_clase2.md
    ├── tarea.md
    └── dudas/
        ├── duda_estructura.md
        ├── duda_item.md
        ├── duda_pydantic.md
        └── duda_statuscode.md
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
