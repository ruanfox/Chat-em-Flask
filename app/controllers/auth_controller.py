from flask import request, session,redirect, jsonify , flash # Importa request para capturar os dados da requisição e session para gerenciar a sessão do usuário
from werkzeug.security import generate_password_hash, check_password_hash  # Importa funções para criptografar e verificar senhas
from models.user import User  # Importa o modelo de usuário para interagir com o banco de dados
from database import db # Importa a instância do banco de dados
from functools import wraps

class AuthController:
    authenticated = False 
    @staticmethod
    def register():
        if request.method == 'POST':
            data = request.form

            if not data:
                return {"error": "Nenhum dado recebido"}, 400
            
            nickname = data.get('nickname')
            email = data.get('email')
            password = data.get('password')

            if not nickname or not email or not password:
                return {"error": "Todos os campos são obrigatórios"}, 400

            if User.query.filter_by(email=email).first():
                return {"error": "Email já cadastrado"}, 400

            hashed_password = generate_password_hash(password)
            new_user = User(nickname=nickname, email=email, password=hashed_password)

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')
                    #{"message": "Usuário criado com sucesso"}, 201
            except Exception as e:
                db.session.rollback()
                return {"error": str(e)}, 500
            
    @staticmethod
    def login():
        data = request.form

        if not data:
            return jsonify({"error": "Nenhum dado recebido"}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("email ou senha invalidos")
            return redirect("/")
               #jsonify({"error": "Credenciais inválidas"}), 401

        session.permanent = True
        session['user_id'] = user.id
        session['_fresh'] = True

        print("Minha session após meu login:", session)
        AuthController.auth_required(True)

        return redirect("/chat")

    @staticmethod
    def logout():
        """
        Realiza o logout do usuário removendo a sessão.
        """
        session.clear()
        
        AuthController.auth_required(False)
        return redirect("/") 
            #jsonify({"Sucesso:": "Logout realizado com sucesso!"}), 200
    
    @staticmethod
    def auth_required(auth=None):
        if auth is not None:
            AuthController.is_authenticated = auth  # Atualiza o estado
        return AuthController.is_authenticated
    
    @staticmethod
    def get_user_session(): 
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Usuário não autenticado"}), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        return jsonify({
            "user_id": user.id,
            "nickname": user.nickname
        })
        
        