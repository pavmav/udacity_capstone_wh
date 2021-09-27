# gunicorn -w 4 app:app --access-logfile -

from flask import Flask, request, abort, jsonify
from models import db, Warehouse, Item, BalanceJournal
import sys

app = Flask(__name__)

app.config.from_object('config')
db.init_app(app)
app.app_context().push()

db.create_all()

# HEALTH CHECK
@app.route("/")
def hello():
    return "Healthy"

# CREATE ENTITIES
@app.route("/warehouses", methods=['POST'])
def add_warehouse():
    
    # get posted json object
    wh_data = request.get_json()

    try:
        new_wh = Warehouse()
        new_wh.name = wh_data['name']
        if 'overdraft_control' in wh_data:
            new_wh.overdraft_control = wh_data['overdraft_control']
        new_wh.insert()

        return jsonify({
            'success': True,
            'new_wh': new_wh.format()
        })

    except:
        print(sys.exc_info())
        abort(400)

@app.route("/items", methods=['POST'])
def add_item():
    
    # get posted json object
    item_data = request.get_json()

    try:
        new_item = Item()
        new_item.name = item_data['name']
        new_item.insert()

        return jsonify({
            'success': True,
            'new_item': new_item.format()
        })

    except:
        print(sys.exc_info())
        abort(400)

# GET ENTITIES
@app.route("/warehouses", methods=['GET'])
def get_warehouses():
    wh_list = [wh.format() for wh in Warehouse.query.all()]

    return jsonify(wh_list)

@app.route("/items", methods=['GET'])
def get_items():
    items_list = [item.format() for item in Item.query.all()]

    return jsonify(items_list)

# DELETE ENTITIES
@app.route("/warehouses/<int:warehouse_id>", methods=['DELETE'])
def delete_warehouse(warehouse_id):

    warehouse = Warehouse.query.get(warehouse_id)

    if warehouse is None:
        abort(404)

    warehouse.delete()

    return jsonify({
        'success': True
    })
    
@app.route("/items/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):

    item = Item.query.get(item_id)

    if item is None:
        abort(404)

    item.delete()

    return jsonify({
        'success': True
    })    

# POST BALANCE OPERATIONS
@app.route("/balances", methods=['POST'])
def post_balance_operation():
    # get posted json object
    operation_data = request.get_json()

    # should have 3 properties:
    #   - warehouse_id: int
    #   - item_id: int
    #   - quantity: int (positives will be added, negatives will be substracted)
    if not ('warehouse_id' in operation_data 
            and 'item_id' in operation_data 
            and 'quantity' in operation_data):
        abort(400)

    warehouse_id = operation_data['warehouse_id']
    item_id = operation_data['item_id']
    quantity = operation_data['quantity']

    bj_entry = BalanceJournal.query.get((warehouse_id, item_id))
    new = False

    # if there are no info in the journal, initiate a new entry
    if bj_entry is None:
        new = True
        bj_entry = BalanceJournal()
        bj_entry.warehouse_id = warehouse_id
        bj_entry.item_id = item_id
        bj_entry.quantity = 0

    bj_entry.quantity = bj_entry.quantity + quantity

    # check for overdraft
    warehouse = Warehouse.query.get(warehouse_id)
    if bj_entry.quantity < 0 and warehouse.overdraft_control:
        abort(400)    

    if new:
        bj_entry.insert()
    else:
        bj_entry.update()

    return jsonify({
        'success': True,
        'new_balance': bj_entry.quantity
    })

# GET BALANCES
@app.route("/balances", methods=['GET'])
def get_all_balances():

    balances_list_raw = BalanceJournal.query.all()

    balances_list = []

    for entry_raw in balances_list_raw:
        warehouse_dict = entry_raw.warehouse.format()
        item_dict = entry_raw.item.format()
        
        entry = {
            'warehouse': warehouse_dict,
            'item': item_dict,
            'quantity': entry_raw.quantity
        }

        balances_list.append(entry)

    return jsonify(balances_list)



if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)