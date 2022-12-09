import eventlet
from eventlet import wsgi
from app import create_app

# app = create_app("development")
# wsgi.server(eventlet.listen(("", 80)), app)

app = create_app("production")
if __name__ == "__main__":
    app.run()
