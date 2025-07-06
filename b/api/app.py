from flask import Flask
import os
from models import db
from routes import api


def create_app():
    app = Flask(__name__)

    # Configuración
    app.config.from_object("config.Config")
    db.init_app(app)

    # Configuración de la carpeta de uploads
    app.config["UPLOAD_FOLDER"] = "/tmp/uploads"  # Usar tmp en Vercel
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    app.register_blueprint(api, url_prefix="/")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
