from flask import request, session, redirect
from models.room import Room
from models.message import Message
from database import db
from controllers.auth_controller import AuthController

class RoomController:
    @staticmethod
    def create_room():
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Não autorizado"}, 401

        data = request.form
        new_room = Room(
            nome=data['nome'],
            criado_por=user_id  # Usa o ID do usuário logado
        )
        db.session.add(new_room)
        db.session.commit()
        db.session.rollback()
        
        return redirect("/chat")
        

    @staticmethod
    def delete_room(room_id):
        user_id = session.get('user_id')  # Obtém o ID do usuário logado
        if not user_id:
            return {"error": "Não autorizado"}, 401

        room = Room.query.get(room_id)
        if not room:
            return {"error": "Sala não encontrada"}, 404

        # Verifica se o usuário logado é o criador da sala
        if room.criado_por != user_id:
            return {"error": "Acesso negado: Você não é o dono desta sala"}, 403

        try:
            # Deleta mensagens associadas antes de remover a sala
            Message.query.filter_by(sala_id=room_id).delete()
            db.session.delete(room)
            db.session.commit()
            return {"message": "Sala excluída com sucesso"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def list_rooms():
        rooms = Room.query.all()
        return {"rooms": [{"id": r.id, "nome": r.nome} for r in rooms]}