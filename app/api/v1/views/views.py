from flask_restful import Resource, reqparse
from app.api.v1.models import Products

product = Products()
# sale = Sales()
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


