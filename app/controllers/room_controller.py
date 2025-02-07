from flask import request, session
from models.room import Room
from models.message import Message
from models.user import User

# Minha classe crontroladora de salas
class RoomControler:
    @staticmethod
    def create_room():
        # se ele não encontrar o usuário, ele vai criar um novo
        if 'user_id' in session:
            return {"erro": "Não"}