#!/bin/bash

CUSTOM_CONFIG=/tmp/config/config.py
if [ -f "$CUSTOM_CONFIG" ]; then
  echo "Using config file: $CUSTOM_CONFIG"
  cp $CUSTOM_CONFIG /home/shico/shico/server/config.py
else
  echo "Using default config"
  # Update ShiCo config file
  cp /home/shico/shico/server/config.docker-default.py /home/shico/shico/server/config.py
fi

# serve backend
gunicorn --bind 0.0.0.0:8000 --timeout 1200 shico.server.wsgi:app
