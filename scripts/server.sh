#!/usr/bin/env bash

set -eux

exec gunicorn -k aiohttp.GunicornWebWorker 'acoustid_search.app:create_app' "$@"
