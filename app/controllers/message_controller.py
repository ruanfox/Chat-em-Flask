from flask import request, session
from datetime import datetime
from models.message import Message
from database import db
from controllers.auth_controller import AuthController

class MessageController:
    @staticmethod
    def send_message():
        user = AuthController.get_current_user()
        if not user:
            return {"error": "Não autorizado"}, 401

        data = request.form
        new_message = Message(
            conteudo=data['conteudo'],
            usuario_id=user.id,  # Usa o ID do usuário logado
            sala_id=data['sala_id'],
            data_envio=datetime.utcnow()
        )
        
        try:
            db.session.add(new_message)
            db.session.commit()
            return {
                "message": "Mensagem enviada",
                "data": {
                    "conteudo": new_message.conteudo,
                    "sala_id": new_message.sala_id,
                    "autor": user.nickname
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def get_messages(room_id):
        messages = Message.query.filter_by(sala_id=room_id).all()
        return {"messages": [{
            "content": m.conteudo,
            "author": m.user.nickname,
            "timestamp": m.data_envio.isoformat()
        } for m in messages]}