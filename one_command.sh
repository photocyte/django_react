#! bash

## Setup virtual environment.

#python3 -m venv venv
source venv/bin/activate

#pip install django djangorestframework biopython django-cors-headers

#django-admin startproject django_react .
#django-admin startapp leads

cd frontend; npm run dev; cd ..
rm -rf leads/migrations/
rm -f db.sqlite3
python manage.py makemigrations leads
python manage.py migrate
##python manage.py createsuperuser
python manage.py runserver
