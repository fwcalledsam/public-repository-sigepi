from flask import Flask
import os

# --------------------
from config import Config

# --------------------
from models import db
from routes import api

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Configuración para producción
app.config["UPLOAD_FOLDER"] = os.getenv(
    "UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads")
)
app.register_blueprint(api, url_prefix="/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# from flask import Flask
# import os

# # --------------------
# from config import Config

# # --------------------
# from models import db
# from routes import api

# app = Flask(__name__)
# app.config.from_object(Config)
# db.init_app(app)

# app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
# app.register_blueprint(api, url_prefix="/")

# if __name__ == "__main__":
#     app.run(debug=True)
