import os
CSRF_ENABLED = True
SECRET_KEY = '**SECRET_KEY**'
JSON_SORT_KEYS = False

basedir = os.path.abspath(os.path.dirname(__file__))
GROUPS = {0: 'Без группы',
        1: 'Товары для дома',
        2: 'Продукты',
        3: 'Рестораны и кафе',
        4: 'Коммунальные платежи',
        5: 'Транспорт',
        6: 'Интернет магазины',
        7: 'Доход',
        8: 'Связь/интернет',
        9: 'Подписки',
        10: 'Прочее'}

SQLALCHEMY_DATABASE_URI = 'mysql://**USER**:*PASSWORD**@**HOST**/**DB**'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQL_ALCHEMY_POOL_RECYCLE = 50
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_ENGINE_OPTIONS = {'pool_size' : 100, 'pool_recycle' : 50, 'pool_pre_ping': True}
### Set True only on HTTPS
REMEMBER_COOKIE_SECURE = True
REMEMBER_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
###
REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True
SESSION_PROTECTION = "basic"
MAX_CONTENT_LENGTH = 50 * 1024 * 1024
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
AVATARS_SAVE_PATH = DIR_PATH + "/app/static/avatars"
AVATARS_SIZE_TUPLE = [30, 90, 180]
AVATARS_CROP_INIT_SIZE = 180
ALLOWED_FILE_EXTENSIONS = ['png', 'jpg', 'jpeg']
