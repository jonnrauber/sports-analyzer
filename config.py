import os

SECRET_KEY = 'sports'
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/sportsanalyzer'
SQLALCHEMY_TRACK_MODIFICATIONS = False
