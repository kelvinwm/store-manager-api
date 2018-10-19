from flask import make_response, jsonify, request
from app.api.v1.utils import Validate
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from instance.config import Config
import functools


config = Config()
users=[]
products = []
all_sales = []
cart_items = []


class Products:
    """Product functions"""

    def get_all_products(self):
        return make_response(jsonify({
            "All products": products
        }), 200)

    def add_product(self, product_name, price, description, quantity):
        item_id = len(products) + 1

        Validate().validate_type(price, quantity)
        new_product = {"id": item_id,
                       "product_name": product_name,
                       "description": description,
                       "quantity": quantity,
                       "price": price}
        products.append(new_product)
        return make_response(jsonify({
            "status": "OK",
            "Message": "Product added successfully",
            "Products": products
        }), 201)

    def get_one_product(self, product_id):
        item = [product for product in products if product["id"] == product_id]
        if not item:
            return make_response(jsonify({
                "status": "OK",
                "Product": "Product not found"
            }), 404)
        return make_response(jsonify({
            "status": "OK",
            "product": item
        }), 200)

    def update_product(self, product_id, product_name, description, quantity, price):

        product = [product for product in products if product["id"] == product_id]
        if not product:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product not found"
            }), 404)
        product[0]['id'] = product_id
        product[0]['description'] = description
        product[0]['quantity'] = quantity
        product[0]['product_name'] = product_name
        product[0]['price'] = price
        return make_response(jsonify({
            "status": "OK",
            "Message": product
        }), 200)

    def delete_product(self, product_id):
        product = [product for product in products if product['id'] == product_id]
        if not product:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product not found"
            }), 404)

        products.remove(product[0])
        return make_response(jsonify({
            "status": "OK",
            "Message": "Product deleted successfully"
        }), 200)


class Sales:
    """sales functions"""

    def get_all_sales(self):
        return make_response(jsonify({
            "All sales": all_sales
        }), 200)

    def add_sale(self, attendant_name, product_name, quantity, price, total_price, date):
        item_id = len(all_sales) + 1
        new_sale = {"sale_id": item_id,
                    "attendant_name": attendant_name,
                    "product_name": product_name,
                    "quantity": quantity,
                    "price": price,
                    "total_price": total_price,
                    "date": date}
        all_sales.append(new_sale)
        product_id = [product for product in products if product['product_name'] == product_name]
        if product_id:
            """call delete function from products class to delete the product from the products list"""
            product_id[0]['quantity']=product_id[0]['quantity']-1
        return make_response(jsonify({
            "status": "OK",
            "Message": "Product added successfully",
            "all_sales": all_sales
        }), 201)

    def get_one_sale(self, product_id):
        item = [sale for sale in all_sales if sale["sale_id"] == product_id]
        if not item:
            return make_response(jsonify({
                "status": "OK",
                "Product": "Product not found"
            }), 404)
        return make_response(jsonify({
            "status": "OK",
            "Sale": item
        }))

    def update_sale(self, product_id, attendant_name, product_name, quantity, price, total_price, date):
        update_sale = [sale for sale in all_sales if sale['sale_id'] == product_id]
        if not update_sale:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product not found"
            }), 404)
        update_sale[0]['sale_id'] = product_id
        update_sale[0]['product_name'] = product_name
        update_sale[0]['quantity'] = quantity
        update_sale[0]['attendant_name'] = attendant_name
        update_sale[0]['price'] = price
        update_sale[0]['total_price'] = total_price
        update_sale[0]['date'] = date
        return make_response(jsonify({
            "status": "OK",
            "Message": all_sales
        }), 200)

    def delete_sale(self, product_id):
        sale = [sale for sale in all_sales if sale['sale_id'] == product_id]
        if not sale:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product not found"
            }), 404)

        all_sales.remove(sale[0])
        return make_response(jsonify({
            "status": "OK",
            "Message": "Product deleted successfully"
        }), 200)


class Users:
    def login(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({"Message": "Please enter all credentials"})
        user = [user for user in users if user["name"] == auth.username]
        if not user:
            return jsonify({"Message": "User does not exist"})
        if check_password_hash(user[0]["password"], auth.password):
            """generate token"""
            s = Serializer(config.SECRET_KEY, expires_in=30)
            token = s.dumps({"username": user[0]["name"]}).decode('utf-8')

            return jsonify({"Token": token})

        return jsonify({"Message": "Invalid credentials"})

    def add_user(self):
        data = request.get_json()
        passwd = generate_password_hash(data["password"], method="sha256")

        new_user = {"name": data["username"],
                    "password": passwd,
                    "Role": data["role"]}
        users.append(new_user)
        return jsonify({"Message": "User registered successfully",
                        "Users": users})
