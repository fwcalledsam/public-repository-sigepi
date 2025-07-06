from run import app
from flask import jsonify


# Necesario para el despliegue en Vercel
def handler(request):
    with app.app_context():
        response = app.full_dispatch_request()
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response.get_data().decode("utf-8"),
        }
