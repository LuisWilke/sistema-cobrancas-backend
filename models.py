from app import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)
