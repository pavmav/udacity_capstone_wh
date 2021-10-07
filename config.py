import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'udacity_wh')
DB_NAME_TEST = os.getenv('DB_NAME_TEST', 'udacity_wh_test')

#SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

# fix for Heroku
if SQLALCHEMY_DATABASE_URI[:9] == 'postgres:':
    SQLALCHEMY_DATABASE_URI = 'postrgesql' + SQLALCHEMY_DATABASE_URI[8:]

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE')
MANAGER_TOKEN = os.getenv('MANAGER_TOKEN')
USER_TOKEN = os.getenv('USER_TOKEN')