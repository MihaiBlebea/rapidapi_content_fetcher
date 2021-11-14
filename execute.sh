#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
eval "./virtualenv/bin/gunicorn --bind 0.0.0.0:5000 api:app"