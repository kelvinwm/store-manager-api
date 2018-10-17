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
                     "price": 1500
                     }
        self.err_data = {"product_name": "Jesma",
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

    def test_invalid_add_product(self):
        """TEST API can add product to list properly"""
        response = self.app.post('/api/v1/users/products', data=json.dumps( self.err_data), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {'message': {'price': 'No price provided'}})

    def test_get_one_product(self):
        """TEST API can get a single product"""
        result = self.app.get('/api/v1/users/products/1', content_type='application/json')
        self.assertEqual(result.status_code, 200)
        result = self.app.get('/api/v1/users/products/11', content_type='application/json')
        self.assertEqual(result.status_code, 404)

    def test_product_list_can_be_edited(self):
        """TEST API can edit existing product list"""
        result = self.app.put('/api/v1/users/products/1', data=json.dumps(self.data), content_type="application/json")
        self.assertEqual(result.status_code, 200)
        res = self.app.put('/api/v1/users/products/12', data=json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 404)

    # def test_product_list_deletion(self):
    #     """TEST API can delete existing product list item"""
    #     result = self.app.delete('/api/v1/users/products/1', data=json.dumps(self.data),
    #                              content_type="application/json")
    #     self.assertEqual(result.status_code, 200)
    #     res = self.app.get('/api/v1/users/products/1', data=json.dumps(self.data), content_type="application/json")
    #     self.assertEqual(res.status_code, 404)
