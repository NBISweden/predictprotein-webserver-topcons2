#!/bin/bash
mkdir -p /topcons/proj/pred/static/log
touch /topcons/proj/pred/static/log/debug.log
cd /topcons
cp proj/dev_settings.py proj/settings.py
python3 /topcons/manage.py runserver 8000
