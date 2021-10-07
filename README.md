# Udacity capstone warehouse

This project is a simple backend warehouse engine. Users can create warehouses, items, perform warehouse operations and see the balances of items in warehouses.

Data model consists of Warehouses, Items stored in these warehouses and Balances table storing number of every item in warehouse.

Warehouses have name and "overdraft control" control feature. If overdraft control is set to True, then API will not allow operations, that lead to balance of any item in the warehouse be less than 0.

Items have name and volume feature. Volume is not required for every item. If the volume is set, then API will return total volume of item calculated as quantity*volume.

Both Warehouses and Items have "unique" constraint on names. So, API will not allow to create or edit warehouse or item if there already exists warehouse or item with such name.

API is supposed to have thee access levels:
- Authenticated users with role Manager have full access to API: they can create, edit and delete items and warehouses, post balance operations and get all the information.
- Authenticated users with role User can only post balance operations using existing warehouses and items. And also get any information.
- Anyone can get all the information about warehouses, items and balances, that does not require authentification.

As a part of the Fullstack Nanodegree, it serves as a capstone for he whole course. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3 and pip installed on their local machines. Also the project was cteated to work with Postgresql db server, though it should be possible to use other databases with some changes. All the other requirements are in requirements.txt.

#### Database

You will need main database and one more database for tests. The default names are 'udacity_wh' and 'udacity_wh_test'.

You can set DB options through environment variables:
- DB_HOST default: localhost:5432
- DB_USER default: postgres
- DB_PASSWORD default: postgres
- DB_NAME default: udacity_wh
- DB_NAME_TEST default: udacity_wh_test

To set an environment variable run the following command:
```
export VARIABLE=VALUE
```

Production database is supposed to be managed with flask_migrate library. So, for migrations use commands:
```
flask db init
flask db migrate
flask db upgrade
```

For test database all the relations are created during tests, the only requirement is that database with name DB_NAME_TEST exists. After running tests the test database should be empty, but in case something went wrong you can always refresh test db using simple SQL script in the file refresh_test_db.sql

#### Backend

From the project folder run `pip install requirements.txt`. All required packages are included in the requirements file.

The project mostly uses various Flask libraries and SQLAlchemy to interact with database.

You can run the app using command: 
```
python3 app.py
```

Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

### Tests
As some features of the application require authentification, tests require two tokens for two users of roles Manager and User. The tokens should be set as environment variables:
```
export MANAGER_TOKEN=token_of_user_with_manager_role
export MANAGER_user=token_of_user_with_user_role
```

In order to run tests run the following command from the project folder: 

```
python3 app_test.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
- Base URL: At present this app is run at https://udacity-capstone-warehouse.herokuapp.com
- Authentication: Some features of this application require authentication with Auth0 third party authentication. Request authentication headers should be of Bearer Token type.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized request
- 403: Forbidden request
- 404: Resource Not Found
- 405: Method not allowed

### Endpoints 
#### GET /
- General:
    - Just a simple health check
- Authentification: does not require authentification.
- Sample: `curl https://udacity-capstone-warehouse.herokuapp.com/`

``` 
{
    "status": "Healthy",
    "success": true
}
```
#### POST /warehouses (Create warehouse)
- General:
    - Creates a new warehouse using the submitted name and overdraft_control value. Returns the formatted representation of the created warehouse and success value.
- Authentification: requires token for a user with manager role.
- Sample: `curl --location --request POST 'https://udacity-capstone-warehouse.herokuapp.com/warehouses' --header 'Authorization: Bearer MANAGER_TOKEN' --header 'Content-Type: application/json' --data-raw '{"name":"Backyard", "overdraft_control":true}'`
  
```
{
    "new_wh": {
        "id": 3,
        "name": "Backyard",
        "overdraft_control": true
    },
    "success": true
}
```

#### POST /items (Create item)
- General:
    - Creates a new item using the submitted name and volume. Returns the formatted representation of the created item and success value.
- Authentification: requires token for a user with manager role.
- Sample: `curl --location --request POST 'https://udacity-capstone-warehouse.herokuapp.com/items' --header 'Authorization: Bearer MANAGER_TOKEN' --header 'Content-Type: application/json' --data-raw '{"name":"Pickled tomatoes 3l jar", "volume":3}'`
  
```
{
    "new_item": {
        "id": 5,
        "name": "Pickled tomatoes 3l jar",
        "volume": 3
    },
    "success": true
}
```
#### PATCH /warehouses/<int:warehouse_id> (Edit warehouse)
- General:
    - Assigns the warehouse with id=warehouse_id name and/or overdraft control value based on submitted json. Returns the formatted representation of the patched warehouse and success value.
- Authentification: requires token for a user with manager role.
- Sample: `curl --location --request PATCH 'https://udacity-capstone-warehouse.herokuapp.com/warehouses/3' --header 'Authorization: Bearer MANAGER_TOKEN' --header 'Content-Type: application/json' --data-raw '{"overdraft_control": false}'`
```
{
    "warehouse": {
        "id": 3,
        "name": "Balcony",
        "overdraft_control": false
    },
    "success": true
}
```
#### PATCH /items/<int:item_id> (Edit item)
- General:
    - Assigns the item with id=item_id name and/or volume based on submitted json. Returns the formatted representation of the patched item and success value.
- Authentification: requires token for a user with manager role.
- Sample: `curl --location --request PATCH 'https://udacity-capstone-warehouse.herokuapp.com/items/2' --header 'Authorization: Bearer MANAGER_TOKEN' --header 'Content-Type: application/json' --data-raw '{"volume": 3}'`
```
{
    "item": {
        "id": 2,
        "name": "pickled zucchini 3 l.",
        "volume": 3
    },
    "success": true
}
```
#### GET /warehouses (List of existing warehouses)
- General:
    - Returns list of existing warehouses and success value.
- Authentification: does not require authentification.
- Sample: `curl https://udacity-capstone-warehouse.herokuapp.com/warehouses`
``` 
{
    "success": true,
    "warehouses": [
        {
            "id": 1,
            "name": "garage",
            "overdraft_control": true
        },
        {
            "id": 2,
            "name": "Country cabin",
            "overdraft_control": false
        },
        {
            "id": 3,
            "name": "Balcony",
            "overdraft_control": true
        },
        {
            "id": 5,
            "name": "Backyard",
            "overdraft_control": true
        }
    ]
}
```
#### GET /items (List of existing items)
- General:
    - Returns list of existing items and success value.
- Authentification: does not require authentification.
- Sample: `curl https://udacity-capstone-warehouse.herokuapp.com/items`
``` 
{
    "items": [
        {
            "id": 1,
            "name": "pickled tomatoes 3 l.",
            "volume": 3
        },
        {
            "id": 2,
            "name": "pickled zucchini 3 l.",
            "volume": 3
        },
        {
            "id": 3,
            "name": "pickled cucumber 2 l.",
            "volume": 2
        },
        {
            "id": 4,
            "name": "winter tires",
            "volume": 0
        },
        {
            "id": 5,
            "name": "shovel",
            "volume": 0
        }
    ],
    "success": true
}
```
#### DELETE /warehouses/<int:warehouse_id> (Delete warehouse)
- General:
    - Deletes the warehouse with id=warehouse_id and returns the success value.
- Authentification: requires token for a user with manager role.
- Sample: `curl --location --request DELETE 'https://udacity-capstone-warehouse.herokuapp.com/warehouses/3' --header 'Authorization: Bearer MANAGER_TOKEN'`
```
{
    "success": true
}
```
#### DELETE /items/<int:item_id> (Delete item)
- General:
    - Deletes the item with id=item_id and returns the success value.
- Authentification: requires token for a user with manager role.
- Sample: `curl --location --request DELETE 'https://udacity-capstone-warehouse.herokuapp.com/item/2' --header 'Authorization: Bearer MANAGER_TOKEN'`
```
{
    "success": true
}
```
#### POST /balances (Create balance operation)
- General:
    - Changes items balance based on the submitted information on how many items should be added or substracted from the balance of ceratin warehouse. Returns the new balance of submitted item in the submitted warehouse and success value.
- Authentification: requires token for a user with manager or user role.
- Sample: `curl --location --request POST 'https://udacity-capstone-warehouse.herokuapp.com/balances' --header 'Authorization: Bearer MANAGER_TOKEN' --header 'Content-Type: application/json' --data-raw '{"warehouse_id":3, "item_id":4,"quantity":-5}'`
  
```
{
    "new_balance": 17,
    "success": true
}
```
#### GET /balances (List of all balances of items in warehouses)
- General:
    - Returns list of all the balances of all the items in all the warehouses.
- Authentification: does not require authentification.
- Sample: `curl https://udacity-capstone-warehouse.herokuapp.com/balances`
``` 
{
    "balances": [
        {
            "item": {
                "id": 4,
                "name": "winter tires",
                "volume": 1
            },
            "quantity": 17,
            "volume": 17,
            "warehouse": {
                "id": 3,
                "name": "Balcony",
                "overdraft_control": true
            }
        },
        {
            "item": {
                "id": 3,
                "name": "pickled cucumber 2 l.",
                "volume": 2
            },
            "quantity": 5,
            "volume": 10,
            "warehouse": {
                "id": 2,
                "name": "Country cabin",
                "overdraft_control": false
            }
        }
    ],
    "success": true
}
```
## Authors
Pavel Mavrichev

## Acknowledgements 
Udacity team