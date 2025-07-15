from database import db

class Usuario(db.Model):
    __tablename__ = 'a_tusuarios'
    __table_args__ = {'schema': 'm2'}

    gid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(100))
    cpf_usuario = db.Column(db.String(50))