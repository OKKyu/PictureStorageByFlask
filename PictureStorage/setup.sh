#!/bin/bash
if [ -d ./venv ]; then
  rm -rf ./venv/.*
  rm -rf ./venv/*
  rmdir ./venv
fi
if [ ! -d ./venv ]; then
 mkdir venv
fi
if [ ! -d ./log ]; then
 mkdir log
fi
if [ ! -d ./data ]; then
 mkdir data
fi

python3 -m venv venv
source ./venv/bin/activate
pip install -U pip

if [ "$1" == "t" ]; then
 pip install -r requirements2.txt
else
 pip install -r requirements1.txt
fi
deactivate
