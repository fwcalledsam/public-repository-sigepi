#!/bin/bash
# Skip system package installation since we can't modify the system in Render
python -m pip install --upgrade pip
python -m pip install --user --no-cache-dir -r requirements.txt
python -m pip install --user gunicorn==20.1.0