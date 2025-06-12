from flask import Flask
from src.routes import weather_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(weather_bp)
    return app