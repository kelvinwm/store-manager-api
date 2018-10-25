import unittest
import json

from app import create_app


class TestSales(unittest.TestCase):
    """TEST CLASS FOR SALES API ENDPOINTS"""

    def setUp(self):
        """INITIALIZATION """
        self.app = create_app().test_client()
        self.app.testing = True
        self.product = {"product_name": "Jesma",
                        "description": "Good book",
                        "quantity": 100,
                        "price": 1500
                        }
        self.data = {"attendant_name": "kevo",
                     "product_name": "Jesma",
                     "quantity": 1,
                     "price": 200,
                     "total_price": 400
                     }
        self.err_data = {"attendant_name": "kampa yeye",
                         "date": "12/12/2018",
                         "price": "",
                         "product_name": "Ata ichelewe",
                         "quantity": 5,
                         "sale_id": 1,
                         "total_price": 1500}
        self.sign_up_data = {"username": "kevo",
                             "email": "prince@gmail.com",
                             "password": "12A#3dsvs3",
                             "role": "admin"
                             }
        self.login_data = {"username": "kevo",
                           "email": "prince@gmail.com",
                           "password": "12A#3dsvs3"
                           }
        response = self.app.post('/api/v1/auth/signup', data=json.dumps(self.sign_up_data),
                                 content_type='application/json')
        self.result = self.app.post('/api/v1/auth/login', data=json.dumps(self.login_data),
                                    content_type='application/json')
        self.token = json.loads(self.result.data.decode('utf-8'))["Token"]
        self.headers = {'content-type': 'application/json', 'access-token': self.token}

    def test_get_all_sale_records(self):
        """TEST API can return all sales in the sales record list"""
        response = self.app.get('/api/v1/sales', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_add_sale_record(self):
        """TEST API can add sale record to list properly"""
        response = self.app.post('/api/v1/products', data=json.dumps(self.product), headers=self.headers)
        response = self.app.post('/api/v1/sales', data=json.dumps(self.data), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], 'Product added successfully')
        self.assertEqual(response.status_code, 201)

    def test_invalid_add_sale_record(self):
        """TEST API can detect sale record with incorrect data"""
        response = self.app.post('/api/v1/sales', data=json.dumps(self.err_data), headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {'message': {'price': 'Invalid entry'}})

    def test_get_one_sale_record(self):
        """TEST API can get a single sales record"""
        result = self.app.get('/api/v1/sales/1', headers=self.headers)
        self.assertEqual(result.status_code, 200)
        response = self.app.get('/api/v1/sales/9', headers=self.headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Product"], 'Product not found')

    def test_sale_record_can_be_edited(self):
        """TEST API can edit existing sale record list"""
        result = self.app.put('/api/v1/sales/1', data=json.dumps(self.data), headers=self.headers)
        self.assertEqual(result.status_code, 200)
        res = self.app.put('/api/v1/sales/12', data=json.dumps(self.data), headers=self.headers)
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result, {'Message': 'Product not found', 'status': 'OK'})

    def test_sale_record_deletion(self):
        """TEST API can delete existing sale record"""
        result = self.app.delete('/api/v1/sales/1', data=json.dumps(self.data), headers=self.headers)
        self.assertEqual(result.status_code, 200)
        res = self.app.get('/api/v1/sales/1', data=json.dumps(self.data), headers=self.headers)
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result, {'Product': 'Product not found', 'status': 'OK'})
