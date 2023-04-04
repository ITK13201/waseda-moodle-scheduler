#!/bin/bash

if command -v docker 1> /dev/null 2>&1; then
    docker compose exec python python "$@"
  else
    python "$@"
fi
