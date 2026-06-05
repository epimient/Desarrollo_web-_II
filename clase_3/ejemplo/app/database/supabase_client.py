# ============================================================
# Cliente de conexión con Supabase.
# Este archivo crea la conexión que usaremos desde los servicios
# para hacer operaciones en la base de datos (insertar, leer, etc).
# ============================================================

# Client es el tipo del cliente de Supabase.
# create_client es la función que crea la conexión.
from supabase import Client, create_client

# Importamos el objeto settings que ya tiene las credenciales
# leídas desde el archivo .env.
from app.core.config import settings


# Creamos el cliente de Supabase usando la URL y la clave.
# Este objeto "supabase" es el que usaremos en los servicios
# para hacer consultas a la base de datos.
#
# Flujo:
#   config.py lee las credenciales del .env
#   → supabase_client.py crea la conexión
#   → item_service.py usa esa conexión para operar la tabla
supabase: Client = create_client(
    settings.supabase_url,
    settings.supabase_key,
)
