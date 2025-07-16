from database import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    gid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    senha = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cpf_usuario = db.Column(db.String(14), nullable=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def to_dict(self):
        """Converte o objeto para dicionário (sem a senha)"""
        return {
            'id': self.gid,
            'email': self.email,
            'nome': self.nome,
            'cpf_usuario': self.cpf_usuario,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }