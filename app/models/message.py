from database import db  # Importe do arquivo central
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    conteudo = db.Column(db.String(500), nullable=False)
    usuario_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    sala_id = db.Column(db.String(50), db.ForeignKey('rooms.id'), nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime)

    # Relationships
    user = db.relationship('User', backref='messages')
    room = db.relationship('Room', backref='messages')

    def __repr__(self):
        return f'<Message {self.conteudo[:20]}>'  # Mostra apenas a primeira parte do conteúdo do mensagem