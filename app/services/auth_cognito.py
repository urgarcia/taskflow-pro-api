import os
import requests
import jwt
from flask import request, jsonify, g
from functools import wraps
import threading

COGNITO_POOL_ID = os.environ.get('COGNITO_POOL_ID')
COGNITO_REGION = os.environ.get('COGNITO_REGION', 'us-east-1')
COGNITO_APP_CLIENT_ID = os.environ.get('COGNITO_APP_CLIENT_ID')
JWKS_URL = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/jwks.json'

_jwks_cache = {}
_jwks_lock = threading.Lock()

def get_jwks():
    with _jwks_lock:
        if not _jwks_cache:
            _jwks_cache['keys'] = requests.get(JWKS_URL).json()['keys']
        return _jwks_cache['keys']

def verify_cognito_jwt(token):
    header = jwt.get_unverified_header(token)
    keys = get_jwks()
    key = next((k for k in keys if k['kid'] == header['kid']), None)
    if not key:
        raise Exception('Public key not found in JWKS')
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
    payload = jwt.decode(
        token,
        public_key,
        algorithms=['RS256'],
        audience=COGNITO_APP_CLIENT_ID
    )
    return payload

def cognito_jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'msg': 'Missing or invalid Authorization header'}), 401
        token = auth.split(' ')[1]
        try:
            payload = verify_cognito_jwt(token)
            g.cognito_user = payload
        except Exception as e:
            return jsonify({'msg': 'Invalid token', 'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated
