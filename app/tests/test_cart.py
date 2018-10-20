import unittest
import json

from app import create_app


class TestCart(unittest.TestCase):
    """TEST CLASS FOR CART API ENDPOINTS"""
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True
        self.data = {
            "date": "12/12/2018",
            "price": 10001,
            "product_name": "Ata ichelewe",
            "quantity": 5,
            "sale_id": 1,
            "total_price": 1500}
        self.sign_up_data = {"username": "admin",
                             "password": "1234",
                             "role": "admin"
                             }
        self.login_data = {"username": "admin",
                           "password": "1234"
                           }
        response = self.app.post('/api/v1/users/signup', data=json.dumps(self.sign_up_data),
                                 content_type='application/json')
        self.result = self.app.post('/api/v1/users/login', data=json.dumps(self.login_data),
                                    content_type='application/json')
        self.token = json.loads(self.result.data.decode('utf-8'))["Token"]
        self.headers = {'content-type': 'application/json', 'access-token': self.token}

    def test_get_all_cart_items(self):
        """TEST API can return all cart items in the cart list"""
        response = self.app.get('/api/v1/users/cart', headers= self.headers)
        self.assertEqual(response.status_code, 200)

    def test_add_item_to_cart_list(self):
        """TEST API can add item to cart list"""
        response = self.app.post('/api/v1/users/cart', data=json.dumps(self.data), headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_sale_record_deletion(self):
        """TEST API can delete existing cart item"""
        result = self.app.delete('/api/v1/users/cart/1', data=json.dumps(self.data), headers=self.headers)
        self.assertEqual(result.status_code, 200)
