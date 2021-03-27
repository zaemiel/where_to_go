# Where to go Django app
Simple sharing places project built with Django 3, Vue.js 2 and using of OpenStreetMaps.

Demo website:
[http://anuctal.pythonanywhere.com/](http://anuctal.pythonanywhere.com/)

Admin credentials:

    login: demo
    password: demo


# Installation
1. Create a virtual environment:

        python -m venv venv

    or

        virtualenv venv

2. Activate the virtual environment:

        source venv/bin/activate

3. Clone the repo:

        git clone https://github.com/zaemiel/where_to_go.git


4. Install dependencies:

        pip install -r requirements.txt

5. Create the `.env` file:

        cd where_to_go/
        touch .env

6. Add to the `.env` file the following variables:

        DEBUG = False
        SECRET_KEY = 'your_secret_key'

7. Create a superuser:

        ./manage.py createsuperuser

8. Run Django dev server:

        ./manage.py runserver
