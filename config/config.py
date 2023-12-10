from dotenv import load_dotenv
import os

load_dotenv()

class Secrets:
    # La variable SECRET_KEY sigue siendo estática
    EMAIL_ADMIN = os.getenv("EMAIL_ADMIN")

    # Configura el atributo DB_CONFIG para usar la variable de entorno
    DB_CONFIG = os.getenv("DB_CONFIG")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = 1800 # 30 minutos

class Static:
    
    # Configuración de Swagger UI
    SWAGGER_URL = '/api/v1/docs'  # URL para acceder a la interfaz Swagger UI
    API_URL = '/api/v1/spec'  # Ruta del endpoint para la especificación Swagger

    CONFIG_SWAGGER = {
        'app_name': "Trailer Movie API v1"
    }