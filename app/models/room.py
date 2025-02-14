from database import db  # Importe do arquivo central

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    criado_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship corrigida
    creator = db.relationship('User', backref='rooms')

    def __repr__(self):
        return f'<Room {self.nome}>'