import unittest
import json

from app import create_app


class TestUsersAuth(unittest.TestCase):
    """TEST CLASS FOR AUTHENTICATION API ENDPOINTS"""

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

        self.sign_up_data = {"username": "admin",
                             "password": "1234",
                             "role": "admin"
                             }
        self.invalid_sign_up_data = {"username": "admin",
                                     "password": "1234",
                                     "role": ""
                                     }
        self.login_data = {"username": "admin",
                           "password": "1234"
                           }
        self.empty_login_data = {"username": "admin",
                                 "password": ""
                                 }
        self.invalid_login_data = {"username": "admin",
                                   "password": "0976"
                                   }

    def test_valid_signup(self):
        """TEST API can sign up users correctly"""
        response = self.app.post('/api/v1/auth/signup', data=json.dumps(self.sign_up_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_valid_login(self):
        """TEST API can sign up users correctly"""
        self.result = self.app.post('/api/v1/auth/login', data=json.dumps(self.login_data),
                                    content_type='application/json')
        self.assertEqual(self.result.status_code, 200)

    def test_invalid_signup(self):
        """TEST API can sign up users correctly"""
        response = self.app.post('/api/v1/auth/signup', data=json.dumps(self.invalid_sign_up_data),
                                 content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Please enter all credentials")

    def test_empty_credentials_login(self):
        """TEST API can sign up users correctly"""
        response = self.app.post('/api/v1/auth/login', data=json.dumps(self.empty_login_data),
                                 content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], "Please enter all credentials")

    def test_invalid_login(self):
        """TEST API can sign up users correctly"""
        response = self.app.post('/api/v1/auth/login', data=json.dumps(self.invalid_login_data),
                                 content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["Message"], "Invalid credentials")
