[![Coverage Status](https://coveralls.io/repos/github/kelvinwm/store-manager-api/badge.svg?branch=ft-api-user-signup-161361425)](https://coveralls.io/github/kelvinwm/store-manager-api?branch=ft-api-user-signup-161361425)
[![Build Status](https://travis-ci.org/kelvinwm/store-manager-api.svg?branch=ft-api-create-sale-record-161300201)](https://travis-ci.org/kelvinwm/store-manager-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/48a671ab90d9f9e709f4/maintainability)](https://codeclimate.com/github/kelvinwm/store-manager-api/maintainability)

## store-manager-api

Store Manager is a web application that helps store owners manage sales and product inventory
records. This application is meant for use in a single store

## Getting Started

Instructions on how to run on your local machine for development and testing purposes. 

### Prerequisites

* Git
* Python 3.6.4
* Virtualenv

### Quick Start

1. Clone the repository

```
https://github.com/kelvinwm/store-manager-api
```
2. Initialize and activate a virtualenv

```
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

3. Install the dependencies

```
$ pip install -r requirements.txt
```

4. Run the development server

```
$ python run.py
```

5. Navigate to [http://localhost:5000](http://localhost:5000)

## Endpoints
Here is a list of all endpoints for store manager API

Endpoint | Functionality 
------------ | -------------
POST   /api/v1/auth/signup | Register a user
POST   /api/v1/auth/login | Log in user
POST  /api/v1/products | Add a product
POST  /api/v1/sales  | Add a sale record
GET  /api/v1/products | Get all products
GET  /api/v1/products/id  | Get a single product
PUT  /api/v1/products/id | Update a single product
DELETE  /api/v1/products/id | Delete a single product
GET  /api/v1/sales | Get all sale records
GET  /api/v1/sales/id | Get a single sale record
PUT  /api/v1/sales/id | Update a single sale record
DELETE  /api/v1/sales/id | Delete a single sale record



