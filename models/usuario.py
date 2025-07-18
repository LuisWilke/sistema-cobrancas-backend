from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'a_usuarios'
    __table_args__ = {'schema': 'm2'}
    
    # Campos baseados na estrutura da tabela m2.a_usuarios
    gid = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    gid_empresa = db.Column(db.Integer, db.ForeignKey('m2.a_empresa.gid'), nullable=False)
    cnpj_empresa = db.Column(db.String(18), nullable=True)  # CNPJ formatado
    cpf_usuario = db.Column(db.String(14), nullable=True)   # CPF formatado
    email = db.Column(db.String(255), unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    celular = db.Column(db.String(20), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    senha = db.Column(db.String(255), nullable=False)  # Hash da senha
    
    # Relacionamento com a empresa
    empresa = db.relationship('Empresa', backref='usuarios', lazy=True)
    
    def __init__(self, email, nome, senha, gid_empresa, cpf_usuario=None, celular=None, data_nascimento=None, cnpj_empresa=None):
        self.email = email
        self.nome = nome
        self.gid_empresa = gid_empresa
        self.cpf_usuario = cpf_usuario
        self.celular = celular
        self.data_nascimento = data_nascimento
        self.cnpj_empresa = cnpj_empresa
        self.set_senha(senha)
    
    def set_senha(self, senha):
        """Gera hash da senha usando bcrypt"""
        self.senha = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return check_password_hash(self.senha, senha)
    
    def to_dict(self):
        """Converte o objeto para dicionário (para JSON)"""
        return {
            'id': self.gid,
            'email': self.email,
            'nome': self.nome,
            'cpf_usuario': self.cpf_usuario,
            'celular': self.celular,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'gid_empresa': self.gid_empresa,
            'cnpj_empresa': self.cnpj_empresa,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Usuario {self.email}>'


class Empresa(db.Model):
    __tablename__ = 'a_empresa'
    __table_args__ = {'schema': 'm2'}
    
    # Campos baseados na estrutura da tabela m2.a_empresa
    gid = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cnpj_empresa = db.Column(db.String(18), unique=True, nullable=False)
    nome_empresa = db.Column(db.String(255), nullable=False)
    razao_social = db.Column(db.String(255), nullable=True)
    obs = db.Column(db.Text, nullable=True)
    
    def __init__(self, cnpj_empresa, nome_empresa, razao_social=None, obs=None):
        self.cnpj_empresa = cnpj_empresa
        self.nome_empresa = nome_empresa
        self.razao_social = razao_social
        self.obs = obs
    
    def to_dict(self):
        """Converte o objeto para dicionário (para JSON)"""
        return {
            'id': self.gid,
            'cnpj_empresa': self.cnpj_empresa,
            'nome_empresa': self.nome_empresa,
            'razao_social': self.razao_social,
            'obs': self.obs,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Empresa {self.nome_empresa}>'

