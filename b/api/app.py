from flask import Flask
from models import db
from routes import api
import os


def create_app():
    app = Flask(__name__)

    # Configuración esencial
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Inicialización de la base de datos
    db.init_app(app)

    # Configuración de uploads
    app.config["UPLOAD_FOLDER"] = "/tmp/uploads"
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Registrar blueprints
    app.register_blueprint(api)

    # Ruta de health check
    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
