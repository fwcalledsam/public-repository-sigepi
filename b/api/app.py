from flask import Flask, jsonify
import os
from models import db
from routes import api


def create_app():
    app = Flask(__name__)

    # Configuración mejorada
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "/tmp/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload

    # Inicialización de la base de datos
    db.init_app(app)

    # Crear carpeta de uploads si no existe
    try:
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    except Exception as e:
        print(f"Error creating upload folder: {e}")

    # Registrar blueprints
    app.register_blueprint(api)

    # Manejo de errores genérico
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
