from datetime import datetime
from flask import Blueprint, Flask, request, jsonify
from models.empresa import Empresa
from models.usuario import Usuario
from database import db
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

def validar_email(email):
    """Valida formato do email"""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def validar_senha(senha):
    """Valida se a senha tem pelo menos 6 caracteres"""
    return len(senha) >= 6

@auth_bp.route('/register', methods=['POST'])
def registro():
    try:
        dados = request.json
        
        # Validar dados obrigatórios
        email = dados.get('email', '').strip().lower()
        senha = dados.get('senha', '')
        nome = dados.get('nome', '').strip()
        cpf_usuario = dados.get('cpf_usuario', '').strip()
        celular = dados.get('celular', '').strip()
        data_nascimento = dados.get('data_nascimento')
        gid_empresa = dados.get('gid_empresa')
        cnpj_empresa = dados.get('cnpj_empresa', '').strip()
        
        if not email or not senha or not nome:
            return jsonify({'erro': 'Email, senha e nome são obrigatórios'}), 400
        
        if not gid_empresa:
            return jsonify({'erro': 'Empresa é obrigatória'}), 400
        
        # Validar formato do email
        if not validar_email(email):
            return jsonify({'erro': 'Formato de email inválido'}), 400
        
        # Validar senha
        if not validar_senha(senha):
            return jsonify({'erro': 'A senha deve ter pelo menos 6 caracteres'}), 400
        
        # Verificar se o usuário já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return jsonify({'erro': 'Email já cadastrado'}), 409
        
        # Verificar se a empresa existe
        empresa = Empresa.query.get(gid_empresa)
        if not empresa:
            return jsonify({'erro': 'Empresa não encontrada'}), 404
        
        # Converter data_nascimento se fornecida
        data_nasc_obj = None
        if data_nascimento:
            try:
                data_nasc_obj = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        # Criar hash da senha
        senha_hash = bcrypt.hash(senha)
        
        # Criar novo usuário
        novo_usuario = Usuario(
            email=email,
            senha=senha_hash,
            nome=nome,
            cpf_usuario=cpf_usuario,
            celular=celular,
            data_nascimento=data_nasc_obj,
            gid_empresa=gid_empresa,
            cnpj_empresa=cnpj_empresa
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        # Gerar token de acesso
        token = create_access_token(identity=str(novo_usuario.gid))
        
        return jsonify({
            'mensagem': 'Usuário criado com sucesso',
            'token': token,
            'usuario': novo_usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        dados = request.json
        
        # Validar dados obrigatórios
        email = dados.get('email', '').strip().lower()
        senha = dados.get('senha', '')
        
        if not email or not senha:
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
        
        # Buscar usuário
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario or not bcrypt.verify(senha, usuario.senha):
            return jsonify({'erro': 'Credenciais inválidas'}), 401
        
        # Gerar token de acesso
        token = create_access_token(identity=str(usuario.gid))
        
        return jsonify({
            'mensagem': 'Login realizado com sucesso',
            'token': token,
            'usuario': {
                'id': usuario.gid,
                'nome': usuario.nome,
                'email': usuario.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    try:
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(int(usuario_id))
        
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'usuario': {
                'id': usuario.gid,
                'nome': usuario.nome,
                'email': usuario.email,
                'cpf_usuario': usuario.cpf_usuario
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@auth_bp.route('/verificar-token', methods=['GET'])
@jwt_required()
def verificar_token():
    try:
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(int(usuario_id))
        
        if not usuario:
            return jsonify({'erro': 'Token inválido'}), 401
        
        return jsonify({
            'valido': True,
            'usuario': {
                'id': usuario.gid,
                'nome': usuario.nome,
                'email': usuario.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': 'Token inválido'}), 401
