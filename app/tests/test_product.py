import unittest
import json

from app import create_app


class TestProducts(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True
        self.data = {"product_name": "Jesma",
                     "description": "Good book",
                     "quantity": 100,
                     "price": 100
                     }
        self.error_data = {"product_name": "Jesma",
                           "description": "Good book",
                           "quantity": 100,
                           "price": "dkls"
                           }

    def test_get_all_items(self):
        """TEST API can return all products in the list"""
        response = self.app.get('/api/v1/users/products', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        """TEST API can add product to list properly"""
        response = self.app.post('/api/v1/users/products', data=json.dumps(self.data), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], "Product added successfully")
        self.assertEqual(response.status_code, 201)
