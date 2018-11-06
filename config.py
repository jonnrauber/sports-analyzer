import os

SECRET_KEY = os.environ['SECRET_KEY']
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
