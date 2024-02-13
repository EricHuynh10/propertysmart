import os

db_config = {
    'type': os.getenv('DB_TYPE', 'postgresql'),
    'host': os.getenv('DB_HOST', 'localhost:5433'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'admin'),
    'schema': os.getenv('DB_SCHEMA', 'realestateDB'),
}

cors_allowed_origins = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost;http://localhost:8081;http://localhost:3000;http://propertysmart-frontend'
)
cors_allowed_origins_list = cors_allowed_origins.split(';')
