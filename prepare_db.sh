#!/bin/sh
type flask >/dev/null 2>&1 || { echo >&2 "[!] flask не найден в \$PATH. Прерывание."; exit 1; }
type python >/dev/null 2>&1 || { echo >&2 "[!] python не найден в \$PATH. Прерывание."; exit 1; }
set -e
echo "[i] Создаём базу данных..."
flask db init
flask db migrate -m "Init"
flask db upgrade
echo "[i] Добавляем стандартные записи..."
python -c 'from app import db, models; db.engine.execute("SET sql_mode = NO_AUTO_VALUE_ON_ZERO"); db.session.add(models.User(id=0, username="Guest", password="", email="guest@example.com")); db.session.commit()'
echo "[+] Готово!"
