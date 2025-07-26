from database import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'a_usuarios'  # Nome correto da tabela

    gid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    senha = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cpf_usuario = db.Column(db.String(14), nullable=True)
    celular = db.Column(db.String(15), nullable=True)  
    data_nascimento = db.Column(db.Date, nullable=True)  
    gid_empresa = db.Column(db.Integer, db.ForeignKey('a_empresa.gid'), nullable=False)
    cnpj_empresa = db.Column(db.String(18), nullable=True)  
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relacionamento com empresa (removido temporariamente)
    # empresa = db.relationship('Empresa', backref='usuarios')

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def to_dict(self):
        """Converte o objeto para dicionário (sem a senha)"""
        return {
            'id': self.gid,
            'email': self.email,
            'nome': self.nome,
            'cpf_usuario': self.cpf_usuario,
            'celular': self.celular,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'gid_empresa': self.gid_empresa,
            'cnpj_empresa': self.cnpj_empresa,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }