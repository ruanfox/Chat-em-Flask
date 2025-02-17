from flask import request, session  # Importa request para capturar os dados da requisição e session para gerenciar a sessão do usuário
from werkzeug.security import generate_password_hash, check_password_hash  # Importa funções para criptografar e verificar senhas
from models.user import User  # Importa o modelo de usuário para interagir com o banco de dados
from database import db # Importa a instância do banco de dados
from functools import wraps

class AuthController:
    @staticmethod
    def register():
        """
        Registra um novo usuário no sistema.
        """
        data = request.form  # Obtém os dados enviados na requisição (método POST)
        
        # Verifica se o email já está cadastrado
        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email já cadastrado"}, 400  # Retorna erro se o email já existir no banco
            
        # Criptografa a senha antes de salvar no banco
        hashed_password = generate_password_hash(data['password'])
        
        # Cria um novo objeto User com os dados fornecidos
        new_user = User(
            nickname=data['nickname'],
            email=data['email'],
            password=hashed_password
        )
        
        try:
            # Adiciona o usuário ao banco de dados e confirma a transação
            db.session.add(new_user)
            db.session.commit()
            
            # Salva o ID do usuário na sessão para mantê-lo autenticado
            session['user_id'] = new_user.id
            
            return {"message": "Usuário criado com sucesso"}, 201  # Retorna mensagem de sucesso e status 201 (Created)
        except Exception as e:
            db.session.rollback()  # Em caso de erro, desfaz a transação no banco
            return {"error": str(e)}, 500  # Retorna erro interno do servidor

    @staticmethod
    def login():
        """
        Realiza o login de um usuário autenticando suas credenciais.
        """
        data = request.form  # Obtém os dados enviados na requisição (método POST)
        
        # Busca o usuário pelo email no banco de dados
        user = User.query.filter_by(email=data['email']).first()
        
        # Verifica se o usuário existe e se a senha está correta
        if not user or not check_password_hash(user.password, data['password']):
            return {"error": "Credenciais inválidas"}, 401  # Retorna erro se o login falhar
            
        # Armazena o ID do usuário na sessão para manter a autenticação
        session.permanent = True  # Mantém a sessão ativa
        session['user_id'] = user.id
        session['_fresh'] = True  # Sessão fresca

        return {"message": "Login bem-sucedido"}, 200  # Retorna mensagem de sucesso e status 200 (OK)

    @staticmethod
    def get_current_user():
        """Retorna o usuário logado ou None"""
        from models.user import User  # Import local para evitar circular
        user_id = session.get('user_id')
        return User.query.get(user_id) if user_id else None

    @staticmethod
    def auth_required(f):
        """Decorator para rotas que requerem autenticação"""
        @wraps(f)
        def decorated(*args, **kwargs):
            if not AuthController.get_current_user():
                return {"error": "Não autorizado"}, 401
            return f(*args, **kwargs)
        return decorated
    
    @staticmethod
    def logout():
        """
        Realiza o logout do usuário removendo a sessão.
        """
        session.clear()  # Remove o ID do usuário da sessão
        session.permanent = False
        
        return {"message": "Logout realizado"}, 200  # Retorna mensagem de sucesso e status 200 (OK)
