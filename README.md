# Kitchen-service

Django project for managing cooks in kitchen

## Check it out!

[Kitchen service project deployed to Render](https://kitchen-service.render.com/)

## Installation

``` Shell
git clone https://github.com/mdubyna/kitchen-servise.git
cd kitchen-servise
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Features

* Authentication functionality for Cook/User
* Managing cooks, dishes, dish types directly from website interface
* Powerful admin panel for advanced managing


## Environment variables

This project uses the following environment variables(type: str):
* DJANGO_SECRET_KEY - for set up SECRET_KEY
* DJANGO_DEBUG - for DEBUG ("RENDER" by default)
* DATABASE_URL - for url to project database (db.sqlite3 is used by default)
