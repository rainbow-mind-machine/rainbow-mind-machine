#!/bin/bash

cd /api

pip3 install -r requirements.txt

exec "$@"
 
