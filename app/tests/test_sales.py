import unittest
import json

from app import create_app


class TestSales(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True
        self.data = {"attendant_name": "kampa yeye",
                     "date": "12/12/2018",
                     "price": 10001,
                     "product_name": "Ata ichelewe",
                     "quantity": 5,
                     "sale_id": 1,
                     "total_price": 1500}
        self.data = {"attendant_name": "kampa yeye",
                     "date": "12/12/2018",
                     "price": "",
                     "product_name": "Ata ichelewe",
                     "quantity": 5,
                     "sale_id": 1,
                     "total_price": 1500}

    def test_get_all_sale_records(self):
        """TEST API can return all sales in the sales record list"""
        response = self.app.get('/api/v1/users/sales', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # def test_add_sale_record(self):
    #     """TEST API can add sale record to list properly"""
    #     response = self.app.post('/api/v1/users/sales', data=json.dumps(self.data), content_type="application/json")
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_invalid_add_sale_record(self):
    #     """TEST API can detect sale record with incorrect data"""
    #     response = self.app.post('/api/v1/users/sales', data=json.dumps( self.err_data), content_type="application/json")
    #     result = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(result, {'message': {'price': 'No price provided'}})
    #
    # def test_get_one_sale_record(self):
    #     """TEST API can get a single sales record"""
    #     result = self.app.get('/api/v1/users/sales/1', content_type='application/json')
    #     self.assertEqual(result.status_code, 200)
    #     result = self.app.get('/api/v1/users/sales/9', content_type='application/json')
    #     self.assertEqual(result.status_code, 404)
    #
    # def test_sale_record_can_be_edited(self):
    #     """TEST API can edit existing sale record list"""
    #     result=self.app.put('/api/v1/users/sales/1', data=json.dumps(self.data), content_type="application/json")
    #     self.assertEqual(result.status_code, 200)
    #     res=self.app.put('/api/v1/users/sales/12', data=json.dumps(self.data), content_type="application/json")
    #     self.assertEqual(res.status_code, 404)
    #
    # def test_sale_record_deletion(self):
    #     """TEST API can delete existing sale record"""
    #     result = self.app.delete('/api/v1/users/sales/1', data=json.dumps(self.data), content_type="application/json")
    #     self.assertEqual(result.status_code, 200)
    #     res = self.app.get('/api/v1/users/sales/1', data=json.dumps(self.data),content_type="application/json")
    #     self.assertEqual(res.status_code, 404)
