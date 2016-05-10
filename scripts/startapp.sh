#!/bin/sh
set -e
APPNAME=$1
env=$2
source $env/bin/activate
APPDIR=/var/www/$APPNAME
cd $APPDIR
pip install -r requirements.pip
export PYTHONPATH=$PYTHONPATH:$APPDIR
export DJANGO_SETTINGS_MODULE=main.settings.production
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate
$env/bin/gunicorn -c scripts/gunicorn.py main.wsgi --reload
