from flask import Flask
import os
from models import db
from routes import api

app = Flask(__name__)

# Configuración (usa variables de entorno en producción)
app.config.from_object("config.Config")
db.init_app(app)

# Configuración de la carpeta de uploads
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.register_blueprint(api, url_prefix="/")

# Para ejecución local
if __name__ == "__main__":
    app.run(debug=True)
