# run.py
from flask import Flask
from app.routes.routes import routes
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "app", "templates"))
app.secret_key = 'mi_clave_secreta_ultrasegura_2024'  # ¡Cambia este valor en producción!
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)