import os

from sayhello import app

db = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path) + '/sayhello', 'data.db')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', db)
