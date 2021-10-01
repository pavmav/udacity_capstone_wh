import os
import unittest
import json

from flask_migrate import heads

from app import app
from models import db, Warehouse, Item, BalanceJournal
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME_TEST, MANAGER_TOKEN, USER_TOKEN

database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_TEST}'

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.client = self.app.test_client
        self.database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_TEST}'
        self.db = db
        
        # binds the app to the current context
        self.db.init_app(app)
        self.app.app_context().push()
        # create all tables
        self.db.create_all()

        self.manager_token = MANAGER_TOKEN
        self.manager_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }
        self.user_token = USER_TOKEN
        self.user_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_check_health(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'Healthy')

    def test_post_warehouse_success(self):
        warehouse_name = 'Test warehouse'

        new_warehouse_json = {
            'name': warehouse_name,
            'overdraft_control': True
        }

        res = self.client().post('/warehouses', headers=self.manager_headers, json=new_warehouse_json)
        data = json.loads(res.data)

        self.assertTrue(data['success'])

        new_wh_dict = data['new_wh']
        new_wh = Warehouse.query.get(new_wh_dict['id'])

        self.assertTrue(not new_wh is None)
        self.assertEqual(new_wh.name, warehouse_name)

        new_wh.delete()



        
        






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


