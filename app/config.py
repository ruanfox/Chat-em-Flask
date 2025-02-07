import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRETE_KEY = os.urandom(24)