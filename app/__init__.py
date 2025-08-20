from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configuración directa sin importar config.py
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'thiSsdn34_?1nds_!=2QWex')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "mysql+pymysql://root:root@localhost:3306/dish_db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # CORS para desarrollo - permite cualquier origen de localhost o cualquier origen
    CORS(app, origins="*")

    from extensions import db
    db.init_app(app)
    migrate = Migrate(app, db)

    from .routes.tasks_routes import tasks_bp
    from .routes.auth_routes import auth_bp
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)

    # Ruta de prueba fuera de blueprint
    @app.route('/', methods=['GET'])
    def health_check():
        return {'status': 'ok', 'message': 'API funcionando correctamente'}, 200

    return app