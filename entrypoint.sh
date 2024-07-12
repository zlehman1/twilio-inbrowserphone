#!/bin/sh

# Export the PORT environment variable
export PORT=${PORT}

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT app:app
