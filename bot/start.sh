#!/bin/sh

python main.py &
nginx -g "daemon off;"
