import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123testando'
    SESSION_COOKIE_NAME = 'chat_session'
    PERMANENT_SESSION_LIFETIME = 86400