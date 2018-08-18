#!/bin/sh

CUSTOM_CONFIG=/tmp/config/config.json
if [ -f "$CUSTOM_CONFIG" ]; then
  echo "Using config file: $CUSTOM_CONFIG"
  cp $CUSTOM_CONFIG ./src/config.json
fi

# serve webapp
gulp serve
