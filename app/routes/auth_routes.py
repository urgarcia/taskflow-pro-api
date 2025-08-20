
from flask import Blueprint, request, jsonify, g
from app.services.user_service import UserService
from app.services.jwt_service import jwt_required

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
    # Esta ruta ahora es solo para referencia
    # La autenticación real se hace desde el frontend con Cognito
    return jsonify({
        'msg': 'Use AWS Cognito para autenticarse. Esta ruta es solo para referencia.',
        'info': 'El frontend debe autenticarse con Cognito y enviar el token en Authorization header'
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required
def profile():
    # Los datos del usuario vienen del token JWT de Cognito
    return jsonify({
        'msg': 'Profile data from Cognito JWT',
        'user': g.current_user
    }), 200
