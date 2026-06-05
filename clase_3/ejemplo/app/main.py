# ============================================================
# Punto de entrada de la aplicación.
# Este es el archivo principal que FastAPI ejecuta.
# Aquí se crea la app y se registran las rutas.
# ============================================================

# FastAPI es el framework que usamos para crear la API.
from fastapi import FastAPI

# Importamos el objeto settings para usar el nombre de la app.
from app.core.config import settings

# Importamos el router de items (las rutas que definimos en routes/).
# Lo renombramos como "item_router" para mayor claridad.
from app.routes.item_routes import router as item_router


# Creamos la instancia de FastAPI.
# "title" es el nombre que aparece en la documentación de Swagger UI.
app = FastAPI(title=settings.app_name)


# Ruta raíz (GET /) para verificar que la API está funcionando.
# Es como un "ping" o "health check".
@app.get("/")
def health_check():
    """
    Devuelve un JSON simple para confirmar que el servidor está activo.
    Útil para probar rápidamente si todo arrancó bien.
    """
    return {"status": "ok", "service": settings.app_name}


# Registramos el router de items en la aplicación.
# Sin esta línea, las rutas de /items/ NO aparecen en Swagger UI.
# include_router conecta todas las rutas definidas en item_routes.py.
app.include_router(item_router)
