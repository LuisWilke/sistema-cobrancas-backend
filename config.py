import os
from datetime import timedelta

class Config:
    # Configuração do banco de dados PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/sistema_cobrancas"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta_muito_segura_aqui")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)