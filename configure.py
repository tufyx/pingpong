#! /bin/bash
# Flask initialization script

# create virtual environment
virtualenv venv

# install Flask
pip install Flask

# install dependencies
venv/bin/pip install flask-login
venv/bin/pip install flask-openid
venv/bin/pip install flask-mail==0.7.6
venv/bin/pip install sqlalchemy==0.7.9
venv/bin/pip install flask-sqlalchemy==0.16
venv/bin/pip install sqlalchemy-migrate==0.7.2
venv/bin/pip install flask-whooshalchemy==0.55a
venv/bin/pip install WTForms-Alchemy
venv/bin/pip install pytz==2013b
venv/bin/pip install flask-babel==0.8
venv/bin/pip install flup
venv/bin/pip install pymysql

# create folder structure
mkdir app
mkdir app/static
mkdir app/templates
mkdir tmp