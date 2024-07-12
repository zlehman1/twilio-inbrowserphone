#!/bin/sh

# Log the PORT value for debugging
echo "Starting Gunicorn on port: $PORT"

# Start Gunicorn
gunicorn --bind 0.0.0.0:$PORT app:app
