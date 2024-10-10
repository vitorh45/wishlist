# Wishlist system

## Contents of this file

 - Introduction
 - Requirements
 - Installation and usage
 - Endpoints

## Introduction

Wishlist is a project to simulate a wish list in a online store.

## Requirements

 - Python 3.11+
 - Postgres as database
 - Docker to create the images (optional)

## Installation and usage

To run the project locally, we need to follow some steps:

 - First we need to have python 3.11 installed. You can use the lib pyenv to control different python versions.
 - Is optional and recommended to use a virtualenv with the python 3.11. By doing that, you can isolate you projects environments.
 - Install the projects dependencies inside the SRC directory with run the command `pip install -r dependencies/requirements-dev.txt`.
 - Rename the `.env_sample` file to `.env`.
 - Having a Postgres running locally, create two databases called `accounttest` and `accounttest_test`. If you change the default Postgres port, change the value in the `.env` file.
 - Create the database tables running the migration command inside the src/api dir: `flask db upgrade`
 - Run the project locally with `flask run`
 - If you want to run using Docker, run the command in the project root dir `docker-compose up`. It will build and start an image of the project and a Postgres as well. Make sure you don't have another postgres instance running in the port 5342.
- to run the unit tests and check the coverage, run the command in root dir `make test`

## Endpoints

Now that the project is running locally in the address http://localhost:5000 (or http://localhost:5001 with the docker image), we are going to do requests to interact with the application.

### Requests
- POST /api/v1/user/login: Pass in the request body two parameters `username` and `password` to authenticate and get the authorization token. The default values are in environment variables for testing purposes.

#### Protected requests
Use the token generated previously in the request header for all following requests. Use the format `Authorization: Bearer {token}`

##### Clients
- POST /api/v1/clients: send two parameters in the request body to create the client. Example: `{"name": "John Wick", "email": "johnwick@gmail.com"}`
- PATCH /api/v1/clients?email=email_value: add in the url parameters the user email and send the new user name in the request body to update the client. Example: `{"name": "John Wick"}`
- GET /api/v1/clients?email=email_value: add in the url parameters the user email to get the client data
- DELETE /api/v1/clients?email=email_value: add in the url parameters the user email to delete the client

##### Products
- GET /api/v1/products?limit=limit_value&offset=offset_value: add in the url parameters the limit and offset as integers to the get the products list filtered.
- GET /api/v1/products/<product_id>: add in the url parameters the product id as UUID to the get the product data.

##### Wishlist
- POST /api/v1/wishlists: send the client_id parameters in the request body to create the wishlist. Example: `{"client_id": "88a29add-72ee-4cdb-8630-efd006107a8c"}`
- GET /api/v1/wishlists/<wishlist_id>: add in the url parameters the wishlist id as UUID to the get the wishlist data.
- PUT /api/v1/wishlists/<wishlist_id>: add in the url parameters the wishlist id as UUID send the product_id parameters in the request body to add a product in the wishlist. Example: `{"client_id": "88a29add-72ee-4cdb-8630-efd006107a8c"}`

### In order to ease the tests, there are two json files with the Postman collections used to test the endpoints.

- Go to Postman, on the top left side click the button `Import`. Select the file and proceed. To the same process with the two files.
- In case you run the project in a different port, change its value in the Postman environments section. 

### Responses
- 200: if the request is successfull
- 201: if the request is successfull
- 401: if you try to authenticate with invalid credentials
- 404: if you try to get a resource but it is not found
- 404: if you try to add a duplicate product in a wishlist

