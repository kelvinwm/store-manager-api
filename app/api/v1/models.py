from flask import make_response, jsonify, request, Flask
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import jwt
import datetime


app= Flask(__name__)
products = []
all_sales = []
cart_items = []
users = []
app.config["SECRET_KEY"]="NOCSNDOCNnocnsodi"


def login_required(func):
    @functools.wraps(func)
    def user_auth(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return "No token"
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = data['username']
        except:
            return "Token is invalid"

        return func(current_user, *args, **kwargs)

    return user_auth


class Products:
    """Product functions"""

    @login_required
    def get_all_products(current_user, self):
        return make_response(jsonify({
            "All products": products
        }), 200)

    @login_required
    def add_product(current_user, self, product_name, price, description, quantity):
        if not current_user == "admin":
            return make_response(jsonify({
                "Message": "Permission denied"
            }))
        item_id = len(products) + 1
        if price < 0:
            # raise ValueError("price cannot be a negative number")
            return make_response(jsonify({
                "Message": "price cannot be a negative number"
            }), 200)
        if quantity < 0:
            return make_response(jsonify({
                "Message": "Quantity cannot be a negative number"
            }), 200)
        # Validate().validate_type(quantity)
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

    @login_required
    def get_one_product(current_user, self, product_id):
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
    def update_product(current_user, self, product_id, product_name, description, quantity, price):

        if not current_user == "admin":
            return make_response(jsonify({
                "Message": "Permission denied"
            }))

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

    @login_required
    def delete_product(current_user, self, product_id):
        if not current_user == "admin":
            return make_response(jsonify({
                "Message": "Permission denied"
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
    def get_all_sales( current_user, self):
        if not current_user == "admin":
            return make_response(jsonify({
                "Message": "Permission denied"
            }))
        return make_response(jsonify({
            "All sales": all_sales
        }), 200)

    @login_required
    def add_sale(current_user, self, attendant_name, product_name, quantity, price, total_price, date):
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
            product_id[0]['quantity'] = product_id[0]['quantity'] - 1
        return make_response(jsonify({
            "status": "OK",
            "Message": "Product added successfully",
            "all_sales": all_sales
        }), 201)

    @login_required
    def get_one_sale(current_user, self, product_id):
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
    def update_sale(current_user, self, product_id, attendant_name, product_name, quantity, price, total_price, date):
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

    @login_required
    def delete_sale(current_user, self, product_id):
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


class Cart:
    """cart functions"""

    def get_all_cart_items(self):
        """Get all items in the cart"""
        return make_response(jsonify({
            "All sales": cart_items
        }), 200)

    def add_to_cart(self, product_name, quantity, price, total_price, date):
        """Get a single item"""
        item_id = len(cart_items) + 1

        if price < 0:
            return make_response(jsonify({
                "Message": "price cannot be a negative number"
            }), 200)
        if total_price < 0:
            return make_response(jsonify({
                "Message": "total_price cannot be a negative number"
            }), 200)
        if quantity < 0:
            return make_response(jsonify({
                "Message": "Quantity cannot be a negative number"
            }), 200)

        new_cart_item = {"id": item_id,
                         "product_name": product_name,
                         "quantity": quantity,
                         "price": price,
                         "total_price": total_price,
                         "date": date}
        cart_items.append(new_cart_item)

        return make_response(jsonify({
            "status": "OK",
            "Message": "Product added successfully",
            "all_sales": cart_items
        }), 201)

    def delete_cart_item(self, product_id):
        cart = [cart for cart in cart_items if cart['id'] == product_id]
        if not cart:
            return make_response(jsonify({
                "status": "OK",
                "Message": "Product not found"
            }), 404)

        cart_items.remove(cart[0])
        return make_response(jsonify({
            "status": "OK",
            "Message": "Product deleted successfully"
        }), 200)


class Users:
    def login(self):
        data = request.get_json()
        if not data or not data["username"] or not data["password"]:
            return jsonify({"Message": "Please enter all credentials"})
        user = [user for user in users if user["name"] == data["username"]]
        if not user:
            return jsonify({"Message": "User does not exist"})
        if check_password_hash(user[0]["password"], data["password"]):
            """generate token"""
            token = jwt.encode({"username": user[0]["name"], 'exp': datetime.datetime.utcnow()
                                                                    + datetime.timedelta(minutes=3)}, app.config["SECRET_KEY"])

            return jsonify({"Token": token.decode('UTF-8')})

        return jsonify({"Message": "Invalid credentials"})

    def add_user(self):
        data = request.get_json()
        pws = data["password"]
        password = generate_password_hash(pws, method="sha256")

        new_user = {"name": data["username"],
                    "password": password,
                    "Role": data["role"]}
        users.append(new_user)
        return jsonify({"Message": "User registered successfully",
                        "Users": users})
