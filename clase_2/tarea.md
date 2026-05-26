36. Tarea
Tarea: Reorganizar y documentar la API

Cada estudiante o grupo debe entregar una API organizada con la siguiente estructura:

app/
├── main.py
├── routers/
│   ├── items.py
│   └── external.py
├── schemas/
│   └── item_schema.py
├── services/
│   └── external_service.py
└── core/
    └── config.py

Debe incluir:

Modelo ItemCreate.
Modelo ItemUpdate.
Modelo ItemResponse.
Modelo ExternalItemResponse.
Endpoint para crear item.
Endpoint para listar items.
Endpoint para consultar item por ID.
Endpoint para actualizar item.
Endpoint para eliminar item.
Endpoint para consultar una API externa.
Manejo de errores con HTTPException.
Uso de response_model.
Uso de códigos de estado HTTP.
Captura de pantalla de /docs.
37. Entregables

El estudiante debe entregar:

Carpeta del proyecto o repositorio.
Captura de /docs.
Captura de una validación fallida.
Captura de un error 404.
Breve explicación escrita de la estructura de carpetas.
38. Preguntas de sustentación

Estas preguntas pueden usarse al final o en la próxima clase:

¿Qué es un modelo Pydantic?
¿Para qué sirve BaseModel?
¿Para qué sirve Field?
¿Qué diferencia hay entre ItemCreate, ItemUpdate y ItemResponse?
¿Por qué no se recomienda usar el mismo modelo para crear, actualizar y responder?
¿Qué hace response_model?
¿Qué pasa si el cliente envía un dato inválido?
¿Qué código HTTP se usa cuando se crea un recurso?
¿Qué código HTTP se usa cuando un recurso no existe?
¿Qué es HTTPException?
¿Qué es APIRouter?
¿Por qué separamos rutas, esquemas y servicios?
¿Qué archivo se encarga de iniciar la aplicación?
¿Qué archivo contiene la lógica para consumir la API externa?
¿Por qué no devolvemos toda la respuesta original de una API externa?
¿Qué aparece automáticamente en /docs?
¿Qué significa ejecutar uvicorn app.main:app --reload?
¿Qué diferencia hay entre path parameter y request body?
¿Por qué ItemUpdate tiene campos opcionales?
¿Qué mejoraría cuando conectemos Supabase?
39. Reto corto en clase
Reto: agregar búsqueda por categoría

Agregar un endpoint:

GET /items/search?category=pokemon

Debe devolver todos los items que pertenezcan a esa categoría.

Código sugerido:

@router.get("/search/", response_model=list[ItemResponse])
def search_items_by_category(category: str):
    results = []

    for item in items_db:
        if item["category"].lower() == category.lower():
            results.append(item)

    return results

Explicación:

Aquí se practica parámetro de consulta.

La ruta se usaría así:

GET /items/search/?category=pokemon

Pregunta para los estudiantes:

¿Por qué category es query parameter y no path parameter?

Respuesta esperada:

Porque no estamos consultando un recurso único por identificador, sino filtrando una colección.

40. Reto adicional para estudiantes avanzados
Reto: guardar un resultado externo como item local

Crear un endpoint:

POST /external/pokemon/{pokemon_name}/save

Objetivo:

Consultar PokéAPI, tomar el resultado y guardarlo en items_db.

Respuesta esperada:

{
  "id": 2,
  "name": "pikachu",
  "description": "Pokemon importado desde API externa",
  "category": "pokemon",
  "source": "pokeapi"
}

Pista:

En external.py podrían importar temporalmente items_db y current_id, aunque más adelante esto debería mejorarse con una capa de servicio o base de datos.

Este reto sirve para conectar dos ideas:

consumir una API externa;
guardar información en nuestra propia API.