#!/bin/sh

# Export the PORT environment variable
export PORT

# Log the PORT value for debugging
echo "Starting Gunicorn on port: $PORT"

# Start Gunicorn
gunicorn --bind 0.0.0.0:$PORT app:app
