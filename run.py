#!/usr/bin/python3
from app import app
if(__name__ == "__main__"):
    from waitress import serve
    serve(app, host = "127.0.0.1", port = 5088)
    # serve(app, host = "127.0.0.1", port = 5088, url_scheme = "https") # Автоматическое перенаправление на HTTPS
