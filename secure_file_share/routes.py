from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, File, bcrypt
from utils import generate_secure_link, verify_secure_link, send_verification_email
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
jwt = JWTManager(app)

# 1. Client User Signup API
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data['email']
    password = data['password']
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, password=hashed_pw, user_type='client')
    db.session.add(new_user)
    db.session.commit()

    token = generate_secure_link(new_user.id, 'email_verification')
    send_verification_email(email, token)
    return jsonify(message="User registered. Please verify your email.")

# 2. User Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'id': user.id, 'type': user.user_type})
        return jsonify(access_token=access_token)

    return jsonify(message="Invalid credentials"), 401

# 3. Ops User Upload File API
@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    user = get_jwt_identity()
    if user['type'] != 'ops':
        return jsonify(message="Unauthorized"), 403

    file = request.files['file']
    if file.filename.split('.')[-1] not in ['pptx', 'docx', 'xlsx']:
        return jsonify(message="Invalid file type"), 400

    file.save(os.path.join('uploads', file.filename))
    new_file = File(filename=file.filename, uploaded_by=user['id'])
    db.session.add(new_file)
    db.session.commit()

    return jsonify(message="File uploaded successfully.")

# 4. Client User Download File API
@app.route('/download/<int:file_id>', methods=['GET'])
@jwt_required()
def download_file(file_id):
    user = get_jwt_identity()
    if user['type'] != 'client':
        return jsonify(message="Unauthorized"), 403

    secure_link = generate_secure_link(file_id, user['id'])
    return jsonify(download_link=secure_link, message="success")
