from flask import request, session
from datetime import datetime
from models.message import Message
from database import db

class MessageController:
    @staticmethod
    def get_messages(room_id):
        """Retorna o histórico de mensagens (HTTP GET)"""
        messages = Message.query.filter_by(sala_id=room_id).all()
        return {"messages": [{
            "content": m.conteudo,
            "author": m.user.nickname,
            "timestamp": m.data_envio.isoformat()
        } for m in messages]}