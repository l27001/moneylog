#!/usr/bin/python3
from app import app
if(__name__ == "__main__"):
    # app.run('127.0.0.1', port = 5088, debug = True)
    from waitress import serve
    serve(app, host = "0.0.0.0", port = 5088, url_scheme = 'https')
