#!/usr/bin/env bash

set -eux

cd $(dirname $0)/..

poetry run flake8 acoustid_search
poetry run mypy acoustid_search
poetry run pytest acoustid_search
