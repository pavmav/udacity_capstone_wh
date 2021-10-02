import os
import unittest
import json

from flask_migrate import heads

from app import app
from models import db, Warehouse, Item, BalanceJournal
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME_TEST, MANAGER_TOKEN, USER_TOKEN

database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_TEST}'

class WarehouseTestCase(unittest.TestCase):
    
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
        for wh in Warehouse.query.all():
            wh.delete()

        for item in Item.query.all():
            item.delete()

        for entry in BalanceJournal.query.all():
            entry.delete()

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

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        new_wh_dict = data['new_wh']
        new_wh = Warehouse.query.get(new_wh_dict['id'])

        self.assertTrue(not new_wh is None)
        self.assertEqual(new_wh.name, warehouse_name)
        self.assertEqual(new_wh.overdraft_control, True)

        new_wh.delete()

    def test_post_warehouse_failure(self):
        new_warehouse_json = {
            'overdraft_control': True
        }

        res = self.client().post('/warehouses', headers=self.manager_headers, json=new_warehouse_json)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)

    def test_post_item_success(self):
        item_name = 'Test item'

        new_item_json = {
            'name': item_name,
            'volume': 1
        }

        res = self.client().post('/items', headers=self.manager_headers, json=new_item_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        new_item_dict = data['new_item']
        new_item = Item.query.get(new_item_dict['id'])

        self.assertTrue(not new_item is None)
        self.assertEqual(new_item.name, item_name)
        self.assertEqual(new_item.volume, 1)

        new_item.delete()

    def test_post_item_failure(self):
        new_item_json = {
            'volume': True
        }

        res = self.client().post('/items', headers=self.manager_headers, json=new_item_json)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)



        
        






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


