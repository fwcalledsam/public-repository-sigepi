from app import app
from flask import request


def handler(req, context):
    with app.app_context():
        # Convertir el evento de Vercel a una solicitud de Flask
        path = req["path"]
        method = req["method"]
        headers = req.get("headers", {})
        body = req.get("body", "")

        # Crear entorno WSGI
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "QUERY_STRING": "",
            "SERVER_NAME": "0.0.0.0",
            "SERVER_PORT": "5000",
            "SERVER_PROTOCOL": "HTTP/1.1",
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": body,
            "wsgi.errors": None,
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
            **{"HTTP_" + k.upper().replace("-", "_"): v for k, v in headers.items()},
        }

        # Ejecutar la aplicación
        response = app(environ, lambda status, headers: None)

        # Convertir la respuesta de Flask al formato que espera Vercel
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response.data.decode("utf-8") if response.data else "",
        }
