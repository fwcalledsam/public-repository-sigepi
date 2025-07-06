from app import app
from werkzeug.datastructures import Headers
import json


def handler(event, _):
    # Convertir evento API Gateway a entorno WSGI
    headers = Headers()
    for key, value in (event.get("headers") or {}).items():
        headers.add(key, value)

    body = event.get("body", "") or ""
    query = event.get("queryStringParameters", {}) or {}

    environ = {
        "REQUEST_METHOD": event["httpMethod"],
        "SCRIPT_NAME": "",
        "PATH_INFO": event["path"],
        "QUERY_STRING": "&".join([f"{k}={v}" for k, v in query.items()]),
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "443",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": headers.get("X-Forwarded-Proto", "https"),
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

        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response[0].decode("utf-8") if response else "",
        }
