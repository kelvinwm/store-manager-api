from flask import Blueprint
from flask_restful import Api

from app.api.v1.views.views import Products
    # , Product, Sale, Sales, Cart, CartItem

admin_api = Blueprint("admin_api", __name__)
api = Api(admin_api)
api.add_resource(Products, '/products', endpoint="products")
# api.add_resource(Product, '/products/<int:product_id>', endpoint="product")
# api.add_resource(Sales, '/sales', endpoint="sales")
# api.add_resource(Sale, '/sales/<int:sale_id>', endpoint="sale")
# api.add_resource(Cart, '/cart', endpoint="cart")
# api.add_resource(CartItem, '/cart/<int:cart_id>', endpoint="cart_item")