from flask import Blueprint, request, jsonify
from models.usuario import Usuario
from database import db
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and bcrypt.verify(senha, usuario.senha):
        token = create_access_token(identity=usuario.gid)
        return jsonify({'token': token, 'nome': usuario.nome})
    
    return jsonify({'erro': 'Credenciais inválidas'}), 401
