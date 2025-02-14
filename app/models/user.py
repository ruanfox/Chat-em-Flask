from database import db  # Importe do arquivo central

class User(db.Model):
    __tablename__ = 'users'  # Nome da tabela em plural
    
    id = db.Column(db.Integer,primary_key=True, nullable=False,autoincrement=True)
    nickname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.nickname}>'