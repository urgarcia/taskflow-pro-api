from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    CORS(app, origins=["http://localhost:4200"])

    from extensions import db, jwt
    db.init_app(app)
    jwt.init_app(app)
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