#!/usr/bin/env bash

MODE="prod" ## or "dev"

### Setup virtual environment.
# sudo apt install -y python3 python3-venv python3-dev python3-wheel gcc python3-pip
# python3 -m venv venv
source venv/bin/activate
# pip install django djangorestframework biopython django-cors-headers python-dotenv
# sudo apt install -y npm


#django-admin startproject django_react .
#django-admin startapp dnaquery
#django-admin startapp frontend
#mkdir -p ./frontend/src/components
#mkdir -p ./frontend/{static,templates}/frontend

#cd ./frontend && npm init -y
#npm i webpack webpack-cli --save-dev
# Add scripts to package.json
#npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
#npm i react react-dom --save-dev
# Add presets to .babelrc
# add rules to webpack.config.js

## Pull down the bioconda container for diamond, execute using singularity/apptainer
## apptainer pull docker://quay.io/biocontainers/diamond:2.0.15--hb97b32f_1

cd frontend; npm run dev; cd ..
rm -rf leads/migrations/
rm -f db.sqlite3
rm -rf ./static ## for collectstatic

python manage.py makemigrations dnaquery
python manage.py migrate
##python manage.py createsuperuser ## Doesn't seem necesarry
if [[ "$MODE" == "dev" ]];
then
python manage.py runserver --insecure 0.0.0.0:52371 ## --insecure required to shut off Debug mode & not run it via wsgi/nginx reverse proxy
fi

if [[ "$MODE" == "prod" ]];
then
pgrep gunicorn | xargs kill

python manage.py collectstatic ## only necesarry when trying to run production

### Deploy to production...
#python3 manage.py check --deploy
#pip3 install uwsgi
#sudo apt install nginx
#uwsgi --http 0.0.0.0:52371 --home /home/tim/source/git/django_react/venv --chdir /home/tim/source/git/django_react/ -w django_react.wsgi

## gunicorn seems easier to use than uswgi
gunicorn django_react.wsgi --bind 127.0.0.1:8000 ## --keyfile privkey.pem --certfile fullchain.pem ## nginx will handle the https

## nginx is running all the time on my linux VM so not so sure if that counts as "one command"
## nginx configured at /etc/nginx/sites-enabled/django_react 
## and /etc/nginx/nginx.conf 
# sudo systemctl restart nginx

fi
