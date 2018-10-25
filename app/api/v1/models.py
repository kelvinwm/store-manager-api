import re

from flask import make_response, jsonify, request, Flask
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import jwt
import datetime
from validate_email import validate_email

app = Flask(__name__)
products = []
all_sales = []
cart_items = []
users = []
black_listed_tokens = []
app.config["SECRET_KEY"] = "NOCSNDOCNnocnsodi"
now = datetime.datetime.now()


def login_required(func):
    @functools.wraps(func)
    def user_auth(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
            tk = [tk for tk in black_listed_tokens if token == tk]
            if tk:
                return "Token blacklisted, please login"
        if not token:
            return "No token"
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = data['username']
        except:
            return "Token is invalid"
        return func(current_user, token, *args, **kwargs)

    return user_auth


class Products:
    """Product functions"""

    @login_required
    def get_all_products(current_user, token, self):
        """View all products"""
        if len(products) == 0:
            return make_response(jsonify({
                "Message": "Empty list"
            }), 200)
        return make_response(jsonify({
            "All products": products
        }), 200)

    @login_required
    def add_product(current_user, token, self, **args):
        """Add a single product"""
        if not args['description'] or not args['product_name'] or args['quantity'] < 1 or args['price'] < 1:
            return jsonify({"Message": "Invalid entry"})
        if current_user != "admin":
            return make_response(jsonify({
                "Message": "Permission denied.Contact admin"
            }))
        product = [product for product in products if product["product_name"] == args['product_name']]
        if product:
            return "Products already exists"
        item_id = len(products) + 1
        new_product = {"id": item_id,
                       "product_name": args['product_name'],
                       "description": args['description'],
                       "quantity": args['quantity'],
                       "price": args['price']}
        products.append(new_product)
        return make_response(jsonify({
            "status": "OK",
            "Message": "Product added successfully",
            "Products": products
        }), 201)

    @login_required
    def get_one_product(current_user, token, self, product_id):
        """Get a single product"""
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

    @login_required
    def update_product(current_user, token, self, product_id, **kwargs):
        """Update a single product"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact admin"
            }))
        product = [product for product in products if product["id"] == product_id]
        if not product:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product not found"
            }), 404)
        product[0]['id'] = product_id
        product[0]['description'] = kwargs['description']
        product[0]['quantity'] = kwargs['quantity']
        product[0]['product_name'] = kwargs['product_name']
        product[0]['price'] = kwargs['price']
        return make_response(jsonify({
            "status": "OK",
            "Message": product
        }), 200)

    @login_required
    def delete_product(current_user, token, self, product_id):
        """Delete a single product"""
        if current_user != "true":
            return make_response(jsonify({
                "Message": "Permission denied.Contact admin"
            }))
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

    @login_required
    def get_all_sales(current_user, token, self):
        """Get all sale record"""
        if current_user != "admin":
            return make_response(jsonify({
                "Message": "Permission denied.Contact admin"
            }))
        if len(all_sales) == 0:
            return make_response(jsonify({
                "Message": "Empty list"
            }), 200)
        return make_response(jsonify({
            "All sales": all_sales
        }), 200)

    @login_required
    def add_sale(current_user, token, self, **kwargs):
        """Add a single sale record"""
        if not kwargs['attendant_name'] or not kwargs['product_name'] or kwargs['quantity'] < 1 or kwargs['price'] < 1 \
                or kwargs['total_price'] < 1:
            return jsonify({"Message": "Invalid entry"})
        user = [user for user in users if user["name"] == kwargs['attendant_name']]
        if not user:
            return jsonify({"Message": "Please login to your account"})
        item_id = len(all_sales) + 1
        new_sale = {"sale_id": item_id,
                    "attendant_name": kwargs['attendant_name'],
                    "product_name": kwargs['product_name'],
                    "quantity": kwargs['quantity'],
                    "price": kwargs['price'],
                    "total_price": kwargs['total_price'],
                    "date": now}
        product = [product for product in products if product['product_name'] == kwargs['product_name']]
        if not product:
            return make_response(jsonify({
                "Message": "No such product"
            }), 200)
        if product:
            """call delete function from products class to delete the product from the products list"""
            product[0]['quantity'] = product[0]['quantity'] - kwargs['quantity']
            if product[0]['quantity'] < 0:
                return jsonify({"Message": "Product is finished, Please restock"})
        all_sales.append(new_sale)
        return make_response(jsonify({
            "status": "OK",
            "Message": "Product added successfully",
            "all_sales": all_sales
        }), 201)

    @login_required
    def get_one_sale(current_user, token, self, product_id):
        """Get a single sale record"""
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

    @login_required
    def update_sale(current_user, token, self, product_id, **kwargs):
        """Update a single sale record"""
        if not kwargs['attendant_name'] or not kwargs['product_name'] or kwargs['quantity'] < 1 or kwargs['price'] < 1 \
                or kwargs['total_price'] < 1:
            return jsonify({"Message": "Invalid entry"})
        update_sale = [sale for sale in all_sales if sale['sale_id'] == product_id]
        if not update_sale:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product not found"
            }), 404)
        update_sale[0]['sale_id'] = product_id
        update_sale[0]['product_name'] = kwargs['product_name']
        update_sale[0]['quantity'] = kwargs['quantity']
        update_sale[0]['attendant_name'] = kwargs['attendant_name']
        update_sale[0]['price'] = kwargs['price']
        update_sale[0]['total_price'] = kwargs['total_price']
        update_sale[0]['date'] = now
        return make_response(jsonify({
            "status": "OK",
            "Message": all_sales
        }), 200)

    @login_required
    def delete_sale(current_user, token, self, product_id):
        """Delete a single sale record"""
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
        """A user can login and get a token"""
        data = request.get_json()
        if not data or not data["email"] or not data["password"]:
            return jsonify({"Message": "Please enter all credentials"})
        is_valid = validate_email(data["email"])
        if not is_valid:
            return jsonify({"Message": "Invalid email"})
        user = [user for user in users if user["email"] == data["email"]]
        if not user:
            return jsonify({"Message": "User does not exist"})
        if check_password_hash(user[0]["password"], data["password"]):
            """generate token"""
            token = jwt.encode({"username": user[0]["Role"], 'exp': datetime.datetime.utcnow()
                                                                    + datetime.timedelta(minutes=60)},
                               app.config["SECRET_KEY"])
            return jsonify({"Token": token.decode('UTF-8')})
        return jsonify({"Message": "Invalid credentials"})

    def add_user(self):
        """A user can signup"""
        data = request.get_json()
        if not data["email"] or not data["password"] or not data["role"]:
            return make_response(jsonify({"message": "Enter all credentials"}))
        is_valid = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data["email"])
        if not is_valid or not re.match('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$])', data["password"]) \
                or len(data["password"]) > 12:
            return jsonify({"Message": "Invalid email or password"})
        pws = data["password"]
        password = generate_password_hash(pws, method="sha256")
        new_user = {"name": data["username"],
                    "email": data["email"],
                    "password": password,
                    "Role": data["role"]}
        user = [user for user in users if user["email"] == new_user["email"]]
        if user:
            return "User Already registered"
        users.append(new_user)
        return make_response(jsonify({"Message": "User registered successfully", "Users": users}), 201)

    @login_required
    def log_out(curreent_user, token, self):
        black_listed_tokens.append(token)
        return make_response(jsonify({"Message": "User logout successful"}), 200)
