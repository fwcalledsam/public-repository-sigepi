from app import app
from flask import Response
import json


def handler(event, _):
    with app.app_context():
        # Convertir el evento de Vercel a una solicitud WSGI
        method = event["httpMethod"]
        path = event["path"]
        headers = event.get("headers", {})
        body = event.get("body", "{}")

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

        # Ejecutar la aplicación Flask
        response = app(environ, lambda status, headers: None)

        # Convertir la respuesta al formato que espera Vercel
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response[0].decode("utf-8") if response else "",
        }
