from flask import Blueprint, jsonify
from models.cliente import Cliente
from database import db

cliente_bp = Blueprint("cliente_bp", __name__)

@cliente_bp.route("/clientes", methods=["GET"])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])
