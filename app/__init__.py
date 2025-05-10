from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
