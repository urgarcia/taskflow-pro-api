
from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)
user_service = UserService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'msg': 'Username and password required'}), 400
    user = user_service.register_user(data['username'], data['password'], data.get('name', ''))
    if not user:
        return jsonify({'msg': 'Username already exists'}), 409
    return jsonify(user.to_dict()), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'msg': 'Username and password required'}), 400
    user = user_service.authenticate(data['username'], data['password'])
    if not user:
        return jsonify({'msg': 'Invalid credentials'}), 401
    
    # Autenticación básica sin JWT por ahora
    return jsonify({'msg': 'Login successful', 'user_id': user.id}), 200

@auth_bp.route('/profile', methods=['GET'])
def profile():
    # TODO: Implementar autenticación simple
    return jsonify({'msg': 'Profile endpoint - authentication needed'}), 401
