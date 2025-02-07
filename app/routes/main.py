from flask import Blueprint

# Cria o Blueprint "main_bp"
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return "Olá, Mundo!"