import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123testando'
    PERMANENT_SESSION_LIFETIME = 86400
    JWT_SECRET_KEY = 'chave_super_secreta'
    
#   Configuração da sessão
    SESSION_TYPE = 'filesystem'  
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = './flask_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_REFRESH_EACH_REQUEST = False  # Evita recriação da sessão automaticamente# Configuração de sessão
    