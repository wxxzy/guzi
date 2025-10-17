# guzi_backend/routes/auth.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db
from ..models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册接口。"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"code": 40001, "message": "Missing username, email or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"code": 40002, "message": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"code": 40003, "message": "Email already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"code": 0, "message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录接口。"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"code": 40001, "message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"code": 0, "message": "Login successful", "data": {"access_token": access_token}}), 200
    else:
        return jsonify({"code": 40101, "message": "Invalid credentials"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """受保护的测试接口。"""
    current_user_id = get_jwt_identity()
    return jsonify({"code": 0, "message": "Access granted", "data": {"user_id": current_user_id}}), 200
