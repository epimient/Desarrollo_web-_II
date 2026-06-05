# ============================================================
# Configuración del proyecto.
# Este archivo lee las variables de entorno desde el archivo .env
# para que las credenciales no queden escritas en el código.
# ============================================================

# BaseSettings es una clase especial de Pydantic que lee variables
# de entorno automáticamente. SettingsConfigDict permite configurar
# de dónde leer esas variables.
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Modelo de configuración del proyecto.
    Cada atributo corresponde a una variable de entorno.
    Por ejemplo: supabase_url busca la variable SUPABASE_URL en .env.
    """

    # URL del proyecto en Supabase (ejemplo: https://xxxxx.supabase.co).
    supabase_url: str

    # Clave de API de Supabase (la encuentras en la configuración del proyecto).
    supabase_key: str

    # Nombre de la aplicación. Si no se define en .env, usa este valor por defecto.
    app_name: str = "API Clase 3"

    # Configuración de dónde leer las variables:
    # - env_file: busca un archivo llamado .env en la raíz del proyecto.
    # - env_file_encoding: usa codificación UTF-8 para leer el archivo.
    # - extra="ignore": si hay variables extra en .env que no están aquí, las ignora.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Creamos una instancia única de Settings.
# Al hacer esto, Python lee el archivo .env y carga los valores.
# Desde cualquier otro archivo podemos hacer:
#   from app.core.config import settings
#   settings.supabase_url
settings = Settings()
