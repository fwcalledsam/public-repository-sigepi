from app import app
from flask import request, Response
import json


def handler(event, context):
    with app.app_context():
        # Convertir el evento de Vercel a una solicitud de Flask
        path = event["path"]
        method = event["httpMethod"]
        headers = event.get("headers", {})
        body = event.get("body", "{}") if event.get("body") else "{}"

        # Crear entorno WSGI
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "QUERY_STRING": "",
            "SERVER_NAME": "0.0.0.0",
            "SERVER_PORT": "5000",
            "SERVER_PROTOCOL": "HTTP/1.1",
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "https",
            "wsgi.input": body,
            "wsgi.errors": None,
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
            **{"HTTP_" + k.upper().replace("-", "_"): v for k, v in headers.items()},
        }

        # Ejecutar la aplicación
        response = Response.from_app(app, environ)

        # Convertir la respuesta al formato que espera Vercel
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response.get_data(as_text=True),
        }
