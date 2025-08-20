
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
    additional_claims = {'username': user.username, 'name': user.name}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify(user.to_dict()), 200
