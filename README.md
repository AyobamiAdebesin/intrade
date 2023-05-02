# intrade

A scalable backend API for an ecommerce company with recurring payment features
## INSTRUCTIONS ON HOW TO RUN THIS PROJECT

* To run this project, you will need to clone this repository into your local machine. On the command line, start by running 
```
git clone https://github.com/AyobamiAdebesin/intrade
```

* Next you will need to navigate into the intrade folder. Run:
```
cd intrade/
```

* Next, you will need to start a virtual environment to run this project. Make sure you have python's ```pipenv``` installed on your machine. Run
```
pipenv install
```
This will install all the dependencies needed for running this project from the Pipfile and Pipfile.lock.

* Activate the virtual environment by running:
```
pipenv shell
```

* Next you need to setup the database for the backend. I have used Amazon RDS PostgreSQL database. If you wish to use Amazon RDS, you will need to create a PostgreSQL database on Amazon RDS and then copy the credentials to the settings.py file in the intrade/intrade folder. If you wish to use a local database, you will need to install PostgreSQL on your machine and then create a database. You will then need to copy the credentials to the settings.py file in the intrade/intrade folder. For testing purposes, you can use the database credentials in the settings.py file as they are.

* Next, you will need to run the migrations to create the tables in the database. Run:
```
python manage.py makemigrations && python manage.py migrate
```

* Next, you will need to create a superuser to access the admin panel. Run:
```
python manage.py createsuperuser
```
and follow the prompts to create a superuser.

* Next, you will need to run the server. Run:
```
python manage.py runserver
```

### PROJECT DEPENDENCIES
* Python 3.8
* Django 4.2
* Django debug toolbar 4.0.0
* Django Rest Framework 3.14.0
* Amazon RDS PostgreSQL
* Pipenv 2020.11.15
* Requests 2.29.0
* Djoser 2.0.3
* Django Rest Framework Simple JWT 5.2.2
* Django Filter 23.2
* Psycopg2 2.9.6


### API ENDPOINTS
GET: /http://127.0.0.1:8000/intrade - This is the root endpoint. It returns a list of all the endpoints in the API.

GET: "http://127.0.0.1:8000/intrade/products/" - This endpoint returns a list of all the products in the database.





