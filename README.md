# Udacity capstone warehouse

This project is a simple backend warehouse engine. Users can create warehouses, items, perform warehouse operations and see the balances of items in warehouses.

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
- Sample: `curl --location --request POST 'https://udacity-capstone-warehouse.herokuapp.com/warehouses' --header 'Authorization: Bearer MANAGER_TOKEN' --header 'Content-Type: application/json' --data-raw '{"name":"Backyard",
"overdraft_control":true}'`
  
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
- Sample: `curl --location --request POST 'https://udacity-capstone-warehouse.herokuapp.com/items' --header 'Authorization: Bearer MANAGER_TOKEN' --header 'Content-Type: application/json' --data-raw '{"name":"Pickled tomatoes 3l jar",
"volume":3}'`
  
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

#### GET /categories/{category_id}/questions
- General:
    - Returns a list of questions objects in a category with id=category_id, categories, current category and total number of questions
- Sample: `curl localhost:5000/categories/1/questions`

``` 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Me", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "Who?"
    }, 
    {
      "answer": "Bar!", 
      "category": 1, 
      "difficulty": 5, 
      "id": 30, 
      "question": "Foo?"
    }
  ], 
  "total_questions": 5
} 
```
#### POST /quizzes
- General:
    - Returns question object based on submitted information: category and IDs of the questions, that already were asked. 
- Sample: `curl -X POST localhost:5000/quizzes -H "Content-Type: application/json" --data '{"previous_questions":[20], "quiz_category": {"type":"Science", "id":"0"}}'`
  
```
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }
}
```
#### GET /questions?page=page_number
- General:
    - Returns a list of questions objects, categories, current category (default=null) and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl localhost:5000/questions?page=2`

``` 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Me", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "Who?"
    }, 
    {
      "answer": "Because I can", 
      "category": 2, 
      "difficulty": 4, 
      "id": 28, 
      "question": "Why?"
    }
  ], 
  "total_questions": 21
}  
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. 
- Sample: `curl -X DELETE localhost:5000/questions/29`
```
{
  "success": true
}
```

## Deployment N/A

## Authors
Udacity team and Pavel Mavrichev

## Acknowledgements 
Udacity team and Coach Caryn!