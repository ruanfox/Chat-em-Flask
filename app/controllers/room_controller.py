from flask import request, session
from models.room import Room
from models.message import Message
from database import db
from controllers.auth_controller import AuthController

class RoomController:
    @staticmethod
    def create_room():
        user = AuthController.get_current_user()
        if not user:
            return {"error": "Não autorizado"}, 401

        data = request.form
        new_room = Room(
            nome=data['nome'],
            criado_por=user.id  # Usa o ID do usuário logado
        )
        
        try:
            db.session.add(new_room)
            db.session.commit()
            return {
                "message": "Sala criada",
                "room_id": new_room.id,
                "nome": new_room.nome
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete_room(room_id):
        user = AuthController.get_current_user()
        if not user:
            return {"error": "Não autorizado"}, 401

        room = Room.query.get_or_404(room_id)
        
        if room.criado_por != user.id:
            return {"error": "Acesso negado"}, 403
            
        try:
            Message.query.filter_by(sala_id=room_id).delete()
            db.session.delete(room)
            db.session.commit()
            return {"message": "Sala excluída"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete_room(room_id):
        current_user = AuthController.get_current_user()
        
        if not current_user:
            return {"erro": "Não autorizado"}, 401
        
        room = Room.query.get(room_id)
        
        if not room:
            return {"error": "Sala Não encontrada"}, 404
        
        if room.criado_por != current_user.id:  # Garantir que ambos são int
            return {"error": "Acesso negado: Você não é o dono desta sala"}, 403
        
        try:
            # Deleta mensagens associadas primeiro
            Message.query.filter_by(sala_id=room_id).delete()
            db.session.delete(room)
            db.session.commit()
            return {"message": "Sala excluída"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def list_rooms():
        rooms = Room.query.all()
        return {"rooms": [{"id": r.id, "nome": r.nome} for r in rooms]}