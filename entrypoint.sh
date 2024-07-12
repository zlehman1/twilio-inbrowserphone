#!/bin/sh

# Check if PORT is set, if not assign a default value
if [ -z "$PORT" ]; then
  PORT=5000
fi

# Export the PORT environment variable
export PORT

# Log the PORT value for debugging
echo "Starting Gunicorn on port: $PORT"

# Validate that PORT is a valid integer
if ! [ "$PORT" -eq "$PORT" ] 2>/dev/null; then
  echo "Error: PORT is not a valid integer."
  exit 1
fi

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT app:app
