from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic BaseSettings.
    Las variables se cargan desde el archivo .env
    """
    PROJECT_NAME: str = "api_abb"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Agregar más configuraciones según sea necesario
    # DATABASE_URL: str
    # SECRET_KEY: str
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
