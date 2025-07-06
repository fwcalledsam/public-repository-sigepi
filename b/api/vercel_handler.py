from app import app
from flask import Response, request
import json
import os


def handler(event, context):
    # Convertir el evento de Vercel a una solicitud Flask
    method = event["httpMethod"]
    path = event["path"]
    headers = event.get("headers", {})
    body = event.get("body", "{}") or "{}"
    query = event.get("queryStringParameters", {}) or {}

    # Configurar entorno WSGI
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": "&".join([f"{k}={v}" for k, v in query.items()]),
        "SERVER_NAME": "0.0.0.0",
        "SERVER_PORT": "5000",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": headers.get("x-forwarded-proto", "https"),
        "wsgi.input": body,
        "wsgi.errors": None,
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
        **{"HTTP_" + k.upper().replace("-", "_"): v for k, v in headers.items()},
    }

    # Ejecutar la aplicación Flask
    with app.app_context():
        response = app(environ, lambda status, headers: None)

        # Convertir respuesta
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response[0].decode("utf-8") if response else "",
        }
