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

* You can then use the url displayed on the terminal to access the browsable API where you can test the endpoints.

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

#### CARTS ENDPOINTS
GET: /http://127.0.0.1:8000/intrade - This is the root endpoint. It returns a list of all the endpoints in the API.

GET: "http://127.0.0.1:8000/intrade/collections/": - This endpoint returns a list of all the collections in the database. If you decide to use the already created database, the database contains a dummy data consisting of a list of 1000 collections that have been paginated. If you decide to create your own database, you will see an empty list. You will need to create collections in the admin panel to see the collections in the database. Or you can also create dummy data from online sources.


GET: "http://127.0.0.1:8000/intrade/products/" - This endpoint returns a list of paginated products in the database. If you decide to use the already created database, the database contains a dummy data consisting of a list of 1000 products. If you decide to create your own database, you will see an empty list. You will need to create products in the admin panel to see the products in the database. Or you can also create dummy data from online sources.

POST: {} :"http://127.0.0.1:8000/intrade/carts" -  This endpoint creates a cart. It takes a product id and a quantity as parameters. It returns the cart id, the product id, the quantity and the total price of the cart.
Carts are anonymous. They are not tied to a user. We can fetch them by their id.

POST: {productId, quantity} : "http://127.0.0.1:8000/intrade/carts/:id/items" -  This endpoint adds an item to a cart. It takes a product id and a quantity as parameters. It returns the cart id, the product id, the quantity and the total price of the cart.

PATCH: {quantity} : "http://127.0.0.1:8000/intrade/carts/:id/items/:id" -  This endpoint updates the quantity of an item in a cart. It takes a quantity as a parameter. It returns the cart id, the product id, the quantity and the total price of the cart.

DELETE: http://127.0.0.1:8000/intrade/carts/:id/items/:id -  This endpoint deletes an item from a cart. It returns the cart id, the product id, the quantity and the total price of the cart.

GET: http://127.0.0.1:8000/intrade/carts/:id -  This endpoint returns a cart. It returns the cart id, the product id, the quantity and the total price of the cart.

DELETE: "http://127.0.0.1:8000/intrade/carts/:id" - This endpoint deletes a cart. It returns the cart id, the product id, the quantity and the total price of the cart.

### USER ENDPOINTS
GET: {} : "http://127.0.0.1:8000/auth/users/" - This endpoint returns a list of all the users in the database. You need to be authorized to access this endpoint. We have used JWT authentication for this project. You will need to create a user and then login to get the token. You can then use the token to access this endpoint.

POST: { email, username, password, first_name, last_name } : "http://127.0.0.1:8000/auth/users/" - This endpoint creates a user. It takes an email, a username and a password as parameters. It returns the user id, the user email, the user username and the user password. 

GET: {} : "http://127.0.0.1:8000/store/customers/ - We do not allow users to access this endpoint. It is only for the admin. It returns a list of all the customers in the database.