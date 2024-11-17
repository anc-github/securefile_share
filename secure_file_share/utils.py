from itsdangerous import URLSafeSerializer
from flask_mail import Message
from app import mail
import os


def generate_secure_link(file_id, user_id):
    serializer = URLSafeSerializer(os.getenv('SECRET_KEY', 'mysecret'))
    return serializer.dumps({'file_id': file_id, 'user_id': user_id})


def verify_secure_link(token):
    serializer = URLSafeSerializer(os.getenv('SECRET_KEY', 'mysecret'))
    try:
        return serializer.loads(token)
    except Exception:
        return None


def send_verification_email(email, token):
    msg = Message('Verify Your Email', recipients=[email])
    msg.body = f"Click the link to verify your email: {token}"
    mail.send(msg)
