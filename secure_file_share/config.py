import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret') 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///secure_file_share.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecret')  
    MAIL_SERVER = 'smtp.gmail.com'  
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')  
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
