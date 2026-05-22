# Modelos, Validaciones y Estructura Profesional en FastAPI

## 1. Introducción al Desarrollo de APIs Profesionales

En la sesión anterior, aprendiste a consumir una API externa utilizando `requests` y a dar tus primeros pasos creando endpoints sencillos con FastAPI. Ahora es momento de avanzar hacia el siguiente nivel. 

En el desarrollo de software profesional, una API no se limita únicamente a "responder datos". Para construir aplicaciones robustas, escalables y seguras, una API debe:

*   **Validar los datos de entrada:** Garantizar que la información recibida cumpla con formatos, tipos y longitudes esperados antes de procesarla.
*   **Controlar la salida:** Asegurar que la API devuelva únicamente la información pertinente, protegiendo datos sensibles o innecesarios.
*   **Gestionar errores de manera clara:** Responder con códigos HTTP adecuados y mensajes descriptivos cuando algo falle.
*   **Organizar el código de forma modular:** Separar el proyecto por responsabilidades (rutas, esquemas, servicios, configuración) en lugar de escribir todo en un solo archivo.
*   **Documentar de forma automática:** Facilitar que otros desarrolladores entiendan y prueben los endpoints sin esfuerzo.

FastAPI nos facilita enormemente estas tareas gracias a su integración nativa con **Pydantic** para la definición y validación de esquemas, y a herramientas como **APIRouter** para estructurar proyectos de gran escala.

---

## 2. ¿Qué aprenderás en esta guía?

Al finalizar el estudio y la práctica de esta guía, serás capaz de:

*   Crear modelos de datos con Pydantic utilizando `BaseModel`.
*   Implementar validaciones avanzadas de datos con tipos de Python y la clase `Field`.
*   Explicar la diferencia entre modelos de creación (`Create`), actualización (`Update`) y respuesta (`Response`), y por qué no debes reutilizar un único modelo para todo.
*   Utilizar `response_model` para controlar y filtrar la salida de tus endpoints.
*   Definir códigos de estado HTTP semánticos y adecuados en cada ruta.
*   Lanzar excepciones controladas utilizando `HTTPException`.
*   Estructurar un proyecto de FastAPI en directorios modulares.
*   Utilizar `APIRouter` para dividir y organizar tus rutas por componentes.

---

## 3. Reflexión Inicial

Antes de entrar en el código, detente un momento a pensar en lo siguiente:

> *Si una API acepta cualquier dato que le envíe el cliente sin realizar ninguna validación, ¿qué problemas podrían surgir en el sistema?*

Si lo analizas, la falta de validación de datos provoca:
*   Registros con información incompleta o inconsistente en la base de datos.
*   Campos con tipos de datos incorrectos (por ejemplo, texto donde debería ir un número), lo que genera fallos inesperados en el backend.
*   Vulnerabilidades de seguridad y fallos lógicos difíciles de depurar.
*   Exposición involuntaria de datos internos del sistema.

En esta guía aprenderás a definir reglas claras para tu API: qué datos acepta, qué datos responde y cómo estructurar el código para evitar el desorden a medida que la aplicación crece.

---

## 4. Concepto 1: ¿Qué es Pydantic y cómo funciona?

**Pydantic** es una biblioteca de Python utilizada por FastAPI para definir la estructura y realizar la validación de los datos que entran o salen de la API. 

En palabras sencillas: **Pydantic te permite definir contratos de datos.** Le indica a Python: *"este objeto debe tener exactamente estos campos, con estos tipos de datos y estas reglas específicas"*.

Si un cliente envía una petición que no cumple con estas reglas, FastAPI y Pydantic interceptan la solicitud y devuelven automáticamente un error detallado, impidiendo que el código del endpoint se ejecute con datos corruptos.

### Ejemplo base de un esquema

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str
    source: str | None = None
```

### Explicación detallada del esquema:

*   `from pydantic import BaseModel, Field`: Importamos `BaseModel` (la clase base para construir cualquier modelo en Pydantic) y `Field` (una herramienta para aplicar reglas de validación adicionales y agregar metadatos a los campos).
*   `class ItemCreate(BaseModel):`: Definimos un modelo llamado `ItemCreate`. Este modelo representará la estructura exacta que esperamos recibir cuando el cliente envíe una petición para registrar o crear un nuevo ítem.
*   `name: str = Field(min_length=3, max_length=80)`: Definimos que el campo `name` es de tipo texto (`str`), obligatorio, y debe tener una longitud mínima de 3 caracteres y máxima de 80.
*   `description: str | None = None`: El campo `description` acepta valores de tipo texto o nulo (`None`). Al asignarle `= None` al final, le indicamos a la API que este campo es opcional.
*   `category: str`: El campo `category` es de tipo texto y es obligatorio (ya que no tiene un valor por defecto asignado).
*   `source: str | None = None`: El campo `source` es opcional. Nos servirá en la práctica para identificar la fuente del ítem (por ejemplo, `"local"` o `"pokeapi"`).

Cuando intentamos inicializar un modelo de Pydantic con datos incorrectos, la biblioteca realiza un análisis (*parsing*) de tipos y lanza un error si la validación falla.

---

## 5. Concepto 2: ¿Por qué no usar el mismo modelo para todo?

Un error muy común al iniciar en FastAPI es intentar usar un único modelo Pydantic para todas las operaciones (creación, edición y respuesta). Aunque parezca que ahorra código al principio, es una mala práctica de diseño.

### Ejemplo de diseño incorrecto (modelo único):

```python
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None
```

### ¿Por qué esto es un problema?

1.  **En la Creación (POST):** El cliente no debería enviar el `id` al crear un elemento, ya que el `id` generalmente es generado de forma automática por la base de datos o por la lógica interna del servidor. Si usamos el modelo anterior, obligaríamos al cliente a mandar un `id` inventado o tendríamos que hacerlo opcional, lo cual debilita el contrato.
2.  **En la Actualización (PUT/PATCH):** Si un usuario quiere editar únicamente el nombre de un elemento, no debería estar obligado a enviar de nuevo la descripción o la categoría. En una actualización, la mayoría de los campos deberían ser opcionales.
3.  **En la Respuesta (Response):** Al responder, sí necesitamos incluir el `id` del recurso generado. Además, es posible que queramos ocultar ciertos campos internos de la base de datos (como contraseñas, hashes o fechas de creación del sistema) que el usuario final no tiene por qué ver.

Por estas razones, la mejor práctica es **separar los modelos según su contexto de uso**.

---

## 6. Estructura de Modelos Recomendada

Siguiendo las mejores prácticas, definiremos nuestros esquemas en un archivo dedicado:

**Ruta sugerida:** `app/schemas/item_schema.py`

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str = Field(min_length=3, max_length=50)
    source: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=80)
    description: str | None = None
    category: str | None = Field(default=None, min_length=3, max_length=50)
    source: str | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None


class ExternalItemResponse(BaseModel):
    external_id: int
    name: str
    source: str
```

### Análisis de cada modelo:

*   `ItemCreate`: Controla estrictamente los datos mínimos que se requieren para insertar un elemento. No expone el `id` porque no es responsabilidad del cliente generarlo.
*   `ItemUpdate`: Todos sus campos son opcionales (`str | None = Field(default=None, ...)`). Esto permite realizar actualizaciones parciales de manera segura. Si el cliente solo envía `{ "name": "Nuevo Nombre" }`, el backend actualizará únicamente ese campo sin alterar ni sobreescribir los demás con valores nulos.
*   `ItemResponse`: Define el formato exacto de salida de la API. Este modelo garantiza que la API siempre devolverá el `id` generado junto con el resto de la información del elemento.
*   `ExternalItemResponse`: Se utiliza para estructurar las respuestas provenientes de servicios o APIs externas. Por ejemplo, al consumir datos de la *PokéAPI*, esta devuelve cientos de campos innecesarios. Con este modelo, filtramos la información para entregarle al usuario únicamente el `external_id`, el `name` y el origen `source`.

---

## 7. Concepto 3: Controlando la Salida con `response_model`

FastAPI incluye un parámetro en sus decoradores de ruta llamado `response_model`. Su función principal es indicarle al framework qué modelo de Pydantic debe utilizar para serializar y filtrar la respuesta que se envía al cliente.

### Ejemplo de uso:

```python
@router.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    ...
```

Al declarar esto, FastAPI se encarga automáticamente de:
1.  **Validar la salida:** Asegurar que los datos que tu función retorna cumplan con la estructura de `ItemResponse`.
2.  **Filtrar los datos:** Si tu función retorna campos adicionales que no pertenecen a `ItemResponse`, FastAPI los omitirá y no los enviará en el JSON de respuesta.
3.  **Documentar el endpoint:** En la interfaz interactiva de Swagger (`/docs`), se mostrará claramente a los consumidores de tu API la estructura exacta del JSON que recibirán de vuelta.

---

## 8. Concepto 4: Códigos de Estado HTTP

Los códigos de estado HTTP son la forma estándar en que un servidor web le comunica al cliente el resultado de su solicitud. Es crucial utilizarlos correctamente para que las aplicaciones cliente (web, móviles u otras APIs) puedan tomar decisiones en consecuencia.

### Tabla de códigos de estado esenciales:

| Código | Nombre | Cuándo se debe utilizar |
| :---: | :--- | :--- |
| **`200`** | `OK` | La solicitud fue exitosa (se usa comúnmente para consultas `GET` y actualizaciones `PUT`). |
| **`201`** | `Created` | La solicitud fue exitosa y se ha creado un nuevo recurso en el servidor (`POST`). |
| **`204`** | `No Content` | La acción se completó con éxito, pero la respuesta no contiene cuerpo (común en eliminaciones `DELETE`). |
| **`400`** | `Bad Request` | La solicitud del cliente es incorrecta o contiene errores lógicos que impiden procesarla. |
| **`404`** | `Not Found` | El recurso solicitado no se encuentra en el servidor. |
| **`422`** | `Unprocessable Entity` | Los datos enviados no pasaron las reglas de validación (por ejemplo, Pydantic detectó un tipo incorrecto o faltan campos obligatorios). |

En FastAPI, puedes definir el código de éxito por defecto directamente en el decorador:

```python
from fastapi import status


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    ...
```

> **Buenas prácticas:** Utiliza siempre el módulo `status` de `fastapi`. De este modo, evitas usar "números mágicos" y tu código se vuelve mucho más legible y autoexplicativo (es mejor leer `status.HTTP_201_CREATED` que simplemente escribir `201`).

---

## 9. Concepto 5: Manejo de Errores con `HTTPException`

Cuando algo falla en tu aplicación (por ejemplo, buscas un usuario por su ID y no existe), nunca debes retornar diccionarios con mensajes de error genéricos acompañados de un código de estado de éxito.

### Enfoque Incorrecto (Mala práctica):
```python
# Retorna un código HTTP 200 (éxito) pero el cuerpo dice que es un error.
# Esto confunde a los clientes de tu API.
return {"error": "No encontrado"}
```

### Enfoque Correcto:
```python
from fastapi import HTTPException, status

if not item:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El recurso solicitado no existe"
    )
```

Al utilizar `raise HTTPException(...)`, FastAPI interrumpe inmediatamente el flujo normal de la función y genera una respuesta HTTP formal con el código de error especificado y una estructura estandarizada en el JSON de respuesta:

```json
{
  "detail": "El recurso solicitado no existe"
}
```

---

## 10. Concepto 6: Modularidad y Separación de Archivos

Cuando creas tus primeras APIs, es común escribir todo el código en un único archivo `main.py`. Sin embargo, a medida que agregas endpoints, modelos y lógica de negocio, ese archivo único se vuelve gigantesco, difícil de leer y propenso a conflictos de código.

La solución profesional consiste en aplicar el principio de **Separación de Responsabilidades**, dividiendo el código en carpetas y archivos especializados de acuerdo con su función:

*   **Punto de entrada (`main.py`):** Inicializa la aplicación y registra los componentes globales. No debe contener lógica de endpoints.
*   **Enrutadores (`routers/`):** Definen únicamente las rutas (endpoints) de la aplicación, los parámetros requeridos y los códigos de respuesta.
*   **Esquemas (`schemas/`):** Contienen los modelos de Pydantic que validan las entradas y salidas de datos.
*   **Servicios (`services/`):** Alojan la lógica de negocio pesada, la comunicación con bases de datos o el consumo de APIs de terceros.
*   **Configuración (`core/`):** Define variables de entorno, credenciales y configuraciones generales del proyecto.

---

## 11. Estructura del Proyecto

Para la aplicación que desarrollaremos en esta sesión, implementaremos la siguiente estructura jerárquica de archivos:

```text
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
```

Esta estructura mantiene el código limpio, modular y listo para crecer cuando necesitemos integrar bases de datos reales como PostgreSQL o Supabase.

---

## 12. Proyecto Práctico: API de Ítems Académicos

A continuación, construirás de forma guiada una API estructurada profesionalmente. Esta API permitirá:

1.  Crear ítems académicos (almacenados en una lista temporal en memoria).
2.  Listar todos los ítems registrados.
3.  Consultar un ítem específico por su ID.
4.  Actualizar la información de un ítem existente.
5.  Eliminar un ítem del sistema.
6.  Consultar un Pokémon de forma externa en la *PokéAPI*, adaptando el resultado a nuestro modelo limpio.

Sigue paso a paso las instrucciones detalladas a continuación para armar tu proyecto.

---

## 13. Paso 1: Creación de la Estructura de Directorios

Abre tu terminal y ubícate en tu espacio de trabajo. Ejecuta los siguientes comandos para crear la estructura de carpetas:

```bash
mkdir clase_2_fastapi
cd clase_2_fastapi
mkdir app
mkdir app/routers
mkdir app/schemas
mkdir app/services
mkdir app/core
```

Una vez creadas las carpetas, genera los archivos correspondientes:

```bash
touch app/main.py
touch app/routers/items.py
touch app/routers/external.py
touch app/schemas/item_schema.py
touch app/services/external_service.py
touch app/core/config.py
```

*(Si estás en Windows PowerShell y el comando `touch` no está disponible, puedes utilizar `New-Item app/main.py` para cada archivo o crearlos manualmente desde tu editor de código).*

---

## 14. Paso 2: Configuración del Entorno Virtual e Instalación

Para mantener aisladas las dependencias del proyecto, crea y activa un entorno virtual en la raíz de `clase_2_fastapi`:

### En macOS y Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### En Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\activate
```

Una vez activado el entorno virtual, instala FastAPI, Uvicorn (para ejecutar el servidor local) y Requests (para realizar la consulta externa):

```bash
pip install fastapi uvicorn requests
```

---

## 15. Paso 3: Implementación de Modelos Pydantic

Abre el archivo `app/schemas/item_schema.py` y escribe la estructura de modelos que estudiamos anteriormente. Estos modelos servirán como contrato de datos para el resto de la aplicación:

```python
# app/schemas/item_schema.py
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str | None = None
    category: str = Field(min_length=3, max_length=50)
    source: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=80)
    description: str | None = None
    category: str | None = Field(default=None, min_length=3, max_length=50)
    source: str | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    source: str | None = None


class ExternalItemResponse(BaseModel):
    external_id: int
    name: str
    source: str
```

---

## 16. Paso 4: Creación del Enrutador de Ítems (`APIRouter`)

Escribe la lógica del CRUD de ítems en `app/routers/items.py`. Aquí utilizaremos `APIRouter` y una lista en memoria (`items_db`) que actuará como base de datos temporal:

```python
# app/routers/items.py
from fastapi import APIRouter, HTTPException, status
from app.schemas.item_schema import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

# Base de datos temporal en memoria
items_db = []
current_id = 1


@router.get("/", response_model=list[ItemResponse])
def get_items():
    """Retorna la lista de todos los ítems registrados."""
    return items_db


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    """Busca y retorna un ítem específico por su ID."""
    for item in items_db:
        if item["id"] == item_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El item solicitado no existe"
    )


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    """Crea un nuevo ítem y lo almacena en la base de datos temporal."""
    global current_id

    new_item = {
        "id": current_id,
        "name": item.name,
        "description": item.description,
        "category": item.category,
        "source": item.source
    }

    items_db.append(new_item)
    current_id += 1

    return new_item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate):
    """Actualiza parcialmente un ítem existente."""
    for item in items_db:
        if item["id"] == item_id:
            # Convertimos el esquema a diccionario ignorando los campos no enviados
            update_data = item_data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                item[key] = value

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se puede actualizar porque el item no existe"
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """Elimina un ítem específico por su ID."""
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se puede eliminar porque el item no existe"
    )
```

---

## 17. Desglose del Enrutador de Ítems

Revisemos las partes clave que acabas de escribir en el archivo anterior:

*   **`prefix="/items"`:** Al configurar esto en `APIRouter`, le indicamos a FastAPI que todas las rutas declaradas en este archivo comenzarán automáticamente con la ruta `/items`. Por lo tanto, un endpoint definido como `@router.get("/")` estará expuesto en `/items/` de cara al cliente.
*   **`tags=["Items"]`:** Permite etiquetar las rutas. En la interfaz gráfica de Swagger UI (`/docs`), todos estos endpoints aparecerán prolijamente agrupados bajo la sección "Items".
*   **`exclude_unset=True` en `model_dump()`:** Esto es fundamental en el método `update_item`. Convierte el modelo Pydantic `ItemUpdate` en un diccionario común de Python, pero **omitiendo los campos que el cliente no envió en su petición**. De esta forma, si el cliente solo envía el campo `name`, el diccionario resultante será `{"name": "Nuevo Nombre"}` y no alterará los campos `description` o `category` existentes.
*   **Uso de `global current_id`:** Dado que estamos usando una lista simple en memoria, utilizamos una variable global de Python para llevar el conteo incremental y único de los identificadores (`id`) de cada elemento creado.

---

## 18. Paso 5: Consumo de APIs Externas (Servicios)

De acuerdo con el principio de separación de responsabilidades, la lógica necesaria para consultar a la *PokéAPI* externa no debe estar directamente en el archivo de rutas (router). En su lugar, la colocaremos dentro de un módulo de servicios.

Abre el archivo `app/services/external_service.py` e implementa la función de consulta externa:

```python
# app/services/external_service.py
import requests
from fastapi import HTTPException, status


def get_pokemon_from_api(pokemon_name: str):
    """Consulta la PokéAPI y retorna los datos mapeados al formato de nuestra API."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La API externa no está disponible en este momento"
        )

    # Si la API externa responde que el recurso no existe
    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El pokemon '{pokemon_name}' no existe en la API externa"
        )

    # Si ocurre otro fallo en el servidor externo
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error inesperado al consultar la API externa"
        )

    data = response.json()

    # Mapeamos los datos de la respuesta original a nuestra estructura limpia
    return {
        "external_id": data["id"],
        "name": data["name"],
        "source": "pokeapi"
    }
```

---

## 19. Desglose del Servicio Externo

Al separar este servicio, logramos que el código sea modular y robusto:

*   **Aislamiento:** Si mañana la API externa cambia de formato o de proveedor (por ejemplo, pasamos de usar PokéAPI a otra API de videojuegos), solo necesitaremos modificar el archivo `external_service.py`. Las rutas e interfaces del frontend permanecerán intactas.
*   **Traducción de Errores (Bad Gateway):** Si la API de Pokémon responde con errores inesperados o se cae, nuestro backend intercepta ese evento y responde de manera elegante con un código **`502 Bad Gateway`** o **`503 Service Unavailable`**, indicando al cliente que el problema radica en un servicio de terceros y no en nuestra propia aplicación.
*   **Mapeo de Datos:** El servicio toma el JSON crudo del exterior (que contiene cientos de claves complejas como sprites, habilidades y estadísticas) y extrae únicamente los tres campos necesarios para cumplir con `ExternalItemResponse`.

---

## 20. Paso 6: Creación del Enrutador Externo

Una vez que la lógica de negocio para consultar la API externa está lista en el servicio, crearemos el router que expondrá esta funcionalidad a los usuarios.

Abre el archivo `app/routers/external.py` y define la ruta:

```python
# app/routers/external.py
from fastapi import APIRouter
from app.schemas.item_schema import ExternalItemResponse
from app.services.external_service import get_pokemon_from_api

router = APIRouter(
    prefix="/external",
    tags=["External API"]
)


@router.get("/pokemon/{pokemon_name}", response_model=ExternalItemResponse)
def get_external_pokemon(pokemon_name: str):
    """Endpoint para consultar y obtener un pokemon adaptado desde la API externa."""
    return get_pokemon_from_api(pokemon_name)
```

---

## 21. Desglose del Enrutador Externo

Este router es sumamente sencillo e ilustra a la perfección el principio de modularidad:

*   **Responsabilidad única:** El endpoint se limita a recibir la petición HTTP, pasar el parámetro `pokemon_name` al servicio correspondiente, y retornar el diccionario obtenido.
*   **Seguridad en el formato:** El parámetro `response_model=ExternalItemResponse` asegura que lo que retorne el servicio `get_pokemon_from_api` se ajustará estrictamente al modelo esperado antes de ser entregado al cliente final.

---

## 22. Paso 7: Configuración de la Aplicación

Para centralizar los valores globales y la metadata de tu API, utilizaremos el módulo de configuración `app/core/config.py`. Abre el archivo e inserta estas variables de configuración básicas:

```python
# app/core/config.py
APP_NAME = "API de Items Académicos"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "API académica para la práctica avanzada de modelos, "
    "validaciones, routers y estructuras de carpetas profesionales con FastAPI."
)
```

*(En proyectos futuros y en producción, este archivo se ampliará para importar bibliotecas como `pydantic-settings` y cargar de forma segura variables de entorno de un archivo `.env`, tales como contraseñas de bases de datos o llaves de API).*

---

## 23. Paso 8: El Punto de Entrada Central (`main.py`)

Con todos los módulos y submódulos creados, es momento de unirlos en la aplicación principal. Abre `app/main.py` y escribe el siguiente código:

```python
# app/main.py
from fastapi import FastAPI
from app.core.config import APP_NAME, APP_VERSION, APP_DESCRIPTION
from app.routers import items, external

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION
)

# Conectamos los enrutadores modulares a la aplicación central
app.include_router(items.router)
app.include_router(external.router)


@app.get("/")
def root():
    """Ruta raíz de la API para verificar el estado del servicio."""
    return {
        "message": f"Bienvenido a la {APP_NAME}",
        "docs": "/docs",
        "status": "online"
    }
```

---

## 24. Desglose de `main.py`

*   **Instancia central de `FastAPI`:** Configura el título, la versión y la descripción de la aplicación importando los valores globales definidos en `app/core/config.py`.
*   **`app.include_router(...)`:** Registra los routers modulares en el núcleo del framework. Si olvidas llamar a `include_router` para alguno de tus módulos, FastAPI no sabrá que esos archivos existen y sus endpoints arrojarán errores `404 Not Found` al intentar consultarlos.

---

## 25. Paso 9: Ejecución de la Aplicación

Asegúrate de tener el entorno virtual activo en tu terminal y de encontrarte en el directorio raíz del proyecto (`clase_2_fastapi`, justo en la carpeta que contiene el directorio `app/`). Ejecuta el servidor de desarrollo local utilizando `uvicorn`:

```bash
uvicorn app.main:app --reload
```

### ¿Qué significan estos argumentos?

*   `app.main:app`: Indica que busque el módulo `main.py` dentro de la carpeta `app`, y que dentro de él ejecute la variable de aplicación `app = FastAPI()`.
*   `--reload`: Modo desarrollo. Reinicia el servidor de manera automática cada vez que detecta un cambio en tus archivos de código.

Abre tu navegador de preferencia y dirígete a:
*   Página de inicio: [http://127.0.0.1:8000](http://127.0.0.1:8000)
*   Documentación Interactiva (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 26. Rutas Disponibles en la Documentación Automática

Al acceder a la documentación interactiva en `/docs`, deberás visualizar la lista completa de endpoints registrados y agrupados adecuadamente:

```http
GET     /                                   Ruta raíz de estado
GET     /items/                             Obtener todos los ítems
POST    /items/                             Registrar un nuevo ítem
GET     /items/{item_id}                    Consultar un ítem por ID
PUT     /items/{item_id}                    Actualizar un ítem por ID
DELETE  /items/{item_id}                    Eliminar un ítem por ID
GET     /external/pokemon/{pokemon_name}    Consultar Pokémon externo
```

---

## 27. Pruebas y Validación de Funcionamiento

A continuación, se describen los escenarios clave que debes probar en la documentación interactiva (o mediante herramientas como Postman o Insomnia) para verificar que las validaciones y los flujos funcionen correctamente:

### Escenario 1: Creación Exitosa de un Ítem
*   **Endpoint:** `POST /items/`
*   **Cuerpo del JSON:**
    ```json
    {
      "name": "Pikachu de Felpa",
      "description": "Juguete coleccionable de tipo eléctrico",
      "category": "Juguetes",
      "source": "manual"
    }
    ```
*   **Resultado esperado:** Código HTTP `201 Created`. El JSON de respuesta debe incluir el `"id": 1` asignado automáticamente.

### Escenario 2: Intento de Creación con Datos Inválidos (Fallo de Validación)
*   **Endpoint:** `POST /items/`
*   **Cuerpo del JSON:**
    ```json
    {
      "name": "Pi",
      "description": "Nombre demasiado corto",
      "category": "Juguetes"
    }
    ```
*   **Resultado esperado:** Código HTTP `422 Unprocessable Entity`. FastAPI y Pydantic detendrán la solicitud indicando que el campo `name` requiere una longitud mínima de 3 caracteres.

### Escenario 3: Obtener la Lista de Ítems
*   **Endpoint:** `GET /items/`
*   **Resultado esperado:** Código HTTP `200 OK`. Retorna un arreglo JSON conteniendo el ítem creado en el Escenario 1.

### Escenario 4: Consultar un Ítem Inexistente
*   **Endpoint:** `GET /items/999`
*   **Resultado esperado:** Código HTTP `404 Not Found` con el mensaje JSON `{"detail": "El item solicitado no existe"}`.

### Escenario 5: Actualizar Parcialmente un Ítem
*   **Endpoint:** `PUT /items/1`
*   **Cuerpo del JSON:**
    ```json
    {
      "name": "Pikachu Gigante Actualizado"
    }
    ```
*   **Resultado esperado:** Código HTTP `200 OK`. La respuesta debe mostrar el nombre actualizado, pero manteniendo la descripción y categoría intactas (gracias a `exclude_unset=True`).

### Escenario 6: Consultar un Pokémon Existente en la API Externa
*   **Endpoint:** `GET /external/pokemon/charmander`
*   **Resultado esperado:** Código HTTP `200 OK`. La respuesta JSON debe tener la forma reducida especificada en tu modelo:
    ```json
    {
      "external_id": 4,
      "name": "charmander",
      "source": "pokeapi"
    }
    ```

### Escenario 7: Consultar un Pokémon que no Existe en la API Externa
*   **Endpoint:** `GET /external/pokemon/no_existe_este_nombre`
*   **Resultado esperado:** Código HTTP `404 Not Found`.

---

## 28. Resumen de Responsabilidades de cada Archivo

A modo de repaso, revisa cómo fluye la información y qué rol cumple cada pieza del rompecabezas:

1.  **`main.py`:** Es la puerta de entrada. Agrupa todos los enrutadores y arranca la aplicación.
2.  **`routers/items.py` y `routers/external.py`:** Controlan el tráfico de entrada. Definen las URLs, reciben los parámetros y deciden qué responder.
3.  **`schemas/item_schema.py`:** Define las reglas del juego. Valida que los datos que entran y salen tengan el formato correcto.
4.  **`services/external_service.py`:** Realiza el trabajo pesado fuera de la API. Se comunica con servidores externos y procesa sus respuestas.
5.  **`core/config.py`:** Almacena los metadatos globales del proyecto.

---

## 29. Desafío Práctico: Reorganiza tu API

**Tu turno de practicar:** A partir del proyecto que construiste en la clase anterior, reestructúralo por completo para aplicar este diseño modular.

### Requisitos del Desafío:
1.  Crea la estructura de carpetas `app/`, `routers/`, `schemas/`, `services/` y `core/`.
2.  Configura e implementa los 4 esquemas de Pydantic estudiados en `item_schema.py`.
3.  Asegura el correcto registro de los routers en `main.py` empleando `app.include_router()`.
4.  Define códigos de estado HTTP semánticos en todos tus endpoints usando `status`.
5.  Verifica que tus respuestas devuelvan exactamente lo que deseas a través de `response_model`.

---

## 30. Preguntas de Autoevaluación

Para verificar que has comprendido los conceptos teóricos clave de esta sesión, intenta responder a las siguientes preguntas:

*   *¿Qué archivo de nuestro proyecto se encarga de levantar y configurar la aplicación principal de FastAPI?*
*   *¿Por qué el modelo `ItemCreate` no debe definir el campo `id`?*
*   *¿Cuál es la diferencia de comportamiento entre usar `ItemCreate` y usar `ItemUpdate` en los endpoints correspondientes?*
*   *¿Cuál es el beneficio de utilizar `response_model` en los decoradores de rutas?*
*   *Si ingresas a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) y una ruta que creaste no aparece en la lista, ¿qué validación deberías hacer en `main.py`?*
*   *¿Qué diferencia conceptual y de código HTTP existe entre un error `404` y un error `422`?*
*   *¿Por qué es una mala práctica retornar un mensaje de error plano en un diccionario (como `return {"error": "..."}`) en lugar de lanzar una `HTTPException`?*

---

## 31. Concepto Adicional: Validación Automática de Datos

Una de las mayores ventajas de FastAPI y Pydantic es que no necesitas escribir validaciones manuales repetitivas en tus funciones.

### Ejemplo de código manual (Mala práctica / Tedioso):
```python
# Sin Pydantic, tendrías que validar todo a mano en cada función
@app.post("/items")
def create_item(name: str, category: str):
    if not name or len(name) < 3:
        return {"error": "El nombre debe tener al menos 3 caracteres"}
    if not category:
        return {"error": "La categoría es obligatoria"}
    # ... más validaciones
```

Con FastAPI, al definir `item: ItemCreate`, Pydantic se encarga de interceptar y rechazar solicitudes no válidas antes de que toquen tu base de datos o lógica interna. Esto reduce drásticamente el código boilerplate de validaciones en tu backend.

---

## 32. Concepto Adicional: Documentación Interactiva

FastAPI lee la firma de tus funciones (los tipos de datos de los argumentos, los valores por defecto y el `response_model`) y genera automáticamente la especificación OpenAPI de tu aplicación. 

Esto se traduce en la interfaz interactiva de Swagger UI que consultas en `/docs`. A través de ella, no solo puedes leer cómo consumir tu API, sino que puedes realizar peticiones de prueba en tiempo real directamente desde el navegador haciendo clic en el botón **"Try it out"**.

---

## 33. Concepto Adicional: Filtrado y Seguridad con `response_model`

Imagina que tu base de datos contiene información de usuarios con la siguiente estructura interna:

```python
user_in_db = {
    "id": 42,
    "name": "Sofía Díaz",
    "email": "sofia@example.com",
    "password_hash": "pbkdf2:sha256:260000$tY2b9..."
}
```

Si retornas el diccionario completo directamente, estarías exponiendo la contraseña cifrada a la red, lo que representa un grave problema de seguridad. 

Sin embargo, si defines un modelo de respuesta restrictivo en Pydantic:

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```

Y declaras en tu endpoint `@router.get("/users/{id}", response_model=UserResponse)`, FastAPI filtrará la información y solo retornará el `id`, `name` y `email`, removiendo de manera segura el campo `password_hash` del JSON enviado al cliente.

---

## 34. Guía de Solución de Problemas (Troubleshooting)

Si encuentras dificultades al levantar o probar tu proyecto, consulta esta lista de errores comunes y sus soluciones:

### Problema 1: "ModuleNotFoundError: No module named 'app'"
*   **Causa:** Estás ejecutando el comando de `uvicorn` desde la carpeta incorrecta (por ejemplo, dentro del directorio `app/`), o bien no tienes el entorno virtual configurado y activo en esa ventana de la terminal.
*   **Solución:** Posiciónate en la carpeta raíz del proyecto (donde se encuentra la carpeta `app/` como subdirectorio) y ejecuta `uvicorn app.main:app --reload`.

### Problema 2: "Las rutas no aparecen en /docs o me da 404 al consultarlas"
*   **Causa:** Creaste correctamente las rutas en tu archivo de router (`items.py` o `external.py`), pero olvidaste importarlo y registrarlo en el archivo raíz.
*   **Solución:** Ve a `app/main.py` y asegúrate de tener las líneas `app.include_router(items.router)` y `app.include_router(external.router)`.

### Problema 3: "Al actualizar un ítem, los campos que no envío se borran o se ponen en null"
*   **Causa:** En tu endpoint de actualización (`PUT`), convertiste el modelo a diccionario usando simplemente `item_data.model_dump()` sin parámetros.
*   **Solución:** Asegúrate de usar `item_data.model_dump(exclude_unset=True)`. Esto garantiza que los campos que el cliente no envió en su JSON sean omitidos en la actualización, previniendo la sobreescritura accidental.

### Problema 4: "Fallo al consultar Pokémon externo (502 Bad Gateway)"
*   **Causa:** Tu servidor local no tiene acceso a internet para comunicarse con la PokéAPI, o bien escribiste mal la URL base del servicio externo en el archivo `external_service.py`.
*   **Solución:** Verifica tu conexión a internet e inspecciona detalladamente la sintaxis de la URL en `get_pokemon_from_api`.

---

## 35. Conclusiones y Siguientes Pasos

¡Felicidades! Has dado un gran paso al estructurar tu aplicación de manera profesional. Has aprendido a validar datos de entrada, filtrar información de salida, mapear respuestas de servicios externos y organizar el backend en directorios con responsabilidades delimitadas.

Aunque por el momento tus datos se pierden al reiniciar el servidor debido al almacenamiento temporal en memoria, has dejado el proyecto listo para una transición limpia y directa hacia una base de datos persistente. En la siguiente sesión, conectarás esta misma estructura a Supabase y PostgreSQL para almacenar tu información de manera permanente.

---

## Referencias Oficiales de Consulta

Para profundizar en los temas abordados, puedes revisar la documentación oficial:

*   [FastAPI: Cuerpo de Petición (Request Body)](https://fastapi.tiangolo.com/tutorial/body/)
*   [FastAPI: Parámetros del Cuerpo y Campos (Body Fields)](https://fastapi.tiangolo.com/tutorial/body-fields/)
*   [FastAPI: Modelo de Respuesta (Response Model)](https://fastapi.tiangolo.com/es/tutorial/response-model/)
*   [FastAPI: Códigos de Estado de Respuesta (Response Status Code)](https://fastapi.tiangolo.com/es/tutorial/response-status-code/)
*   [FastAPI: Manejo de Errores (Handling Errors)](https://fastapi.tiangolo.com/es/tutorial/handling-errors/)
*   [FastAPI: Aplicaciones Más Grandes - Múltiples Archivos (Bigger Applications)](https://fastapi.tiangolo.com/es/tutorial/bigger-applications/)
*   [Pydantic: Conceptos de Modelos (Models)](https://docs.pydantic.dev/latest/concepts/models/)
