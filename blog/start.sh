#!/usr/bin/env sh
set -e

exec gunicorn -k uvicorn.workers.UvicornWorker -b :${PORT} blog.main:app