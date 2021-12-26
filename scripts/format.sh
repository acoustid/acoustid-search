#!/usr/bin/env bash

set -eux

cd $(dirname $0)/..

poetry run black acoustid_search
