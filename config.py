import os
CSRF_ENABLED = True
SECRET_KEY = '**SECRET_KEY**'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://**USER**:*PASSWORD**@**HOST**/**DB**'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False