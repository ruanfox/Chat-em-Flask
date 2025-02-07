import os
from flask import Flask
from config import Config
from database import db  # Importa a instância central

def create_app():
    app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
    app.config.from_object(Config)

    # Inicializa o banco de dados
    db.init_app(app)

    # Importa os models dentro do contexto da aplicação
    with app.app_context():
        from models.user import User
        from models.room import Room
        from models.message import Message
        db.create_all()

    # Configure as rotas
    from controllers.user_controller import UserController
    app.add_url_rule('/', 'index', UserController.index)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)