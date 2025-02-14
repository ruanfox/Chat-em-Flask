from flask import Blueprint
from controllers.auth_controller import AuthController
from controllers.room_controller import RoomController
from controllers.message_controller import MessageController

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Autenticação
api_bp.route('/register', methods=['POST'])(AuthController.register)
api_bp.route('/login', methods=['POST'])(AuthController.login)
api_bp.route('/logout', methods=['POST'])(AuthController.logout)

# Salas (Protegidas)
api_bp.route('/rooms', methods=['GET'])(RoomController.list_rooms)
api_bp.route('/rooms', methods=['POST'])(AuthController.auth_required(RoomController.create_room))
api_bp.route('/rooms/<int:room_id>', methods=['DELETE'])(AuthController.auth_required(RoomController.delete_room))

# Mensagens (Protegidas)
api_bp.route('/messages/<int:room_id>', methods=['GET'])(MessageController.get_messages)
api_bp.route('/messages', methods=['POST'])(AuthController.auth_required(MessageController.send_message))