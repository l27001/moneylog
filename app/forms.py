from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username', validators = [DataRequired("Необходимо заполнить все поля")])
    password = PasswordField('password', validators = [DataRequired("Необходимо заполнить все поля")])
    remember_me = BooleanField('remember_me', default = False)
 
