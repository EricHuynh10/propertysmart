import os

db_config = {
    'type': os.getenv('DB_TYPE', 'postgresql'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'admin'),
    'schema': os.getenv('DB_SCHEMA', 'propertySmart'),
}

cors_allowed_origins = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost;http://localhost:8081;http://localhost:3000;https://blue-moss-0ff9cb900.4.azurestaticapps.net'
)
cors_allowed_origins_list = cors_allowed_origins.split(';')