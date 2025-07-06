#!/bin/bash
# Instalar dependencias del sistema
apt-get update && apt-get install -y libpq-dev gcc python3-dev

# Instalar dependencias de Python incluyendo gunicorn
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt
python -m pip install gunicorn==20.1.0