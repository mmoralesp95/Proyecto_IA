from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    Swagger(app)

    @app.route("/")
    def home():
        return "¡Hola, Flask está funcionando!"

    from .routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
