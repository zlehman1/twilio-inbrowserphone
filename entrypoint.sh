#!/bin/sh

# Log the PORT value for debugging
echo "Starting Gunicorn on port: $PORT"

# Export the PORT variable to ensure it's correctly interpreted
export PORT

# Start Gunicorn
gunicorn --bind 0.0.0.0:$PORT app:app
