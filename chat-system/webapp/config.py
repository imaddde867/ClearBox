import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'postgresql://admin:{os.environ.get("DB_PASSWORD")}@localhost/chatdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
