#!/usr/bin/env bash
HOST=0.0.0.0
PORT=8080
RELOAD_FLAG=""

if [ "$INSTALL_DEV" = true ]; then
  RELOAD_FLAG="--reload"
fi

poetry run uvicorn --workers 1 --host $HOST --port $PORT $RELOAD_FLAG app.core.api.main:app

