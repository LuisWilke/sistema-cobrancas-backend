#!/usr/bin/env python3
from app import create_app
from database import db
from models.usuario import Usuario
from models.empresa import Empresa
from models.cliente import Cliente

def init_database():
    """Inicializa o banco de dados criando todas as tabelas"""
    app = create_app()
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Banco de dados inicializado com sucesso!")
            print("✅ Tabelas criadas:")
            
            # Listar tabelas criadas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            for table in tables:
                print(f"   - {table}")
                
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {e}")
            return False
    
    return True

if __name__ == "__main__":
    init_database()


