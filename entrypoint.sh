#!/bin/sh

# Log the PORT value for debugging
echo "Starting Gunicorn on port: $PORT"

# Check if PORT is set and is a valid number
if [ -z "$PORT" ] || ! [ "$PORT" -eq "$PORT" ] 2>/dev/null; then
  echo "Error: PORT is not set or is not a valid number."
  exit 1
fi

# Export the PORT variable to ensure it's correctly interpreted
export PORT

# Start Gunicorn
gunicorn --bind 0.0.0.0:$PORT app:app
