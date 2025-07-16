from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from routes.auth_routes import auth_bp
from routes.cliente_routes import cliente_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurar CORS para permitir requisições do frontend
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Inicializar extensões
    db.init_app(app)
    jwt = JWTManager(app)

    # Registro de Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Criar tabelas se não existirem
    app.run(host='0.0.0.0', port=5000, debug=True)