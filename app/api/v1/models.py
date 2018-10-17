from flask import make_response, jsonify
# from app.api.v1.utils import Validate
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

        #

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


