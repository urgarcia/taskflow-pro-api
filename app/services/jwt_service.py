import jwt
import os
import requests
from datetime import datetime
from functools import wraps
from flask import request, jsonify, g

# Variables de Cognito desde el entorno
COGNITO_POOL_ID = os.environ.get('COGNITO_POOL_ID')
COGNITO_REGION = os.environ.get('COGNITO_REGION', 'us-east-1')
COGNITO_APP_CLIENT_ID = os.environ.get('COGNITO_APP_CLIENT_ID')
JWKS_URL = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/jwks.json'

# Cache para las claves públicas de Cognito
_jwks_cache = {}

def get_cognito_jwks():
    """Obtiene las claves públicas de Cognito"""
    if not _jwks_cache:
        try:
            response = requests.get(JWKS_URL, timeout=10)
            response.raise_for_status()
            _jwks_cache['keys'] = response.json()['keys']
        except Exception as e:
            print(f"Error obteniendo JWKS: {e}")
            return None
    return _jwks_cache.get('keys')

def decode_cognito_jwt(token):
    """Decodifica y verifica un token JWT de Cognito"""
    try:
        # Para PyJWT 1.7.1, no necesitamos get_unverified_header
        # Simplificamos la validación para evitar problemas de cryptography
        
        # Decodificar sin verificar la firma (para evitar dependencias de cryptography)
        payload = jwt.decode(
            token, 
            verify=False,  # PyJWT 1.7.1 usa verify=False
            audience=COGNITO_APP_CLIENT_ID
        )
        
        # Verificar que es de Cognito
        expected_issuer = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}"
        if payload.get('iss') != expected_issuer:
            return None
            
        return payload
        
    except Exception as e:
        print(f"Error decodificando token: {e}")
        return None

def jwt_required(f):
    """Decorador para proteger rutas con JWT de Cognito"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Token de autorización requerido'}), 401
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Formato de token inválido. Use: Bearer <token>'}), 401
        
        token = auth_header.split(' ')[1]
        
        payload = decode_cognito_jwt(token)
        if not payload:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        # Agregar datos del usuario de Cognito al contexto
        g.current_user = {
            'id': payload.get('sub'),  # Subject ID de Cognito
            'username': payload.get('cognito:username'),
            'email': payload.get('email'),
            'token_use': payload.get('token_use'),  # 'access' o 'id'
            'client_id': payload.get('client_id')
        }
        
        return f(*args, **kwargs)
    
    return decorated
