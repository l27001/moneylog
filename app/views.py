from flask import render_template, abort, request, redirect, url_for, g, session, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app import app, forms, models, db

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
    return models.User.query.filter_by(id=user_id).first_or_404()

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',
        title="Index page",
        user=g.user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if(g.user is not None and g.user.is_authenticated): return redirect(url_for('index'))
    form = forms.LoginForm()
    if(form.validate_on_submit() == True):
        cur_user = models.User.query.filter_by(username=form.username.data).first_or_404()
        if(cur_user and cur_user.check_password(form.password.data) == True):
            login_user(load_user(cur_user.id), remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash("Неверный логин или пароль")
    return render_template('auth.html',
        title = "Auth",
        form = form)