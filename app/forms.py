from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField, PasswordField, SelectField, IntegerField, DateField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, Email
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import app

class LoginForm(Form):
    username = StringField('username',
        validators = [DataRequired("Необходимо заполнить все поля")])
    password = PasswordField('password',
        validators = [DataRequired("Необходимо заполнить все поля")])
    remember_me = BooleanField('remember_me',
        default = False)

class RegisterForm(Form):
    username = StringField('username',
        validators = [DataRequired("Необходимо заполнить все поля"),
            Length(4,32,"Логин должен содержать от 4 до 32 символов"),
            Regexp("^[A-Za-z_\-0-9]+$",0,"Логин может содержать только латинские буквы, цифры и символы - и _")])
    email = StringField('email',
        validators = [DataRequired("Необходимо заполнить все поля"),
            Email("Введён некорректный email"),
            Length(0,120,"Email должен содержать не более 120 символов")])
    password = PasswordField('password',
        validators = [DataRequired("Заполните все поля"),
            Length(6,64,"Пароль должен содержать от 6 до 64 символов")])
    password2 = PasswordField('password2',
        validators = [DataRequired("Заполните все поля"),
            EqualTo("password", "Пароли должны совпадать")])

class LogAdd(Form):
    cost = IntegerField('cost',
        validators = [DataRequired("Некорректное значение")])
    description = StringField('description',
        validators = [Length(0,128,"Максимальная длина пояснения 128 символов")],
        widget=TextArea())
    group = SelectField('group',
        coerce=int)
    balance = BooleanField('balance',
        default = False)
    date = DateField('date',
        format = '%Y-%m-%d',
        validators = [DataRequired("Необходимо ввести корректное значение [yyyy-mm-dd]")])

class ProfileChangepass(Form):
    cur_password = StringField('cur_password',
        validators = [DataRequired("Заполните все поля")],)
    new_password = PasswordField('new_password',
        validators = [DataRequired("Заполните все поля"),
            Length(6,64,"Пароль должен содержать от 6 до 64 символов")])
    new_password2 = PasswordField('new_password2',
        validators = [DataRequired("Заполните все поля"),
            EqualTo("new_password", "Пароли должны совпадать")])

class UploadAvatarForm(Form):
    file = FileField('Upload (<=40M)', validators=[
        FileRequired("Необходимо прикрепить файл"),
        FileAllowed(app.config['ALLOWED_FILE_EXTENSIONS'], 'Поддерживаются только форматы ' + (',').join(app.config['ALLOWED_FILE_EXTENSIONS']))
    ])

class CropAvatarForm(Form):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()

class ChangeEmail(Form):
    class Meta:
        csrf = False

    email = StringField('email',
        validators = [DataRequired("Необходимо заполнить все поля"),
            Email("Введён некорректный email"),
            Length(0,120,"Email должен содержать не более 120 символов")])
