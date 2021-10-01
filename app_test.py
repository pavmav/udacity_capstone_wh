import os
import unittest
import json

from flask_migrate import heads

from app import app
from models import db, Warehouse, Item, BalanceJournal
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME_TEST, MANAGER_TOKEN

database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_TEST}'

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_TEST}'
        self.db = db
        
        # binds the app to the current context
        self.db.init_app(app)
        self.app.app_context().push()
        # create all tables
        self.db.create_all()

        self.manager_token = MANAGER_TOKEN
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }


    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_check_health(self):
        res = self.client().get('/', headers=self.headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'Healthy')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


