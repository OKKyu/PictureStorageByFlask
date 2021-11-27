#!/bin/bash

source ./venv/bin/activate
gunicorn -w $1 -b $2:$3 main:app --timeout 240 --certfile=env/certfile.crt --keyfile=env/secret_PS.key
#gunicorn -w $1 -b $2:$3 main:app --timeout 240
