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

echo "Please input '0' if you want to use only webapp."
echo "If you want to use test script, please input other char."
read choose
if [ "$choose" == "0" ]; then
 pip install -r requirements.txt
else
 pip install -r requirements2.txt
fi
deactivate
