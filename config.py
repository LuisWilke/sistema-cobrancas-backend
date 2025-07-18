import os
from datetime import timedelta

class Config:
    # Configuração do banco de dados PostgreSQL
    # Adaptado para usar o banco 'reguacobranca' com esquema 'm2'
    DATABASE_URL = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/reguacobranca'
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração para usar o esquema 'm2' por padrão
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'options': '-csearch_path=m2,public'  # Define m2 como esquema padrão
        }
    }
    
    # Configurações JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'sua_chave_secreta_muito_segura_aqui'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_ALGORITHM = 'HS256'
    
    # Configurações da aplicação
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configurações CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']