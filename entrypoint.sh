#!/bin/sh

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT app:app
