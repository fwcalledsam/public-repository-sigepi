#!/bin/bash
# Instalar dependencias del sistema (como en tu Dockerfile)
apt-get update && apt-get install -y libpq-dev gcc

# Instalar dependencias de Python
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt gunicorn