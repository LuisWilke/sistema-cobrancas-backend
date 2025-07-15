from flask import Flask
from flask_cors import CORS
from config import Config
from database import db
from routes.auth_routes import auth_bp
from routes.cliente_routes import cliente_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    # Registro de Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # apenas local
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)