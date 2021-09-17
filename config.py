import os
CSRF_ENABLED = True
SECRET_KEY = '**SECRET_KEY**'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://**USER**:*PASSWORD**@**HOST**/**DB**'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQL_ALCHEMY_POOL_RECYCLE = 50
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_ENGINE_OPTIONS = {'pool_size' : 100, 'pool_recycle' : 50, 'pool_pre_ping': True}