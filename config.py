import os.path 
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = "DSIN"