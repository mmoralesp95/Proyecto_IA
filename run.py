# run.py
from flask import Flask
from app.routes.routes import routes
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "app", "templates"))
app.secret_key = os.getenv("APP_SECRET_KEY", "default")
app.register_blueprint(routes)

@app.route("/")
def hello():
    return "¡Hola, soy Miguel, bienvenido a mi app!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)