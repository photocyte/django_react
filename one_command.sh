#!/usr/bin/env bash

### Setup virtual environment.
# sudo apt install -y python3 python3-venv python3-dev python3-wheel gcc python3-pip
# python3 -m venv venv
source venv/bin/activate
# pip install django djangorestframework biopython django-cors-headers
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

## apptainer pull docker://quay.io/biocontainers/diamond:2.0.15--hb97b32f_1

cd frontend; npm run dev; cd ..
rm -rf leads/migrations/
rm -f db.sqlite3

python manage.py makemigrations dnaquery
python manage.py migrate
##python manage.py createsuperuser ## Doesn't seem necesarry
python manage.py runserver --insecure 0.0.0.0:52371 ## --insecure required to shut off Debug mode & not run it on real host

### Deploy to production
#python3 manage.py check --deploy
#pip3 install uwsgi
#sudo apt install nginx
#uwsgi --http :8080 --home /home/tim/source/git/django_react/venv --chdir /home/tim/source/git/django_react/ -w django_react.wsgi
