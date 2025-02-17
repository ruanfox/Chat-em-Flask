import os
from flask import Flask
from config import Config
from database import db  # Importa a instância central
from routes.api_routes import api_bp

def create_app():
    app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
    app.config.from_object(Config)

    # Configure session cookies
    app.config.update(
        SESSION_COOKIE_SECURE=False,    # True em produção
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_REFRESH_EACH_REQUEST=True
    )
    
    # Inicializa o banco de dados
    db.init_app(app)

    # Configura as rotas
    app.register_blueprint(api_bp)

    # Importa os models dentro do contexto da aplicação
    with app.app_context():
        from models.user import User
        from models.room import Room   
        from models.message import Message
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)