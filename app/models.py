from app import db
import bcrypt
from sqlalchemy.sql import func

ROLE_USER = 0
ROLE_ADMIN = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True, nullable = False)
    password = db.Column(db.String(128), index = True, nullable = False)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER, nullable = False)
    is_active = 1
    is_authenticated = 1
    is_anonymous = 0

    def __repr__(self):
        return '<User %r>' % (self.username)

    def get_id(self): return self.id

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        # db.session.commit()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())

class Group(db.Model):
    id = db.Column(db.SmallInteger, primary_key = True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128), nullable = False)

    def __repr__(self):
        return '<Group %r>' % (self.name)

class MoneyLog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    group_id = db.Column(db.SmallInteger, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cost = db.Column(db.Integer, index = True)
    timestamp = db.Column(db.Date(), index = True, default=func.now())
    description = db.Column(db.String(128), default='', nullable = False)

    def __repr__(self):
        return '<Log %r>' % (self.id) 
