from flask import request, jsonify, g
from functools import wraps


def cognito_jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'msg': 'Missing or invalid Authorization header'}), 401
        
        # Por ahora, simplemente verificamos que el token existe
        # TODO: Implementar validación JWT real más tarde
        token = auth.split(' ')[1]
        if not token or len(token) < 10:
            return jsonify({'msg': 'Invalid token'}), 401
            
        # Mock user data - reemplazar con validación real
        g.cognito_user = {'sub': 'test-user', 'email': 'test@example.com'}
        return f(*args, **kwargs)
    return decorated
