from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models.usuario import Usuario, Empresa
from utils.validators import validar_email, validar_senha
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['POST'])
def registro():
    try:
        dados = request.get_json()
        
        # Validar dados obrigatórios
        if not dados or not all(k in dados for k in ('nome', 'email', 'senha')):
            return jsonify({'erro': 'Nome, email e senha são obrigatórios'}), 400
        
        nome = dados.get('nome').strip()
        email = dados.get('email').strip().lower()
        senha = dados.get('senha')
        cpf_usuario = dados.get('cpf_usuario', '').strip()
        celular = dados.get('celular', '').strip()
        data_nascimento = dados.get('data_nascimento')
        gid_empresa = dados.get('gid_empresa')  # ID da empresa (obrigatório)
        cnpj_empresa = dados.get('cnpj_empresa', '').strip()
        
        # Validações
        if not validar_email(email):
            return jsonify({'erro': 'Email inválido'}), 400
        
        if not validar_senha(senha):
            return jsonify({'erro': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        if not gid_empresa:
            return jsonify({'erro': 'ID da empresa é obrigatório'}), 400
        
        # Verificar se o email já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Verificar se a empresa existe
        empresa = Empresa.query.get(gid_empresa)
        if not empresa:
            return jsonify({'erro': 'Empresa não encontrada'}), 400
        
        # Converter data_nascimento se fornecida
        data_nasc_obj = None
        if data_nascimento:
            try:
                data_nasc_obj = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Data de nascimento inválida. Use o formato YYYY-MM-DD'}), 400
        
        # Criar novo usuário
        novo_usuario = Usuario(
            email=email,
            nome=nome,
            senha=senha,
            gid_empresa=gid_empresa,
            cpf_usuario=cpf_usuario if cpf_usuario else None,
            celular=celular if celular else None,
            data_nascimento=data_nasc_obj,
            cnpj_empresa=cnpj_empresa if cnpj_empresa else None
        )
        
        # Salvar no banco
        db.session.add(novo_usuario)
        db.session.commit()
        
        # Gerar token de acesso
        token = create_access_token(identity=str(novo_usuario.gid))
        
        return jsonify({
            'mensagem': 'Usuário criado com sucesso',
            'token': token,
            'usuario': {
                'id': novo_usuario.gid,
                'nome': novo_usuario.nome,
                'email': novo_usuario.email,
                'gid_empresa': novo_usuario.gid_empresa,
                'empresa': empresa.to_dict()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        dados = request.get_json()
        
        if not dados or not all(k in dados for k in ('email', 'senha')):
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
        
        email = dados.get('email').strip().lower()
        senha = dados.get('senha')
        
        # Buscar usuário
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario or not usuario.verificar_senha(senha):
            return jsonify({'erro': 'Email ou senha incorretos'}), 401
        
        # Gerar token de acesso
        token = create_access_token(identity=str(usuario.gid))
        
        # Buscar dados da empresa
        empresa = Empresa.query.get(usuario.gid_empresa)
        
        return jsonify({
            'mensagem': 'Login realizado com sucesso',
            'token': token,
            'usuario': {
                'id': usuario.gid,
                'nome': usuario.nome,
                'email': usuario.email,
                'gid_empresa': usuario.gid_empresa,
                'empresa': empresa.to_dict() if empresa else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@auth_bp.route('/verificar-token', methods=['GET'])
@jwt_required()
def verificar_token():
    try:
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(int(usuario_id))
        
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Buscar dados da empresa
        empresa = Empresa.query.get(usuario.gid_empresa)
        
        return jsonify({
            'valido': True,
            'usuario': {
                'id': usuario.gid,
                'nome': usuario.nome,
                'email': usuario.email,
                'gid_empresa': usuario.gid_empresa,
                'empresa': empresa.to_dict() if empresa else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    try:
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(int(usuario_id))
        
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Buscar dados da empresa
        empresa = Empresa.query.get(usuario.gid_empresa)
        
        return jsonify({
            'usuario': {
                'id': usuario.gid,
                'nome': usuario.nome,
                'email': usuario.email,
                'cpf_usuario': usuario.cpf_usuario,
                'celular': usuario.celular,
                'data_nascimento': usuario.data_nascimento.isoformat() if usuario.data_nascimento else None,
                'gid_empresa': usuario.gid_empresa,
                'cnpj_empresa': usuario.cnpj_empresa,
                'created_at': usuario.created_at.isoformat() if usuario.created_at else None,
                'empresa': empresa.to_dict() if empresa else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@auth_bp.route('/empresas', methods=['GET'])
def listar_empresas():
    """Endpoint para listar empresas disponíveis para registro"""
    try:
        empresas = Empresa.query.all()
        return jsonify({
            'empresas': [empresa.to_dict() for empresa in empresas]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500