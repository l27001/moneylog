from flask import render_template, abort, request, redirect, url_for, g, session, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app import app, forms, models, db
from sqlalchemy import or_

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth'

@lm.unauthorized_handler
def unauthorized():
    if(request.method == "GET"):
        return redirect(url_for('auth'))
    else:
        return {"status":"unauthorized", "desc":"Необходимо авторизоваться"}

@lm.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
# @login_required
def index():
    if(g.user.is_authenticated):
        logs = models.MoneyLog.query.filter(models.MoneyLog.user_id == g.user.id).order_by(models.MoneyLog.timestamp.desc(), models.MoneyLog.id.desc()).all()
        groups = {}
        for n in models.Group.query.all():
            n = n.__dict__
            groups.update({n['id']:[n['name'], n['description']]})
    else:
        logs = None
        groups = None
    return render_template('index.html',
        title = "Index page",
        user = g.user,
        logs = logs,
        groups = groups)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли", "success")
    return redirect(url_for('index'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if(g.user is not None and g.user.is_authenticated): return redirect(url_for('index'))
    form = forms.LoginForm()
    if(form.validate_on_submit() == True):
        cur_user = models.User.query.filter(or_(models.User.username == form.username.data, models.User.email == form.username.data)).first()
        if(cur_user and cur_user.check_password(form.password.data) == True):
            login_user(load_user(cur_user.id), remember=form.remember_me.data)
            flash("Вы успешно авторизовались", "success")
            return redirect(url_for('index'))
        else:
            flash("Неверный логин или пароль", "error")
    return render_template('auth.html',
        title = "Auth",
        form = form,
        user = g.user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if(g.user is not None and g.user.is_authenticated): return redirect(url_for('index'))
    form = forms.RegisterForm()
    if(form.validate_on_submit() == True):
        if(models.User.query.filter(or_(models.User.username == form.username.data, models.User.email == form.email.data)).first() is not None):
            flash("Пользователь с таким именем или email уже зарегистрирован", "error")
        else:
            user = models.User(username = form.username.data, email = form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(load_user(user.id), remember=True)
            return redirect(url_for('index'))
    return render_template('register.html',
        title = "Register",
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
            user_id = g.user.id)
        db.session.add(add)
        db.session.commit()
        flash("Запись успешно добавлена" ,"success")
        return redirect(url_for('index'))
    return render_template("log/add.html",
        form = form,
        user = g.user)

@app.route('/log/del/<int:id_>', methods=['GET', 'POST'])
@login_required
def log_del(id_):
    d = models.MoneyLog.query.filter(models.MoneyLog.user_id == g.user.id, models.MoneyLog.id == id_).first_or_404()
    db.session.delete(d)
    db.session.commit()
    flash("Запись успешно удалена", "success")
    return redirect(url_for('index'))