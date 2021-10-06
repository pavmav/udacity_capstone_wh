import os
import unittest
import json

from flask_migrate import heads

from app import app, patch_warehouse
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

    ### ENDPOINTS TESTS
    def test_check_health(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'Healthy')

    ### CREATE ENTITIES
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

    ### GET ENTITIES
    def test_get_warehouses_success(self):
        # create warehouse for operation
        new_wh = Warehouse()
        new_wh.id = 1
        new_wh.name = 'Test warehouse'
        new_wh.overdraft_control = True
        new_wh.insert()

        model_dict = {
        "success": True, 
        "warehouses": [
                {
                "id": 1, 
                "name": "Test warehouse", 
                "overdraft_control": True
                }
            ]
        }

        res = self.client().get('/warehouses')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, model_dict)

        new_wh.delete()

    def test_get_warehouses_failure(self):

        res = self.client().put('/warehouses')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_items_success(self):
        # create item for operation
        new_item = Item()
        new_item.id = 1
        new_item.name = 'Test item'
        new_item.volume = 2
        new_item.insert()

        model_dict = {
        "success": True, 
        "items": [
                {
                "id": 1, 
                "name": "Test item", 
                "volume": 2
                }
            ]
        }

        res = self.client().get('/items')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, model_dict)

        new_item.delete()

    def test_get_items_failure(self):

        res = self.client().put('/items')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

    ### PATCH ENTITIES
    def test_patch_warehouse_success(self):
        # create warehouse to patch
        new_wh = Warehouse()
        new_wh.id = 1
        new_wh.name = 'Test warehouse'
        new_wh.overdraft_control = True
        new_wh.insert()

        patch_warehouse_json = {
            'name': 'Warehouse 1',
            'overdraft_control': False
        }

        res = self.client().patch('/warehouses/1', headers=self.manager_headers, json=patch_warehouse_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        wh = Warehouse.query.get(1)

        self.assertEqual(wh.name, 'Warehouse 1')
        self.assertEqual(wh.overdraft_control, False)     

    def test_patch_warehouse_failure(self):

        patch_warehouse_json = {
            'name': 'Warehouse 1',
            'overdraft_control': False
        }

        res = self.client().patch('/warehouses/1', headers=self.manager_headers, json=patch_warehouse_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_patch_item_success(self):
        # create item to patch
        new_item = Item()
        new_item.id = 1
        new_item.name = 'Test item'
        new_item.volume = 1
        new_item.insert()

        patch_item_json = {
            'name': 'Item 1',
            'volume': 2
        }

        res = self.client().patch('/items/1', headers=self.manager_headers, json=patch_item_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        item = Item.query.get(1)

        self.assertEqual(item.name, 'Item 1')
        self.assertEqual(item.volume, 2)  

    def test_patch_item_failure(self):

        patch_item_json = {
            'name': 'Item 1',
            'value': 2
        }

        res = self.client().patch('/items/1', headers=self.manager_headers, json=patch_item_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    ### DELETE ENTITIES
    def test_delete_warehouse_success(self):
        # create wawrehouse to patch
        new_wh = Warehouse()
        new_wh.id = 1
        new_wh.name = 'Test warehouse'
        new_wh.overdraft_control = True
        new_wh.insert()

        res = self.client().delete('/warehouses/1', headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        wh = Warehouse.query.get(1)

        self.assertIsNone(wh)

    def test_delete_warehouse_failure(self):

        res = self.client().delete('/warehouses/1', headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_item_success(self):
        # create item to patch
        new_item = Item()
        new_item.id = 1
        new_item.name = 'Test item'
        new_item.volume = 1
        new_item.insert()

        res = self.client().delete('/items/1', headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        item = Item.query.get(1)

        self.assertIsNone(item)

    def test_delete_item_failure(self):

        res = self.client().delete('/items/1', headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    ### POST BALANCE OPERATION
    def test_post_balance_operation_success(self):
        # create warehouse for operation
        new_wh = Warehouse()
        new_wh.id = 1
        new_wh.name = 'Test warehouse'
        new_wh.overdraft_control = True
        new_wh.insert()

        # create item for operation
        new_item = Item()
        new_item.id = 1
        new_item.name = 'Test item'
        new_item.volume = 1
        new_item.insert()

        # json of operation
        balance_operation_json = {
            'warehouse_id': 1,
            'item_id': 1,
            'quantity': 10
        }
        
        res = self.client().post('/balances', headers=self.manager_headers, json=balance_operation_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['new_balance'], 10)

        res = self.client().post('/balances', headers=self.manager_headers, json=balance_operation_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['new_balance'], 20)

        entry = BalanceJournal.query.get((1, 1))

        self.assertEqual(entry.quantity, 20)

        entry.delete()
        Warehouse.query.get(1).delete()
        Item.query.get(1).delete()

    def test_post_balance_operation_failure(self):
        # create warehouse for operation
        new_wh = Warehouse()
        new_wh.id = 1
        new_wh.name = 'Test warehouse'
        new_wh.overdraft_control = True
        new_wh.insert()

        # create item for operation
        new_item = Item()
        new_item.id = 1
        new_item.name = 'Test item'
        new_item.volume = 1
        new_item.insert()

        # json of operation
        balance_operation_json = {
            'warehouse_id': 1,
            'item_id': 1,
            'quantity': -10
        }
        
        res = self.client().post('/balances', headers=self.manager_headers, json=balance_operation_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        
        Warehouse.query.get(1).delete()
        Item.query.get(1).delete()
    
    ### GET BALANCE
    def test_get_balance_success(self):

        # create warehouse for operation
        new_wh = Warehouse()
        new_wh.id = 1
        new_wh.name = 'Test warehouse'
        new_wh.overdraft_control = True
        new_wh.insert()

        # create item for operation
        new_item = Item()
        new_item.id = 1
        new_item.name = 'Test item'
        new_item.volume = 2
        new_item.insert()

        # create balance
        entry = BalanceJournal()
        entry.warehouse_id = 1
        entry.item_id = 1
        entry.quantity = 43
        entry.insert()

        model_dict = {
            "balances": [
                {
                    "item": {
                        "id": 1,
                        "name": "Test item",
                        "volume": 2
                    },
                    "quantity": 43,
                    "volume": 86,
                    "warehouse": {
                        "id": 1,
                        "name": "Test warehouse",
                        "overdraft_control": True
                    }
                }
            ],
            "success": True
        }

        res = self.client().get('/balances', headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, model_dict)

        BalanceJournal.query.get((1,1)).delete()
        Warehouse.query.get(1).delete()
        Item.query.get(1).delete()

    def test_get_balance_failure(self):

        res = self.client().put('/balances')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

    #### RBAC TESTS
    def test_manager_post_warehouse_success(self):
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

    def test_manager_post_warehouse_failure(self):
        warehouse_name = 'Test warehouse'

        new_warehouse_json = {
            'name': warehouse_name,
            'overdraft_control': True
        }

        res = self.client().post('/warehouses', headers=self.user_headers, json=new_warehouse_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_user_post_balance_success(self):
        # create warehouse for operation
        new_wh = Warehouse()
        new_wh.id = 1
        new_wh.name = 'Test warehouse'
        new_wh.overdraft_control = True
        new_wh.insert()

        # create item for operation
        new_item = Item()
        new_item.id = 1
        new_item.name = 'Test item'
        new_item.volume = 1
        new_item.insert()

        # json of operation
        balance_operation_json = {
            'warehouse_id': 1,
            'item_id': 1,
            'quantity': 10
        }
        
        res = self.client().post('/balances', headers=self.user_headers, json=balance_operation_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['new_balance'], 10)

        res = self.client().post('/balances', headers=self.user_headers, json=balance_operation_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['new_balance'], 20)

        entry = BalanceJournal.query.get((1, 1))

        self.assertEqual(entry.quantity, 20)

        entry.delete()
        Warehouse.query.get(1).delete()
        Item.query.get(1).delete()

    def test_user_post_item_failure(self):
        item_name = 'Test item'

        new_item_json = {
            'name': item_name,
            'volume': 1
        }

        res = self.client().post('/items', headers=self.user_headers, json=new_item_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()


