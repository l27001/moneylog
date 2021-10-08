from flask import render_template, abort, request, redirect, url_for, g, session, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from datetime import datetime
from werkzeug.utils import secure_filename
from random import randint
import os
from app import app, forms, models, db, avatars
from app.decorators import login_not_required

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth'

@lm.unauthorized_handler
def unauthorized():
    if(request.method == "GET"):
        flash("Необходимо авторизоваться", "warning")
        return redirect(url_for('auth'))
    else:
        return {"status":"unauthorized", "description":"Необходимо авторизоваться"}

@lm.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/dashboard')
@login_required
def index():
    return render_template('index.html',
        title = "Главная",
        user = g.user)

@app.route('/log/get', methods=['POST'])
def log_get():
    logs_count = models.MoneyLog.query.filter(models.MoneyLog.user_id == g.user.id).count()
    logs = models.MoneyLog.query.filter(models.MoneyLog.user_id == g.user.id).order_by(models.MoneyLog.timestamp.desc(), models.MoneyLog.id.desc()).all()
    if(logs):
        logs_out = []
        groups = {}
        for n in models.Group.query.all():
            n = n.__dict__
            groups.update({n['id']:n['name']})
        for log in logs:
            try: group = groups[log.group_id]
            except KeyError: group = "Неизвестно"
            logs_out.append([log.timestamp.strftime('%Y-%m-%d'), group, log.description, log.cost, log.id])
    else:
        logs_out = []
    return jsonify(logs_out)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли", "success")
    return redirect(url_for('auth'))

@app.route('/auth', methods=['GET', 'POST'])
@login_not_required
def auth():
    form = forms.LoginForm()
    if(form.validate_on_submit() == True):
        cur_user = models.User.query.filter(or_(models.User.username == form.username.data, models.User.email == form.username.data)).first()
        if(cur_user and cur_user.check_password(form.password.data) == True):
            login_user(load_user(cur_user.id), remember=form.remember_me.data)
            flash("Вы успешно авторизовались", "success")
            return redirect(url_for('index'))
        else:
            flash("Неверный логин или пароль", "danger")
    return render_template('auth.html',
        title = "Вход",
        form = form,
        user = g.user)

@app.route('/register', methods=['GET', 'POST'])
@login_not_required
def register():
    form = forms.RegisterForm()
    if(form.validate_on_submit() == True):
        if(models.User.query.filter(or_(models.User.username == form.username.data, models.User.email == form.email.data)).first() is not None):
            flash("Пользователь с таким именем или email уже зарегистрирован", "danger")
        else:
            user = models.User(username = form.username.data, email = form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(load_user(user.id), remember=True)
            return redirect(url_for('index'))
    return render_template('register.html',
        title = "Регистрация",
        form = form,
        user = g.user)

@app.route('/log/add', methods=['GET', 'POST'])
@login_required
def log_add():
    form = forms.LogAdd()
    groups = [(n.id, n.name) for n in models.Group.query.all()]
    form.group.choices = groups
    if(form.validate_on_submit() == True):
        add = models.MoneyLog(cost = form.cost.data,
            description = form.description.data,
            group_id = form.group.data,
            user_id = g.user.id,
            timestamp = form.date.data)
        if(form.balance.data == True):
            g.user.balance += form.cost.data
            if(g.user.balance < 0): g.user.balance = 0
        db.session.add(add)
        db.session.commit()
        flash("Запись успешно добавлена" ,"success")
        return redirect(url_for('index'))
    form.date.data = datetime.now()
    return render_template("log/add.html",
        title = "Добавить запись",
        form = form,
        user = g.user)

@app.route('/log/delete', methods=['POST'])
@login_required
def log_del():
    id_ = request.form.get('id')
    d = models.MoneyLog.query.filter(models.MoneyLog.user_id == g.user.id, models.MoneyLog.id == id_).first_or_404()
    if(d):
        db.session.delete(d)
        db.session.commit()
        return {"status":"success"}
    else:
        return {"status":"fail", "description":"Запись не найдена"}

@app.route('/log/edit/<int:id_>', methods=['GET' ,'POST'])
@login_required
def log_edit(id_):
    item = models.MoneyLog.query.filter(models.MoneyLog.user_id == g.user.id, models.MoneyLog.id == id_).first_or_404()
    form = forms.LogAdd()
    groups = [(n.id, n.name) for n in models.Group.query.all()]
    form.group.choices = groups
    if(form.validate_on_submit() == True):
        item.group_id = form.group.data
        item.cost = form.cost.data
        item.description = form.description.data
        item.timestamp = form.date.data
        db.session.commit()
        flash("Запись успешно сохранена" ,"success")
        return redirect(url_for('index'))
    form.group.data = item.group_id
    form.cost.data = item.cost
    form.description.data = item.description
    form.date.data = item.timestamp
    return render_template("log/edit.html",
        title = "Редактировать запись",
        form = form,
        user = g.user)

@app.route('/profile/avatar/<path:filename>')
@login_required
def get_avatar(filename):
    return send_from_directory(app.config['AVATARS_SAVE_PATH'], filename)

@app.route('/profile/balance', methods=['POST'])
@login_required
def user_balance_edit():
    balance = request.form.get('balance')
    try: balance = int(balance)
    except ValueError: abort(400)
    if(balance is None): abort(400)
    if(balance < 0):
        return {"status": "fail", "description": "Сумма не может быть меньше 0"}, 200
    old_balance = g.user.balance
    g.user.balance = balance
    add = models.MoneyLog(group_id = 0, user_id = g.user.id, cost = balance-old_balance, description = "Изменение баланса")
    db.session.add(add)
    db.session.commit()
    return {"status": "success"}, 200

@app.route('/profile/avatar/crop', methods=['GET', 'POST'])
@login_required
def avatar_crop():
    form = forms.CropAvatarForm()
    if(session.get('avatar_') is None):
        return redirect(url_for('profile'))
    if(form.validate_on_submit() == True):
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        filenames = avatars.crop_avatar(session['avatar_'], x, y, w, h)
        os.remove(app.config['AVATARS_SAVE_PATH'] + "/" + session['avatar_'])
        session.pop('avatar_')
        if(g.user.avatar != None):
            for n in ['s', 'm', 'l']:
                a = g.user.avatar.split('_')
                try:
                    os.remove(app.config['AVATARS_SAVE_PATH'] + "/" + a[0] + "_" + n + a[1][1:])
                except FileNotFoundError:
                    pass
        g.user.avatar = filenames[2]
        db.session.commit()
        flash('Аватар обновлён' ,"success")
        return redirect(url_for('profile'))
    return render_template('profile/avatar_crop.html',
        user = g.user,
        form = form,
        title = "Обрезать аватар")

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = forms.UploadAvatarForm()
    if(form.validate_on_submit() == True):
        if(os.path.isdir(app.config['AVATARS_SAVE_PATH']) == False):
            os.mkdir(app.config['AVATARS_SAVE_PATH'])
        if('file' not in request.files):
            form.file.errors.append("Некорректный файл")
        file = request.files['file']
        if(file.filename == ''):
            form.file.errors.append("Не выбран файл")
        elif(file.filename.split('.')[-1].lower() in app.config['ALLOWED_FILE_EXTENSIONS']):
            session['avatar_'] = avatars.save_avatar(file)
            return redirect(url_for('avatar_crop'))
    return render_template("profile.html",
        title = "Профиль",
        user = g.user,
        form = form)

@app.route('/profile/changepass', methods=['GET', 'POST'])
@login_required
def profile_changepass():
    form = forms.ProfileChangepass()
    if(form.validate_on_submit() == True):
        if(g.user.check_password(form.cur_password.data) != True):
            form.cur_password.errors.append("Текущий пароль введён неверно")
        elif(form.cur_password.data == form.new_password.data):
            form.new_password.errors.append("Новый пароль должен отличаться от старого")
        else:
            g.user.set_password(form.new_password.data)
            flash("Пароль успешно изменён", "success")
            return redirect(url_for('index'))
    return render_template("/profile/changepass.html",
        title = "Смена пароля",
        form = form,
        user = g.user)

@app.route('/profile/delete')
@login_required
def profile_delete():
    d = models.MoneyLog.query.filter(models.MoneyLog.user_id == g.user.id).all()
    for n in d:
        db.session.delete(n)
    if(g.user.avatar):
        for n in ['s', 'm', 'l']:
            a = g.user.avatar.split('_')
            try:
                os.remove(app.config['AVATARS_SAVE_PATH'] + "/" + a[0] + "_" + n + a[1][1:])
            except FileNotFoundError:
                pass
    user = models.User.query.filter(models.User.id == g.user.id).first()
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash("Аккаунт успешно удалён" ,"success")
    return redirect(url_for('auth'))

@app.route('/profile/change_currency', methods=['POST'])
@login_required
def change_currency():
    currency = request.form['currency']
    if(currency not in g.user.currency_list):
        flash("Валюты нет в списке", "danger")
        return {"status":"fail", "description":"Валюты нет в списке"}
    flash("Валюта изменена", "success")
    if(currency == g.user.currency): return {"status": "success"}
    g.user.currency = currency
    db.session.commit()
    return {"status":"success"}

@app.route('/profile/email/change', methods=['POST'])
@login_required
def change_email():
    form = forms.ChangeEmail()
    if(form.validate_on_submit() != True):
        return {"status":"fail", "description":form.email.errors[0]}
    if(models.User.query.filter(models.User.email == form.email.data).first() != None):
        return {"status":"fail", "description":"Этот email уже занят"}
    else:
        g.user.email = form.email.data
        db.session.commit()
    return {"status":"success"}

