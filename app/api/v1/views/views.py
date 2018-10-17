from flask_restful import Resource, reqparse
from app.api.v1.models import Products, Sales

product = Products()

sale = Sales()
# cart = Cart()


class Products(Resource):
    """get all Products or post a product to the products list"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("product_name", required=True, help="No product name provided", location=['json'])
        self.parser.add_argument("price", required=True, type=int, help="No price provided", location=['json'])
        self.parser.add_argument("description", required=True, help="No price provided", location=['json'])
        self.parser.add_argument("quantity", required=True, type=int, help="No quantity provided", location=['json'])
        super().__init__()

    def get(self):
        """get all Products from products list"""
        return product.get_all_products()

    def post(self):
        """Add a product to the products list"""
        args = self.parser.parse_args()
        return product.add_product(**args)


class Product(Resource):
    """get or update or delete a single product from the products list """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("product_name", required=True, help="No product name provided", location=['json'])
        self.parser.add_argument("price", required=True, type=int, help="No price provided", location=['json'])
        self.parser.add_argument("description", required=True, help="No price provided", location=['json'])
        self.parser.add_argument("quantity", required=True, type=int, help="No quantity provided", location=['json'])
        super().__init__()

    def get(self, product_id):
        """get a single product from the products list """
        return product.get_one_product(product_id)

    def put(self, product_id):
        """update a single product from the products list """
        args = self.parser.parse_args()
        return product.update_product(product_id, **args)

    def delete(self, product_id):
        """delete a single product from the products list """
        return product.delete_product(product_id)

class Sales(Resource):
    """Sales """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("attendant_name", required=True, help="No product name provided", location=['json'])
        self.parser.add_argument("product_name", required=True, help="No product name provided", location=['json'])
        self.parser.add_argument("price", required=True, type=int, help="No price provided", location=['json'])
        self.parser.add_argument("total_price", required=True, type=int, help="No price provided", location=['json'])
        self.parser.add_argument("quantity", required=True, type=int, help="No quantity provided", location=['json'])
        self.parser.add_argument("date", required=True, help="No quantity provided", location=['json'])
        super().__init__()

    def get(self):
        """get all sales from all_sales list """
        return sale.get_all_sales()