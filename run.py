#!/usr/bin/env python3
"""
Punto de entrada para desarrollo local
Ejecuta: python run.py
"""

from app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    
    # Configuración para desarrollo
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🚀 Starting TaskFlow Pro API...")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🗄️  Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')}")
    print("=" * 50)
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )
