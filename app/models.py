from app import db, app
import bcrypt, os
from sqlalchemy.sql import func
from glob import glob

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True, nullable = False)
    password = db.Column(db.String(64), index = True, nullable = False)
    email = db.Column(db.String(120), index = True, unique = True)
    balance = db.Column(db.BigInteger, default = 0, nullable = False)
    registered = db.Column(db.Date(), default = func.now(), nullable = False)
    avatar = db.Column(db.String(64))
    currency = db.Column(db.String(4), default = '₽')
    logs = db.relationship('MoneyLog', backref = 'user', lazy = 'dynamic', cascade = "all,delete")
    is_active = True
    is_authenticated = True
    is_anonymous = False
    currency_list = ['₽', '$', '€', '£', '¥']

    def __repr__(self):
        return '<User %r>' % (self.username)

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def get_avatar_link(self, size = "m"):
        if(self.avatar == None):
            return f"/static/avatars/default_{size}.png"
        else:
            return f"/static/avatars/{self.avatar}{size}.png"

    def delete_avatar(self, update = False):
        for file in glob(app.config['AVATARS_SAVE_PATH'] + '/' + self.avatar + '*'):
            os.remove(file)
        if(update):
            self.avatar = None

class Group(db.Model):
    id = db.Column(db.SmallInteger, primary_key = True)
    name = db.Column(db.String(128), nullable = False)
    logs = db.relationship('MoneyLog', backref = db.backref('group', lazy='select'), uselist=False)

    def __repr__(self):
        return '<Group %r>' % (self.name)

class MoneyLog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    group_id = db.Column(db.SmallInteger, db.ForeignKey('group.id'), index = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True, nullable = False)
    cost = db.Column(db.BigInteger, nullable = False)
    timestamp = db.Column(db.Date(), index = True, default=func.now(), nullable = False)
    description = db.Column(db.String(128), default='', nullable = False)

    def __repr__(self):
        return '<Log %r>' % (self.id) 
