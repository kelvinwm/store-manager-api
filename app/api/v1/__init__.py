from flask import Blueprint
from flask_restful import Api

from app.api.v1.views.views import (Products, Product, Sales, Home,
                                    Sale, UserSignup, UserLogin)

admin_api = Blueprint("admin_api", __name__)
api = Api(admin_api)
api.add_resource(Products, '/products', endpoint="products")
api.add_resource(Product, '/products/<int:product_id>', endpoint="product")
api.add_resource(Sales, '/sales', endpoint="sales")
api.add_resource(Sale, '/sales/<int:sale_id>', endpoint="sale")
api.add_resource(UserLogin, '/login', endpoint="auth_login")
api.add_resource(UserSignup, '/signup', endpoint="auth_signup")
api.add_resource(Home, '/', endpoint="Home")
