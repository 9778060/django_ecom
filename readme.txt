VENV:
Install - virtualenv venv -p python3.12
Activate - venv\Scripts\activate
Deactivate - deactivate

REQUIREMENTS INSTALL:
Install - pip install -r requirements.txt

DJANGO:
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial
python manage.py createsuperuser
python manage.py runserver
