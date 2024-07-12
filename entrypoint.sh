#!/bin/sh

# Check if PORT is set, if not assign a default value
if [ -z "$PORT" ]; then
  PORT=5000
fi

# Export the PORT environment variable
export PORT

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT app:app
