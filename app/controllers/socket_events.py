from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room
from database import db
from models.message import Message
from datetime import datetime

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on("send_message")
def handle_send_message(data):
    """Recebe uma mensagem e a envia para os clientes na sala."""
    
    room_id = data.get("room_id")
    message_content = data.get("message")
    author = data.get("author")
    user_id = data.get("user_id")

    if not room_id or not message_content or not user_id:
        print("Dados incompletos:", data)
        return  

    try:
        # Cria uma nova mensagem no banco de dados
        new_message = Message(
            conteudo=message_content,  
            usuario_id=user_id,        
            sala_id=room_id,           
            data_envio=datetime.utcnow()  
        )
        db.session.add(new_message)
        db.session.commit()

        # Envia a mensagem para todos na sala
        emit("receive_message", {
            "room_id": room_id,
            "message": message_content,
            "author": author,
            "timestamp": new_message.data_envio.isoformat()  # Usa o timestamp salvo
        }, room=room_id)

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar mensagem: {str(e)}")
        emit("error", {"message": "Erro ao enviar mensagem"}, room=room_id)

@socketio.on("join_room")
def handle_join_room(data):
    """Usuário entra em uma sala."""
    room_id = data.get("room_id")
    if room_id:
        join_room(room_id)  # Associa o cliente à sala
        emit("system_message", {"message": f"Usuário entrou na sala {room_id}"}, room=room_id)

@socketio.on("leave_room")
def handle_leave_room(data):
    """Usuário sai da sala."""
    room_id = data.get("room_id")
    if room_id:
        leave_room(room_id)  # Remove o cliente da sala
        emit("system_message", {"message": f"Usuário saiu da sala {room_id}"}, room=room_id)