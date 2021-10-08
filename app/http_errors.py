from flask import render_template, g
from app import app

@app.errorhandler(413)
def request_too_large(e):
    return render_template('error.html',
        title = f"Ошибка #{e.code}",
        user = g.user,
        name = "Тело запроса слишком велико",
        description = 'Переданные вами данные/файл превышают лимит сервера. \
        Попробуйте уменьшить передаваемый объём данных.'), e.code

@app.errorhandler(405)
def not_found(e):
    return render_template('error.html',
        title = f"Ошибка #{e.code}",
        user = g.user,
        name = "Метод не разрешён",
        description = 'Запрашиваемый вами метод не применим к данной странице.'), e.code

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html',
        title = f"Ошибка #{e.code}",
        user = g.user,
        name = "Страница не найдена",
        description = 'Страница которую вы запросили не может быть найдена. \
        Возможно она была удалена или перемещена.'), e.code

@app.errorhandler(403)
def no_access(e):
    return render_template('error.html',
        title = f"Ошибка #{e.code}",
        user = g.user,
        name = "Доступ запрещён",
        description = 'У Вас нет прав доступа к этому объекту. \
        Файл недоступен для чтения, или сервер не может его прочитать.'), e.code

@app.errorhandler(401)
def auth_required(e):
    return render_template('error.html',
        title = f"Ошибка #{e.code}",
        user = g.user,
        name = "Требуется аутентификация",
        description = 'Вы не прошли аутентификацию для просмотра данной страницы.'), e.code

@app.errorhandler(400)
def auth_required(e):
    return render_template('error.html',
        title = f"Ошибка #{e.code}",
        user = g.user,
        name = "Ошибка запроса",
        description = 'Запрос отправленный браузером содержит ошибку, либо не содержит важных данных.'), e.code

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html',
        title = f"Ошибка #{e.code}",
        user = g.user,
        name = "Внутренняя ошибка сервера",
        description = 'Произошла неизвестная ошибка. \
        Попробуйте обновить страницу, или вернитесь сюда позже.'), e.code
