# MoneyLog
Веб-сайт для учёта доходов и расходов написанный на *flask*.

## Требования
- Python 3.8+
- База данных MySQL
- Flask 2.0.0+

## Установка
Копируем репозиторий и устанавливаем необходимые модули:
```
git clone https://git.ezdomain.ru/l27001/moneylog
cd moneylog
pip install -r requirements.txt
```
Открываем `config.py` любым текстовым редактором и меняем `SECRET_KEY` на произвольную строку (желательно > 32 символа).
```
SECRET_KEY = 'rPY@OaVaxjCQiA+hwXeo7-I-LqZPkZZZ'
``` 
Затем меняем данные в строке `SQLALCHEMY_DATABASE_URI` на ваши, к примеру:
```
SQLALCHEMY_DATABASE_URI = 'mysql://MyCoolUsername:myCoolPassword@localhost/myCoolDatabase'
```
Так-же обратите внимание на строки
```
REMEMBER_COOKIE_SECURE = True
REMEMBER_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
```
Если они установлены в `True`, вы не сможете авторизоваться на сайте без HTTPS. При необходимости измените значения на `False`
После этого можно закрыть файл.

Теперь создаём структуру базы данных:
```
./prepare_db.sh
```
В файле `run.py` можете изменить адрес, и порт на котором будет запущен веб-сервер.
```
serve(app, host = "127.0.0.1", port = 5088, url_scheme = 'https')
```
Теперь можно запустить скрипт `run.py` и зайти на сайт (адрес по-умолчанию: `http://127.0.0.1:5088`)
```
python run.py
```

## Демо
https://moneylog.ezdomain.ru