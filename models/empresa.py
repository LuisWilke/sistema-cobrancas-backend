from database import db
from datetime import datetime

class Empresa(db.Model):
    __tablename__ = 'a_empresa'

    gid = db.Column(db.Integer, primary_key=True)
    cnpj_empresa = db.Column(db.String(18), unique=True, nullable=False)
    nome_empresa = db.Column(db.String(255), nullable=False)
    razao_social = db.Column(db.String(255), nullable=True)
    obs = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Empresa {self.nome_empresa}>'

    def to_dict(self):
        return {
            'id': self.gid,
            'cnpj_empresa': self.cnpj_empresa,
            'nome_empresa': self.nome_empresa,
            'razao_social': self.razao_social,
            'obs': self.obs,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }