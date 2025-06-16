from flask import Flask
from flasgger import Swagger
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def create_app():

    app = Flask(__name__)
    Swagger(app)

    @app.route("/")
    def home():
        return "¡Hola, Flask está funcionando!"

    from app.routes.routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
