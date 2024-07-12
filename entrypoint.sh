#!/bin/sh

# Check if PORT is set, if not assign a default value
if [ -z "$PORT" ]; then
  PORT=5000
fi

# Export the PORT environment variable
export PORT

# Log the PORT value for debugging
echo "Starting Gunicorn on port: $PORT"

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT app:app
