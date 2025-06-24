#!/bin/sh

# Start Gunicorn in the background
# Ensure the app module and instance are correctly named (e.g., app:app)
# The number of workers can be adjusted based on CPU cores, e.g., (2*CPU)+1
gunicorn --workers 3 --bind 127.0.0.1:8000 app:app &

# Start Nginx in the foreground
nginx -g 'daemon off;'
