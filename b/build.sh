#!/bin/bash
# Instala gunicorn primero
pip install gunicorn==20.1.0  # Puedes especificar una versión o dejarlo sin versión
# Luego instala los demás requirements
pip install -r requirements.txt