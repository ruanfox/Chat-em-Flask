from flask import Blueprint
from controllers.auth_controller import AuthController
from controllers.room_controller import RoomController
from controllers.message_controller import MessageController

api_bp = Blueprint('api', __name__, url_prefix='/api')

# --- Autenticação ---
api_bp.route('/register', methods=['POST'])(AuthController.register)
api_bp.route('/login', methods=['POST'])(AuthController.login)
api_bp.route('/logout', methods=['POST'])(AuthController.logout)

# --- Salas ---
api_bp.route('/rooms', methods=['GET'])(RoomController.list_rooms)      # Listar salas
api_bp.route('/rooms', methods=['POST'])(RoomController.create_room)   # Criar sala
api_bp.route('/rooms/<int:room_id>', methods=['DELETE'])(RoomController.delete_room)  # Excluir sala

# --- Mensagens ---
api_bp.route('/messages/<int:room_id>', methods=['GET'])(MessageController.get_messages)  # Histórico

# --- informação do usuário ---
api_bp.route('/user_session', methods=['GET'])(AuthController.get_user_session)